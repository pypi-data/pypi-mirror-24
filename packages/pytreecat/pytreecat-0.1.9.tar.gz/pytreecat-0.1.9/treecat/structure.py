from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
from collections import defaultdict
from collections import deque

import numba
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree

from six.moves import range
from six.moves import zip
from treecat.util import COUNTERS
from treecat.util import HISTOGRAMS
from treecat.util import SERIES
from treecat.util import jit
from treecat.util import profile
from treecat.util import sample_from_probs

logger = logging.getLogger(__name__)


class TreeStructure(object):
    """Topological data representing a tree on features."""

    def __init__(self, num_vertices):
        logger.debug('TreeStructure with %d vertices', num_vertices)
        self._num_vertices = num_vertices
        self._num_edges = num_vertices - 1
        self.set_edges([(v, v + 1) for v in range(num_vertices - 1)])
        self._complete_grid = None  # Lazily constructed.
        self._vertices = np.arange(num_vertices, dtype=np.int32)

    def __eq__(self, other):
        return (self._num_vertices == other._num_vertices and  #
                (self._tree_grid == other._tree_grid).all())

    def set_edges(self, edges):
        """Sets the edges of this tree.

        Args:
            edges: A list of (vertex, vertex) pairs.
        """
        assert len(edges) == self._num_edges
        self._tree_grid = make_tree(edges)

    def get_edges(self):
        """Returns the edges of this tree.

        Returns:
            A list of (vertex, vertex) pairs.
        """
        return [(v1, v2) for e, v1, v2 in self._tree_grid.T]

    @property
    def num_vertices(self):
        return self._num_vertices

    @property
    def num_edges(self):
        return self._num_edges

    @property
    def tree_grid(self):
        """Array of (edge, vertex, vertex) triples defining the tree graph."""
        return self._tree_grid

    @property
    def complete_grid(self):
        """Array of (edge,vertex,vertex) triples defining a complete graph."""
        if self._complete_grid is None:
            self._complete_grid = make_complete_graph(self._num_vertices)
        return self._complete_grid

    @property
    def vertices(self):
        return self._vertices

    def gc(self):
        """Garbage collect temporary cached data structures."""
        self._complete_grid = None


@jit(numba.int32(numba.int32, numba.int32), nopython=True, cache=True)
def find_complete_edge(v1, v2):
    """Find the edge index k of an unsorted pair of vertices (v1, v2)."""
    if v2 < v1:
        v1, v2 = v2, v1
    return v1 + v2 * (v2 - 1) // 2


def make_complete_graph(num_vertices):
    """Constructs a complete graph.

    The pairing function is: k = v1 + v2 * (v2 - 1) // 2

    Args:
        num_vertices: Number of vertices.

    Returns: A tuple with elements:
        V: Number of vertices.
        K: Number of edges.
        grid: a 3 x K grid of (edge, vertex, vertex) triples.
    """
    V = num_vertices
    K = V * (V - 1) // 2
    grid = np.zeros([3, K], np.int32)
    k = 0
    for v2 in range(V):
        for v1 in range(v2):
            grid[:, k] = [k, v1, v2]
            k += 1
    return grid


def make_tree(edges):
    """Constructs a tree graph from a set of (vertex,vertex) pairs.

    Args:
        edges: A list or set of unordered (vertex, vertex) pairs.

    Returns: A tuple with elements:
        V: Number of vertices.
        E: Number of edges.
        grid: a 3 x E grid of (edge, vertex, vertex) triples.
    """
    assert all(isinstance(edge, tuple) for edge in edges)
    edges = [tuple(sorted(edge)) for edge in edges]
    edges.sort()
    E = len(edges)
    grid = np.zeros([3, E], np.int32)
    for e, (v1, v2) in enumerate(edges):
        grid[:, e] = [e, v1, v2]
    return grid


def find_center_of_tree(grid):
    """Finds a maximally central vertex in a tree graph.

    Args:
        grid: A tree graph as returned by make_tree().

    Returns:
        Vertex id of a maximally central vertex.
    """
    E = grid.shape[1]
    V = 1 + E
    neighbors = [set() for _ in range(V)]
    for e, v1, v2 in grid.T:
        neighbors[v1].add(v2)
        neighbors[v2].add(v1)
    queue = deque()
    for v in reversed(range(V)):
        if len(neighbors[v]) <= 1:
            queue.append(v)
    while queue:
        v = queue.popleft()
        for v2 in sorted(neighbors[v], reverse=True):
            neighbors[v2].remove(v)
            if len(neighbors[v2]) == 1:
                queue.append(v2)
    return v


