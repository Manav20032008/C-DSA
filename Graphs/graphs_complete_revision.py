"""
GRAPHS — COMPLETE DSA REVISION
==============================

Placement-focused revision library covering:
- Graph representations
- BFS / DFS
- Connected components
- Cycle detection
- Bipartite graphs
- Shortest paths
- Dijkstra
- Bellman-Ford
- Floyd-Warshall
- Topological sorting
- Union-Find / DSU
- Kruskal / Prim MST
- Grid BFS / DFS
- Multi-source BFS
- 0-1 BFS
- SCC
- Bridges / articulation points
- Graph cloning
- Common interview patterns

Python implementations.
"""


from collections import deque
import heapq


# ============================================================
# GRAPH REPRESENTATIONS
# ============================================================

class Graph:
    """Basic graph using adjacency lists."""

    def __init__(self, vertices, directed=False):
        self.vertices = vertices
        self.directed = directed
        self.adj = [[] for _ in range(vertices)]

    def add_edge(self, u, v):
        self.adj[u].append(v)

        if not self.directed:
            self.adj[v].append(u)

    def add_weighted_edge(self, u, v, weight):
        self.adj[u].append((v, weight))

        if not self.directed:
            self.adj[v].append((u, weight))

    def __repr__(self):
        return repr(self.adj)


def build_adjacency_matrix(n, edges, directed=False):
    matrix = [[0] * n for _ in range(n)]

    for u, v in edges:
        matrix[u][v] = 1

        if not directed:
            matrix[v][u] = 1

    return matrix


def build_weighted_adjacency_list(n, edges, directed=False):
    adj = [[] for _ in range(n)]

    for u, v, weight in edges:
        adj[u].append((v, weight))

        if not directed:
            adj[v].append((u, weight))

    return adj


# ============================================================
# BFS
# ============================================================

def bfs(graph, start):
    """BFS traversal of a graph."""
    visited = [False] * graph.vertices
    queue = deque([start])
    visited[start] = True
    result = []

    while queue:
        node = queue.popleft()
        result.append(node)

        for neighbor in graph.adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

    return result


def bfs_shortest_path(graph, start):
    """Shortest distance from start in an unweighted graph."""
    distance = [-1] * graph.vertices
    distance[start] = 0

    queue = deque([start])

    while queue:
        node = queue.popleft()

        for neighbor in graph.adj[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                queue.append(neighbor)

    return distance


def bfs_shortest_path_with_parent(graph, start, target):
    """Return shortest path in an unweighted graph."""
    parent = [-1] * graph.vertices
    distance = [-1] * graph.vertices

    distance[start] = 0
    queue = deque([start])

    while queue:
        node = queue.popleft()

        if node == target:
            break

        for neighbor in graph.adj[node]:
            if distance[neighbor] == -1:
                distance[neighbor] = distance[node] + 1
                parent[neighbor] = node
                queue.append(neighbor)

    if distance[target] == -1:
        return []

    path = []
    current = target

    while current != -1:
        path.append(current)
        current = parent[current]

    return path[::-1]


# ============================================================
# DFS — RECURSIVE
# ============================================================

def dfs_recursive(graph, start):
    visited = [False] * graph.vertices
    result = []

    def dfs(node):
        visited[node] = True
        result.append(node)

        for neighbor in graph.adj[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    dfs(start)
    return result


# ============================================================
# DFS — ITERATIVE
# ============================================================

def dfs_iterative(graph, start):
    visited = [False] * graph.vertices
    stack = [start]
    result = []

    while stack:
        node = stack.pop()

        if visited[node]:
            continue

        visited[node] = True
        result.append(node)

        for neighbor in reversed(graph.adj[node]):
            if not visited[neighbor]:
                stack.append(neighbor)

    return result


# ============================================================
# TRAVERSE ALL COMPONENTS
# ============================================================

def connected_components(graph):
    visited = [False] * graph.vertices
    components = []

    for start in range(graph.vertices):
        if visited[start]:
            continue

        component = []
        stack = [start]
        visited[start] = True

        while stack:
            node = stack.pop()
            component.append(node)

            for neighbor in graph.adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    stack.append(neighbor)

        components.append(component)

    return components


def count_connected_components(graph):
    return len(connected_components(graph))


# ============================================================
# CYCLE DETECTION — UNDIRECTED
# ============================================================

def has_cycle_undirected_dfs(graph):
    visited = [False] * graph.vertices

    def dfs(node, parent):
        visited[node] = True

        for neighbor in graph.adj[node]:
            if not visited[neighbor]:
                if dfs(neighbor, node):
                    return True

            elif neighbor != parent:
                return True

        return False

    for node in range(graph.vertices):
        if not visited[node]:
            if dfs(node, -1):
                return True

    return False


def has_cycle_undirected_bfs(graph):
    visited = [False] * graph.vertices

    for start in range(graph.vertices):
        if visited[start]:
            continue

        queue = deque([(start, -1)])
        visited[start] = True

        while queue:
            node, parent = queue.popleft()

            for neighbor in graph.adj[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, node))

                elif neighbor != parent:
                    return True

    return False


# ============================================================
# CYCLE DETECTION — DIRECTED
# ============================================================

def has_cycle_directed_dfs(graph):
    """0 = unvisited, 1 = visiting, 2 = finished."""
    state = [0] * graph.vertices

    def dfs(node):
        state[node] = 1

        for neighbor in graph.adj[node]:
            if state[neighbor] == 1:
                return True

            if state[neighbor] == 0 and dfs(neighbor):
                return True

        state[node] = 2
        return False

    for node in range(graph.vertices):
        if state[node] == 0:
            if dfs(node):
                return True

    return False


# ============================================================
# BIPARTITE GRAPH
# ============================================================

def is_bipartite(graph):
    color = [-1] * graph.vertices

    for start in range(graph.vertices):
        if color[start] != -1:
            continue

        queue = deque([start])
        color[start] = 0

        while queue:
            node = queue.popleft()

            for neighbor in graph.adj[node]:
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)

                elif color[neighbor] == color[node]:
                    return False

    return True


# ============================================================
# TOPOLOGICAL SORT — KAHN'S ALGORITHM
# ============================================================

def topological_sort_kahn(graph):
    indegree = [0] * graph.vertices

    for u in range(graph.vertices):
        for v in graph.adj[u]:
            indegree[v] += 1

    queue = deque(
        node for node in range(graph.vertices)
        if indegree[node] == 0
    )

    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in graph.adj[node]:
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                queue.append(neighbor)

    # If fewer than V vertices were processed, graph has a cycle.
    return order if len(order) == graph.vertices else []


# ============================================================
# TOPOLOGICAL SORT — DFS
# ============================================================

def topological_sort_dfs(graph):
    state = [0] * graph.vertices
    order = []

    def dfs(node):
        state[node] = 1

        for neighbor in graph.adj[node]:
            if state[neighbor] == 1:
                return False

            if state[neighbor] == 0:
                if not dfs(neighbor):
                    return False

        state[node] = 2
        order.append(node)
        return True

    for node in range(graph.vertices):
        if state[node] == 0:
            if not dfs(node):
                return []

    return order[::-1]


# ============================================================
# COURSE SCHEDULE PATTERN
# ============================================================

def can_finish_courses(num_courses, prerequisites):
    """
    prerequisites = [[course, prerequisite], ...]

    Equivalent to checking whether the directed
    prerequisite graph contains a cycle.
    """
    graph = Graph(num_courses, directed=True)

    for course, prerequisite in prerequisites:
        graph.add_edge(prerequisite, course)

    return len(topological_sort_kahn(graph)) == num_courses


def course_order(num_courses, prerequisites):
    graph = Graph(num_courses, directed=True)

    for course, prerequisite in prerequisites:
        graph.add_edge(prerequisite, course)

    return topological_sort_kahn(graph)


# ============================================================
# DIJKSTRA
# ============================================================

def dijkstra(graph, start):
    """
    graph.adj[u] contains (v, weight).

    Requires NON-NEGATIVE edge weights.
    """
    distances = [float("inf")] * graph.vertices
    distances[start] = 0

    heap = [(0, start)]

    while heap:
        current_distance, node = heapq.heappop(heap)

        if current_distance != distances[node]:
            continue

        for neighbor, weight in graph.adj[node]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(
                    heap,
                    (new_distance, neighbor)
                )

    return distances


def dijkstra_with_parent(graph, start):
    distances = [float("inf")] * graph.vertices
    parent = [-1] * graph.vertices
    distances[start] = 0

    heap = [(0, start)]

    while heap:
        current_distance, node = heapq.heappop(heap)

        if current_distance != distances[node]:
            continue

        for neighbor, weight in graph.adj[node]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parent[neighbor] = node
                heapq.heappush(
                    heap,
                    (new_distance, neighbor)
                )

    return distances, parent