# Op codes for propagation programs.
OP_UP = 0
OP_IN = 1
OP_ROOT = 2
OP_OUT = 3
OP_DOWN = 4


def make_propagation_program(grid, root=None):
    """Makes an efficient program for message passing on a tree.

    This creates a program of instructions to be intrepreted by various
    virtual machines. Each 8-byte instruction is broken into 4 2-byte chunks:

      [ op_code | vertex | relative_vertex | relative_edge ]

    where the relative_* operands are optional.
    The five instructions are (in order of occurrence at each vertex):

      OP_UP: Propagate upwards from observed state to latent state.
          vertex: The current vertex.
          relative_vertex: Not set.
          relative_edge: Not set.

      OP_IN: Propagate inwards from latent leaves towards latent root,
          assuming OP_UP has already been called on this vertex.
          vertex: The target parent vertex.
          relative_vertex: The source child vertex.
          relative_edge: The edge between parent and child.

      OP_ROOT: Process the root node after OP_UP and OP_IN have been called.
          vertex: The root vertex.
          relative_vertex: Not set.
          relative_edge: Not set.

      OP_OUT: Popagate outwards from the latent root towards latent leaves,
          assuming OP_UP and OP_IN have been called as needed.
          vertex: The target child vertex.
          relative_vertex: The source parent vertex.
          relative_edge: The edge between parent and child.

      OP_DOWN: Propagate downwards from latent state to observed state,
          assuming OP_UP, OP_IN, and OP_OUT have been called as needed.
          vertices and OP_IN has been called on all edges.
          vertex: The current vertex.
          relative_vertex: Not set.
          relative_edge: Not set.

    Args:
        grid: A tree graph as returned by make_tree().
        root: Optional root vertex, defaults to find_center_of_tree(grid).

    Returns:
        A [V+E+1+E+V, 4]-shaped numpy array whose rows are instructions.
    """
    if root is None:
        root = find_center_of_tree(grid)
    E = grid.shape[1]
    V = 1 + E
    neighbors = [set() for _ in range(V)]
    edge_dict = {}
    for e, v1, v2 in grid.T:
        neighbors[v1].add(v2)
        neighbors[v2].add(v1)
        edge_dict[v1, v2] = e
        edge_dict[v2, v1] = e

    # Construct a nested program.
    nested_program = []
    queue = deque()
    queue.append((root, None))
    while queue:
        v, parent = queue.popleft()
        nested_program.append((v, parent, []))
        for v2 in sorted(neighbors[v]):
            if v2 != parent:
                queue.append((v2, v))
    for v, parent, children in nested_program:
        for v2 in sorted(neighbors[v]):
            if v2 != parent:
                children.append(v2)

    # Construct a flattened program.
    program = np.zeros([V + E + 1 + E + V, 4], np.int16)
    pos = 0
    for v, parent, children in reversed(nested_program):
        program[pos, :] = [OP_UP, v, 0, 0]
        pos += 1
        for child in children:
            program[pos, :] = [OP_IN, v, child, edge_dict[v, child]]
            pos += 1
    program[pos, :] = [OP_ROOT, root, 0, 0]
    pos += 1
    for v, parent, children in nested_program:
        if parent is not None:
            program[pos, :] = [OP_OUT, v, parent, edge_dict[v, parent]]
            pos += 1
        program[pos, :] = [OP_DOWN, v, 0, 0]
        pos += 1
    assert pos == program.shape[0]

    return program


# A jit_set is an array representation of a set of 16-bit integers.
# The memory layout is:
# [ size | item[1] | item[2] | ... | item[size] | unused | ... | unused ]


@jit(nopython=True, cache=True)
def jit_set_add(jit_set, item):
    """Add an item to a jit_set.

    Warning: this assumes item is not already in the set.
    """
    size = jit_set[0] + 1
    jit_set[0] = size
    jit_set[size] = item


@jit(nopython=True, cache=True)
def jit_set_pop(jit_set):
    """Remove and return an arbitrary item from a jit_set."""
    size = jit_set[0]
    jit_set[0] = size - 1
    return jit_set[size]


@jit(nopython=True, cache=True)
def jit_set_remove(jit_set, item):
    """Remove the given item from a jit_set.

    Warning: this does not preserve order.
    """
    pos = 1
    while jit_set[pos] != item:
        pos += 1
    size = jit_set[0]
    if pos != size:
        jit_set[pos] = jit_set[size]
    jit_set[0] = size - 1


@jit(nopython=True, cache=True)
def jit_remove_edge(grid, e2k, neighbors, components, e):
    """Remove an edge from a spanning tree."""
    k = e2k[e]
    v1, v2 = grid[1:3, k]
    jit_set_remove(neighbors[v1], v2)
    jit_set_remove(neighbors[v2], v1)
    stack = np.zeros(neighbors.shape[0], np.int16)
    jit_set_add(stack, v1)
    while stack[0]:
        v1 = jit_set_pop(stack)
        components[v1] = True
        for i in range(neighbors[v1, 0]):
            v2 = neighbors[v1, i + 1]
            if not components[v2]:
                jit_set_add(stack, v2)
    return k


@jit(nopython=True, cache=True)
def jit_add_edge(grid, e2k, neighbors, components, e, k):
    """Add an edge connecting two components to create a spanning tree."""
    e2k[e] = k
    v1, v2 = grid[1:3, k]
    jit_set_add(neighbors[v1], v2)
    jit_set_add(neighbors[v2], v1)
    components[:] = False


@jit(nopython=True, cache=True)
def find_valid_edges(components, valid_edges):
    """Find all edges between two components in a complete undirected graph.

    Args:
        components: A [V]-shaped array of boolean component ids. This assumes
            there are exactly two nonemtpy components.
        valid_edges: An uninitialized array where output is written. On return,
            the subarray valid_edges[:end] will contain edge ids k for all
            valid edges.

    Returns:
        The number of valid edges found.
    """
    k = 0
    end = 0
    for v2, c2 in enumerate(components):
        for v1 in range(v2):
            if c2 ^ components[v1]:
                valid_edges[end] = k
                end += 1
            k += 1
    return end


@profile
def sample_tree(grid, edge_logits, edges):
    """Sample a random spanning tree of a dense weighted graph using MCMC.

    This uses Gibbs sampling on edges. Consider E undirected edges that can
    move around a graph of V=1+E vertices. The edges are constrained so that no
    two edges can span the same pair of vertices and so that the edges must
    form a spanning tree. To Gibbs sample, chose one of the E edges at random
    and move it anywhere else in the graph. After we remove the edge, notice
    that the graph is split into two connected components. The constraints
    imply that the edge must be replaced so as to connect the two components.
    Hence to Gibbs sample, we collect all such bridging (vertex,vertex) pairs
    and sample from them in proportion to exp(edge_logits).

    Args:
        grid: A 3 x K array as returned by make_complete_graph().
        edge_logits: A length-K array of nonnormalized log probabilities.
        edges: A list of E initial edges in the form of (vertex,vertex) pairs.

    Returns:
        A list of (vertex, vertex) pairs.
    """
    logger.debug('sample_tree sampling a random spanning tree')
    COUNTERS.sample_tree_calls += 1
    if len(edges) <= 1:
        return edges
    E = len(edges)
    V = E + 1
    K = V * (V - 1) // 2
    e2k = np.zeros(E, np.int32)
    neighbors = np.zeros((V, V), np.int16)
    components = np.zeros(V, np.bool_)
    for e in range(E):
        v1, v2 = edges[e]
        e2k[e] = find_complete_edge(v1, v2)
        jit_set_add(neighbors[v1], v2)
        jit_set_add(neighbors[v2], v1)
    valid_edges = np.empty(K, np.int32)

    accepted = 0
    log2_choices = []
    for e in np.random.permutation(E):  # Sequential scanning doesn't work.
        k1 = jit_remove_edge(grid, e2k, neighbors, components, e)
        num_valid_edges = find_valid_edges(components, valid_edges)
        valid_probs = edge_logits[valid_edges[:num_valid_edges]]
        valid_probs -= valid_probs.max()
        valid_probs = np.exp(valid_probs)
        total_prob = valid_probs.sum()
        if total_prob > 0:
            k2 = valid_edges[sample_from_probs(valid_probs)]
        else:
            k2 = k1
            COUNTERS.sample_tree_infeasible += 1
        jit_add_edge(grid, e2k, neighbors, components, e, k2)

        accepted += (k1 != k2)
        log2_choices.append(num_valid_edges.bit_length())
    COUNTERS.sample_tree_accept += accepted
    COUNTERS.sample_tree_propose += E
    SERIES.sample_tree_accepted.append(accepted)
    HISTOGRAMS.sample_tree_log2_choices.update(log2_choices)

    edges = sorted((grid[1, k], grid[2, k]) for k in e2k)
    assert len(edges) == E
    return edges