def reconstruct_path(parent, start, target):
    if target != start and parent[target] == -1:
        return []

    path = []
    current = target

    while current != -1:
        path.append(current)

        if current == start:
            break

        current = parent[current]

    if path[-1] != start:
        return []

    return path[::-1]


# ============================================================
# BELLMAN-FORD
# ============================================================

def bellman_ford(n, edges, source):
    """
    edges = [(u, v, weight), ...]

    Handles negative edges.
    Returns:
        (distances, has_negative_cycle)
    """
    distances = [float("inf")] * n
    distances[source] = 0

    for _ in range(n - 1):
        changed = False

        for u, v, weight in edges:
            if distances[u] == float("inf"):
                continue

            candidate = distances[u] + weight

            if candidate < distances[v]:
                distances[v] = candidate
                changed = True

        if not changed:
            break

    negative_cycle = False

    for u, v, weight in edges:
        if distances[u] == float("inf"):
            continue

        if distances[u] + weight < distances[v]:
            negative_cycle = True
            break

    return distances, negative_cycle


# ============================================================
# FLOYD-WARSHALL
# ============================================================

def floyd_warshall(n, edges, directed=True):
    INF = float("inf")
    distance = [[INF] * n for _ in range(n)]

    for i in range(n):
        distance[i][i] = 0

    for u, v, weight in edges:
        distance[u][v] = min(distance[u][v], weight)

        if not directed:
            distance[v][u] = min(distance[v][u], weight)

    for via in range(n):
        for u in range(n):
            if distance[u][via] == INF:
                continue

            for v in range(n):
                candidate = (
                    distance[u][via] +
                    distance[via][v]
                )

                if candidate < distance[u][v]:
                    distance[u][v] = candidate

    return distance


def has_negative_cycle_floyd_warshall(distance):
    return any(
        distance[i][i] < 0
        for i in range(len(distance))
    )


# ============================================================
# DISJOINT SET UNION / UNION-FIND
# ============================================================

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        # Union by rank.
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a

        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1

        return True

    def union_by_size(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a

        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]

        return True

    def connected(self, a, b):
        return self.find(a) == self.find(b)


def has_cycle_using_dsu(n, edges):
    dsu = DSU(n)

    for u, v in edges:
        if not dsu.union(u, v):
            return True

    return False


# ============================================================
# KRUSKAL MST
# ============================================================

def kruskal_mst(n, edges):
    """
    edges = [(u, v, weight), ...]

    Returns:
        (total_weight, mst_edges)

    If graph is disconnected, mst_edges will not contain
    n - 1 edges.
    """
    dsu = DSU(n)
    mst_edges = []
    total_weight = 0

    for u, v, weight in sorted(edges, key=lambda e: e[2]):
        if dsu.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight

            if len(mst_edges) == n - 1:
                break

    return total_weight, mst_edges


# ============================================================
# PRIM MST
# ============================================================

def prim_mst(graph):
    """
    graph must be an undirected weighted graph.
    Returns (total_weight, mst_edges).
    """
    if graph.vertices == 0:
        return 0, []

    visited = [False] * graph.vertices
    heap = [(0, 0, -1)]
    total_weight = 0
    mst_edges = []

    while heap:
        weight, node, parent = heapq.heappop(heap)

        if visited[node]:
            continue

        visited[node] = True
        total_weight += weight

        if parent != -1:
            mst_edges.append((parent, node, weight))

        for neighbor, edge_weight in graph.adj[node]:
            if not visited[neighbor]:
                heapq.heappush(
                    heap,
                    (edge_weight, neighbor, node)
                )

    return total_weight, mst_edges


# ============================================================
# GRID GRAPH — DFS
# ============================================================

DIRECTIONS_4 = [
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1),
]


def count_islands(grid):
    """
    grid contains '1' for land and '0' for water.
    """
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    grid = [row[:] for row in grid]
    count = 0

    def dfs(r, c):
        if (
            r < 0 or r >= rows or
            c < 0 or c >= cols or
            grid[r][c] != "1"
        ):
            return

        grid[r][c] = "0"

        for dr, dc in DIRECTIONS_4:
            dfs(r + dr, c + dc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)

    return count


def flood_fill(image, sr, sc, color):
    rows = len(image)
    cols = len(image[0])

    original = image[sr][sc]

    if original == color:
        return image

    def dfs(r, c):
        if (
            r < 0 or r >= rows or
            c < 0 or c >= cols or
            image[r][c] != original
        ):
            return

        image[r][c] = color

        for dr, dc in DIRECTIONS_4:
            dfs(r + dr, c + dc)

    dfs(sr, sc)
    return image


# ============================================================
# GRID BFS — SHORTEST PATH
# ============================================================

def shortest_path_binary_grid(grid):
    """
    0 = open, 1 = blocked.
    Returns shortest distance from top-left to bottom-right.
    """
    if not grid or grid[0][0] != 0:
        return -1

    rows = len(grid)
    cols = len(grid[0])

    distance = [[-1] * cols for _ in range(rows)]
    distance[0][0] = 1

    queue = deque([(0, 0)])

    while queue:
        r, c = queue.popleft()

        if r == rows - 1 and c == cols - 1:
            return distance[r][c]

        for dr, dc in DIRECTIONS_4:
            nr = r + dr
            nc = c + dc

            if (
                0 <= nr < rows and
                0 <= nc < cols and
                grid[nr][nc] == 0 and
                distance[nr][nc] == -1
            ):
                distance[nr][nc] = distance[r][c] + 1
                queue.append((nr, nc))

    return -1


# ============================================================
# MULTI-SOURCE BFS
# ============================================================

def rotten_oranges(grid):
    """
    0 = empty
    1 = fresh
    2 = rotten

    Returns minutes to rot all oranges, or -1.
    """
    if not grid:
        return 0

    rows = len(grid)
    cols = len(grid[0])

    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))

            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0

    while queue and fresh:
        for _ in range(len(queue)):
            r, c = queue.popleft()

            for dr, dc in DIRECTIONS_4:
                nr = r + dr
                nc = c + dc

                if (
                    0 <= nr < rows and
                    0 <= nc < cols and
                    grid[nr][nc] == 1
                ):
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))

        minutes += 1

    return -1 if fresh else minutes


# ============================================================
# 0-1 BFS
# ============================================================

def zero_one_bfs(graph, source):
    """
    graph.adj[u] contains (v, weight), where weight is 0 or 1.
    """
    distances = [float("inf")] * graph.vertices
    distances[source] = 0

    queue = deque([source])

    while queue:
        node = queue.popleft()

        for neighbor, weight in graph.adj[node]:
            new_distance = distances[node] + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance

                if weight == 0:
                    queue.appendleft(neighbor)
                else:
                    queue.append(neighbor)

    return distances


# ============================================================
# STRONGLY CONNECTED COMPONENTS — KOSARAJU
# ============================================================

def strongly_connected_components_kosaraju(graph):
    n = graph.vertices
    visited = [False] * n
    finish_order = []

    def dfs1(node):
        visited[node] = True

        for neighbor in graph.adj[node]:
            if not visited[neighbor]:
                dfs1(neighbor)

        finish_order.append(node)

    for node in range(n):
        if not visited[node]:
            dfs1(node)

    reverse_graph = [[] for _ in range(n)]

    for u in range(n):
        for v in graph.adj[u]:
            reverse_graph[v].append(u)

    visited = [False] * n
    components = []

    def dfs2(node, component):
        visited[node] = True
        component.append(node)

        for neighbor in reverse_graph[node]:
            if not visited[neighbor]:
                dfs2(neighbor, component)

    for node in reversed(finish_order):
        if not visited[node]:
            component = []
            dfs2(node, component)
            components.append(component)

    return components


# ============================================================
# STRONGLY CONNECTED COMPONENTS — TARJAN
# ============================================================

def strongly_connected_components_tarjan(graph):
    n = graph.vertices
    discovery = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    stack = []

    timer = 0
    components = []

    def dfs(node):
        nonlocal timer

        discovery[node] = timer
        low[node] = timer
        timer += 1

        stack.append(node)
        on_stack[node] = True

        for neighbor in graph.adj[node]:
            if discovery[neighbor] == -1:
                dfs(neighbor)
                low[node] = min(
                    low[node],
                    low[neighbor]
                )

            elif on_stack[neighbor]:
                low[node] = min(
                    low[node],
                    discovery[neighbor]
                )

        if low[node] == discovery[node]:
            component = []

            while True:
                current = stack.pop()
                on_stack[current] = False
                component.append(current)

                if current == node:
                    break

            components.append(component)

    for node in range(n):
        if discovery[node] == -1:
            dfs(node)

    return components


# ============================================================
# BRIDGES — TARJAN
# ============================================================