def triangular_to_square(grid, triangle):
    """Convert a packed triangular matrix to a square matrix.

    Args:
        grid: A 3 x K array as returned by make_complete_graph().
        triangle: A length-K array.

    Returns:
        A square symmetric V x V array with zero on the diagonal.
    """
    K = len(triangle)
    assert grid.shape == (3, K)
    V = int(round(0.5 + (0.25 + 2 * K)**0.5))
    assert K == V * (V - 1) // 2
    square = np.zeros([V, V], dtype=triangle.dtype)
    square[grid[1, :], grid[2, :]] = triangle
    square[grid[2, :], grid[1, :]] = triangle
    return square


@profile
def estimate_tree(grid, edge_logits):
    """Compute a maximum likelihood spanning tree of a dense weighted graph.

    Args:
        grid: A 3 x K array as returned by make_complete_graph().
        edge_logits: A length-K array of nonnormalized log probabilities.

    Returns:
        A list of (vertex, vertex) pairs.
    """
    K = len(edge_logits)
    assert grid.shape == (3, K)
    weights = triangular_to_square(grid, edge_logits)
    weights *= -1
    weights -= weights.min()
    weights += 1.0
    csr = minimum_spanning_tree(weights, overwrite=True)
    coo = csr.tocoo()
    edges = zip(coo.row, coo.col)
    edges = sorted(tuple(sorted(pair)) for pair in edges)
    assert len(edges) == weights.shape[0] - 1
    return edges


def print_tree(edges, feature_names, root=None):
    """Returns a text representation of the feature tree.

    Args:
        edges: A list of (vertex, vertex) pairs.
        feature_names: A list of feature names.
        root: The name of the root feature (optional).

    Returns:
        A text representation of the tree with one feature per line.
    """
    assert len(feature_names) == 1 + len(edges)
    if root is None:
        root = feature_names[find_center_of_tree(make_tree(edges))]
    assert root in feature_names
    neighbors = defaultdict(set)
    for v1, v2 in edges:
        neighbors[v1].add(v2)
        neighbors[v2].add(v1)
    stack = [feature_names.index(root)]
    seen = set(stack)
    lines = []
    while stack:
        backtrack = True
        for neighbor in sorted(neighbors[stack[-1]], reverse=True):
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
                backtrack = False
                break
        if backtrack:
            name = feature_names[stack.pop()]
            lines.append((len(stack), name))
    lines.reverse()
    return '\n'.join(['{}{}'.format('  ' * i, n) for i, n in lines])


def order_vertices(edges):
    """Sort vertices using greedy bin packing.

    This is mainly useful for plotting and printing.

    Args:
        edges: A list of (vertex, vertex) pairs.

    Returns:
        An (permutation, inverse) pair, each a list of vertices.
    """
    grid = make_tree(edges)
    root = find_center_of_tree(grid)

    E = len(edges)
    V = E + 1
    neighbors = [set() for _ in range(V)]
    for v1, v2 in edges:
        neighbors[v1].add(v2)
        neighbors[v2].add(v1)
    orders = [None for v in range(V)]
    seen = [False] * V
    stack = [root]
    seen[root] = True
    while stack:
        v = stack[-1]
        done = True
        for v2 in neighbors[v]:
            if not seen[v2]:
                stack.append(v2)
                seen[v2] = True
                done = False
                break
        if not done:
            continue
        lhs = []
        rhs = []
        parts = [(v2, orders[v2]) for v2 in neighbors[v]
                 if orders[v2] is not None]
        parts.sort(key=lambda x: len(x[1]))
        for v2, part in parts:
            midpoint = (len(part) - 1) / 2
            if len(lhs) < len(rhs):
                if part.index(v2) < midpoint:
                    part.reverse()
                lhs = part + lhs
            else:
                if part.index(v2) > midpoint:
                    part.reverse()
                rhs = rhs + part
        orders[v] = lhs + [v] + rhs
        stack.pop()

    order_inv = orders[root]
    order = [None] * V
    for v1, v2 in enumerate(order_inv):
        order[v2] = v1
    return order, order_inv