def find_bridges(graph):
    """
    Undirected graph.
    Returns edges whose removal increases number of components.
    """
    n = graph.vertices
    discovery = [-1] * n
    low = [0] * n
    timer = 0
    bridges = []

    def dfs(node, parent):
        nonlocal timer

        discovery[node] = low[node] = timer
        timer += 1

        for neighbor in graph.adj[node]:
            if neighbor == parent:
                continue

            if discovery[neighbor] == -1:
                dfs(neighbor, node)

                low[node] = min(
                    low[node],
                    low[neighbor]
                )

                if low[neighbor] > discovery[node]:
                    bridges.append((node, neighbor))

            else:
                low[node] = min(
                    low[node],
                    discovery[neighbor]
                )

    for node in range(n):
        if discovery[node] == -1:
            dfs(node, -1)

    return bridges


# ============================================================
# ARTICULATION POINTS
# ============================================================

def find_articulation_points(graph):
    n = graph.vertices
    discovery = [-1] * n
    low = [0] * n
    timer = 0
    articulation = set()

    def dfs(node, parent):
        nonlocal timer

        discovery[node] = low[node] = timer
        timer += 1

        children = 0

        for neighbor in graph.adj[node]:
            if neighbor == parent:
                continue

            if discovery[neighbor] == -1:
                children += 1

                dfs(neighbor, node)

                low[node] = min(
                    low[node],
                    low[neighbor]
                )

                if parent != -1 and low[neighbor] >= discovery[node]:
                    articulation.add(node)

            else:
                low[node] = min(
                    low[node],
                    discovery[neighbor]
                )

        if parent == -1 and children > 1:
            articulation.add(node)

    for node in range(n):
        if discovery[node] == -1:
            dfs(node, -1)

    return sorted(articulation)


# ============================================================
# GRAPH CLONING
# ============================================================

class GraphNode:
    def __init__(self, value=0, neighbors=None):
        self.value = value
        self.neighbors = neighbors if neighbors else []


def clone_graph(node):
    if node is None:
        return None

    clones = {}

    def dfs(current):
        if current in clones:
            return clones[current]

        copy = GraphNode(current.value)
        clones[current] = copy

        for neighbor in current.neighbors:
            copy.neighbors.append(dfs(neighbor))

        return copy

    return dfs(node)


# ============================================================
# WORD LADDER PATTERN
# ============================================================

def word_ladder_length(begin_word, end_word, word_list):
    words = set(word_list)

    if end_word not in words:
        return 0

    queue = deque([(begin_word, 1)])
    visited = {begin_word}

    while queue:
        word, distance = queue.popleft()

        if word == end_word:
            return distance

        for i in range(len(word)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                candidate = (
                    word[:i] +
                    ch +
                    word[i + 1:]
                )

                if candidate in words and candidate not in visited:
                    visited.add(candidate)
                    queue.append(
                        (candidate, distance + 1)
                    )

    return 0


# ============================================================
# NUMBER OF PROVINCES / COMPONENTS FROM MATRIX
# ============================================================

def number_of_provinces(is_connected):
    n = len(is_connected)
    visited = [False] * n
    count = 0

    def dfs(node):
        visited[node] = True

        for neighbor in range(n):
            if (
                is_connected[node][neighbor] == 1
                and not visited[neighbor]
            ):
                dfs(neighbor)

    for node in range(n):
        if not visited[node]:
            count += 1
            dfs(node)

    return count


# ============================================================
# CHEAT SHEET
# ============================================================

"""
GRAPH PATTERN RECOGNITION
=========================

1. Need visit all reachable nodes?
   -> DFS / BFS

2. Need shortest path in UNWEIGHTED graph?
   -> BFS

3. Need shortest path with NON-NEGATIVE weights?
   -> Dijkstra

4. Negative edge weights?
   -> Bellman-Ford

5. All-pairs shortest paths?
   -> Floyd-Warshall

6. Need dependency ordering?
   -> Topological Sort

7. Directed graph + prerequisite relation?
   -> Topological Sort / cycle detection

8. Need dynamic connectivity?
   -> DSU / Union-Find

9. Need Minimum Spanning Tree?
   -> Kruskal / Prim

10. Need connected components?
    -> DFS / BFS / DSU

11. Need detect cycle in undirected graph?
    -> DFS with parent OR DSU

12. Need detect cycle in directed graph?
    -> DFS recursion state OR Kahn

13. Need two-color graph?
    -> Bipartite BFS / DFS

14. Grid considered as graph?
    -> BFS / DFS

15. Multiple starting sources expanding simultaneously?
    -> Multi-source BFS

16. Edge weights only 0 or 1?
    -> 0-1 BFS

17. Strongly connected directed regions?
    -> Kosaraju / Tarjan

18. Edge whose removal disconnects graph?
    -> Bridge

19. Vertex whose removal disconnects graph?
    -> Articulation point

20. Prefix transformation / word transformation?
    -> Often BFS + pattern buckets

21. Need autocomplete / prefix lookup?
    -> Trie


COMPLEXITY CHEAT SHEET
======================

V = vertices
E = edges

Adjacency list:
    Space: O(V + E)

Adjacency matrix:
    Space: O(V²)

BFS:
    Time:  O(V + E)
    Space: O(V)

DFS:
    Time:  O(V + E)
    Space: O(V)

Connected components:
    O(V + E)

Cycle detection:
    O(V + E)

Bipartite:
    O(V + E)

Topological sort:
    O(V + E)

Dijkstra with binary heap:
    O((V + E) log V)

Bellman-Ford:
    O(VE)

Floyd-Warshall:
    O(V³)

DSU:
    Almost O(1) amortized per operation
    More precisely O(alpha(V))

Kruskal:
    O(E log E)

Prim with heap:
    O(E log V)

Kosaraju:
    O(V + E)

Tarjan SCC:
    O(V + E)

Bridges:
    O(V + E)

Articulation points:
    O(V + E)


DIJKSTRA WARNING
================

Dijkstra DOES NOT work correctly with negative edge weights.

Use Bellman-Ford when negative edges matter.


DAG
===

DAG = Directed Acyclic Graph.

Useful for:
    - dependencies
    - scheduling
    - compilation
    - course prerequisites
    - dynamic programming on graphs

Topological order exists ONLY for DAGs.


MST
===

Minimum Spanning Tree:

    - connects all vertices
    - exactly V - 1 edges
    - no cycle
    - minimum total edge weight

Kruskal:
    Sort edges + DSU

Prim:
    Grow tree using minimum outgoing edge


BFS VS DFS
==========

BFS:
    queue
    level-by-level
    shortest path in unweighted graph

DFS:
    stack / recursion
    deep exploration
    components
    cycle detection
    topological DFS
    bridges / articulation points


IMPORTANT INTERVIEW QUESTIONS
=============================

1. Number of Islands
2. Clone Graph
3. Course Schedule
4. Course Schedule II
5. Number of Connected Components
6. Graph Valid Tree
7. Is Graph Bipartite?
8. Rotting Oranges
9. Word Ladder
10. Pacific Atlantic Water Flow
11. Surrounded Regions
12. Flood Fill
13. Shortest Path in Binary Matrix
14. Network Delay Time
15. Cheapest Flights Within K Stops
16. Path With Minimum Effort
17. Reconstruct Itinerary
18. Alien Dictionary
19. Accounts Merge
20. Redundant Connection
21. Min Cost to Connect All Points
22. Network Connectivity
23. Critical Connections
24. Number of Provinces
25. Evaluate Division
26. Open the Lock
27. Snakes and Ladders
28. Swim in Rising Water
29. Graph shortest path variants
30. MST variants


PLACEMENT CHECKLIST
===================

BASICS
[ ] Graph terminology
[ ] Directed / undirected
[ ] Weighted / unweighted
[ ] Adjacency list
[ ] Adjacency matrix
[ ] Edge insertion

TRAVERSAL
[ ] BFS
[ ] DFS recursive
[ ] DFS iterative
[ ] Connected components
[ ] Shortest unweighted path

CYCLES
[ ] Undirected DFS
[ ] Undirected BFS
[ ] DSU cycle detection
[ ] Directed DFS
[ ] Kahn cycle detection

STRUCTURAL
[ ] Bipartite graph
[ ] Topological sort DFS
[ ] Topological sort Kahn
[ ] Course Schedule

SHORTEST PATH
[ ] BFS
[ ] Dijkstra
[ ] Bellman-Ford
[ ] Floyd-Warshall
[ ] 0-1 BFS
[ ] Path reconstruction

MST
[ ] DSU
[ ] Kruskal
[ ] Prim

GRID
[ ] Number of Islands
[ ] Flood Fill
[ ] Grid BFS
[ ] Multi-source BFS
[ ] Shortest grid path

ADVANCED
[ ] SCC — Kosaraju
[ ] SCC — Tarjan
[ ] Bridges
[ ] Articulation points
[ ] Graph cloning
[ ] Word Ladder pattern

THE GOLDEN GRAPH QUESTIONS
==========================

Before coding, ask:

1. Is the graph directed or undirected?
2. Is it weighted?
3. Are weights negative?
4. Do I need reachability or shortest path?
5. Is shortest path weighted or unweighted?
6. Is there a cycle?
7. Is this a dependency problem?
8. Do I need all connected components?
9. Is this actually a grid graph?
10. Are there multiple sources?
11. Is this an MST problem?
12. Can DSU simplify the problem?
13. Is the graph a DAG?
14. Do I need strongly connected components?

If you answer these before coding,
the algorithm often becomes obvious.
"""


# ============================================================
# TESTS
# ============================================================

def run_revision_tests():

    # Undirected graph.
    graph = Graph(5)

    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)

    assert bfs(graph, 0) == [0, 1, 2, 3, 4]
    assert dfs_recursive(graph, 0) == [0, 1, 3, 2, 4]

    assert bfs_shortest_path(graph, 0) == [0, 1, 1, 2, 2]
    assert bfs_shortest_path_with_parent(graph, 0, 4) == [0, 2, 4]

    assert count_connected_components(graph) == 1
    assert not has_cycle_undirected_dfs(graph)
    assert not has_cycle_undirected_bfs(graph)

    # Cycle.
    cyclic = Graph(3)
    cyclic.add_edge(0, 1)
    cyclic.add_edge(1, 2)
    cyclic.add_edge(2, 0)

    assert has_cycle_undirected_dfs(cyclic)
    assert has_cycle_undirected_bfs(cyclic)

    # Bipartite.
    bipartite = Graph(4)
    bipartite.add_edge(0, 1)
    bipartite.add_edge(0, 3)
    bipartite.add_edge(2, 1)
    bipartite.add_edge(2, 3)

    assert is_bipartite(bipartite)

    # Directed DAG.
    dag = Graph(6, directed=True)
    dag.add_edge(5, 2)
    dag.add_edge(5, 0)
    dag.add_edge(4, 0)
    dag.add_edge(4, 1)
    dag.add_edge(2, 3)
    dag.add_edge(3, 1)

    order = topological_sort_kahn(dag)
    assert len(order) == 6

    position = {node: i for i, node in enumerate(order)}

    for u in range(dag.vertices):
        for v in dag.adj[u]:
            assert position[u] < position[v]

    assert topological_sort_dfs(dag)

    directed_cycle = Graph(3, directed=True)
    directed_cycle.add_edge(0, 1)
    directed_cycle.add_edge(1, 2)
    directed_cycle.add_edge(2, 0)

    assert has_cycle_directed_dfs(directed_cycle)
    assert topological_sort_kahn(directed_cycle) == []
    assert topological_sort_dfs(directed_cycle) == []

    # Course Schedule.
    assert can_finish_courses(
        2,
        [[1, 0]]
    )

    assert not can_finish_courses(
        2,
        [[1, 0], [0, 1]]
    )

    assert course_order(
        2,
        [[1, 0]]
    ) == [0, 1]

    # Dijkstra.
    weighted = Graph(5)

    weighted.add_weighted_edge(0, 1, 2)
    weighted.add_weighted_edge(0, 2, 4)
    weighted.add_weighted_edge(1, 2, 1)
    weighted.add_weighted_edge(1, 3, 7)
    weighted.add_weighted_edge(2, 4, 3)
    weighted.add_weighted_edge(3, 4, 1)

    assert dijkstra(weighted, 0) == [0, 2, 3, 9, 6]

    distances, parent = dijkstra_with_parent(weighted, 0)
    assert distances == [0, 2, 3, 9, 6]
    assert reconstruct_path(parent, 0, 4) == [0, 1, 2, 4]

    # Bellman-Ford.
    edges = [
        (0, 1, 4),
        (0, 2, 5),
        (1, 2, -2),
        (2, 3, 3),
        (1, 3, 4),
    ]

    distances, negative_cycle = bellman_ford(
        4,
        edges,
        0
    )

    assert distances == [0, 4, 2, 5]
    assert not negative_cycle

    # Floyd-Warshall.
    matrix = floyd_warshall(
        4,
        edges,
        directed=True
    )

    assert matrix[0][3] == 5
    assert not has_negative_cycle_floyd_warshall(matrix)

    # DSU.
    dsu = DSU(5)

    assert dsu.union(0, 1)
    assert dsu.union(1, 2)
    assert dsu.connected(0, 2)
    assert not dsu.connected(0, 3)

    # Kruskal.
    mst_edges = [
        (0, 1, 10),
        (0, 2, 6),
        (0, 3, 5),
        (1, 3, 15),
        (2, 3, 4),
    ]

    total, selected = kruskal_mst(4, mst_edges)
    assert total == 19
    assert len(selected) == 3

    # Prim.
    prim_graph = Graph(4)

    prim_graph.add_weighted_edge(0, 1, 10)
    prim_graph.add_weighted_edge(0, 2, 6)
    prim_graph.add_weighted_edge(0, 3, 5)
    prim_graph.add_weighted_edge(1, 3, 15)
    prim_graph.add_weighted_edge(2, 3, 4)

    total, selected = prim_mst(prim_graph)
    assert total == 19
    assert len(selected) == 3

    # Grid.
    grid = [
        ["1", "1", "0", "0"],
        ["1", "0", "0", "1"],
        ["0", "0", "1", "1"],
        ["0", "0", "0", "0"],
    ]

    assert count_islands(grid) == 3

    image = [
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
    ]

    assert flood_fill(image, 1, 1, 2) == [
        [2, 2, 2],
        [2, 2, 0],
        [2, 0, 1],
    ]

    binary_grid = [
        [0, 0, 1],
        [1, 0, 0],
        [1, 1, 0],
    ]

    assert shortest_path_binary_grid(binary_grid) == 5

    oranges = [
        [2, 1, 1],
        [1, 1, 0],
        [0, 1, 1],
    ]

    assert rotten_oranges(oranges) == 4

    # 0-1 BFS.
    zero_one = Graph(4)

    zero_one.add_weighted_edge(0, 1, 0)
    zero_one.add_weighted_edge(1, 2, 1)
    zero_one.add_weighted_edge(0, 3, 1)
    zero_one.add_weighted_edge(3, 2, 0)

    assert zero_one_bfs(zero_one, 0) == [0, 0, 1, 1]

    # SCC.
    scc_graph = Graph(5, directed=True)

    scc_graph.add_edge(0, 1)
    scc_graph.add_edge(1, 2)
    scc_graph.add_edge(2, 0)
    scc_graph.add_edge(2, 3)
    scc_graph.add_edge(3, 4)
    scc_graph.add_edge(4, 3)

    kosaraju = strongly_connected_components_kosaraju(
        scc_graph
    )

    tarjan = strongly_connected_components_tarjan(
        scc_graph
    )

    assert sorted(map(sorted, kosaraju)) == [
        [0, 1, 2],
        [3, 4]
    ]

    assert sorted(map(sorted, tarjan)) == [
        [0, 1, 2],
        [3, 4]
    ]

    # Bridges.
    bridge_graph = Graph(5)
    bridge_graph.add_edge(0, 1)
    bridge_graph.add_edge(1, 2)
    bridge_graph.add_edge(2, 0)
    bridge_graph.add_edge(1, 3)
    bridge_graph.add_edge(3, 4)

    bridges = find_bridges(bridge_graph)

    assert {tuple(sorted(edge)) for edge in bridges} == {
        (1, 3),
        (3, 4)
    }

    # Provinces.
    provinces = [
        [1, 1, 0],
        [1, 1, 0],
        [0, 0, 1],
    ]

    assert number_of_provinces(provinces) == 2

    # Word ladder.
    assert word_ladder_length(
        "hit",
        "cog",
        ["hot", "dot", "dog", "lot", "log", "cog"]
    ) == 5

    print("All Graph revision tests passed! ✓")


if __name__ == "__main__":
    print("=" * 72)
    print("GRAPHS — COMPLETE DSA REVISION")
    print("=" * 72)
    print("Representations                 ✓")
    print("BFS / DFS                       ✓")
    print("Connected Components            ✓")
    print("Cycle Detection                 ✓")
    print("Bipartite Graph                 ✓")
    print("Topological Sort                ✓")
    print("Dijkstra                        ✓")
    print("Bellman-Ford                    ✓")
    print("Floyd-Warshall                  ✓")
    print("DSU / Union-Find                ✓")
    print("Kruskal / Prim                  ✓")
    print("Grid BFS / DFS                  ✓")
    print("Multi-source BFS                ✓")
    print("0-1 BFS                         ✓")
    print("SCC — Kosaraju / Tarjan         ✓")
    print("Bridges / Articulation Points   ✓")
    print("Graph Cloning                   ✓")
    print("Word Ladder                     ✓")
    print("Interview Cheat Sheet           ✓")
    print()
    print("Run run_revision_tests() to verify all implementations.")
    print("=" * 72)
