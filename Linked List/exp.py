import numpy as np
import heapq


class SimpleHNSW:
    def __init__(self, M=3):
        self.M = M                  # max neighbors per node
        self.vectors = []
        self.graph = []

    def distance(self, a, b):
        # Euclidean distance
        return np.linalg.norm(a - b)

    def add(self, vector):
        vector = np.asarray(vector, dtype=float)

        node = len(self.vectors)

        self.vectors.append(vector)
        self.graph.append([])

        # First node
        if node == 0:
            return

        # Find distances to existing nodes
        distances = []

        for i, existing in enumerate(self.vectors[:-1]):
            d = self.distance(vector, existing)
            distances.append((d, i))

        # Connect to M closest nodes
        distances.sort()

        neighbors = distances[:self.M]

        for _, neighbor in neighbors:
            self.graph[node].append(neighbor)
            self.graph[neighbor].append(node)

    def search(self, query, k=3):
        query = np.asarray(query, dtype=float)

        entry = 0

        visited = {entry}

        # (distance, node)
        candidates = [
            (self.distance(query, self.vectors[entry]), entry)
        ]

        results = []

        while candidates:

            distance, node = heapq.heappop(candidates)

            results.append((distance, node))

            for neighbor in self.graph[node]:

                if neighbor in visited:
                    continue

                visited.add(neighbor)

                d = self.distance(
                    query,
                    self.vectors[neighbor]
                )

                heapq.heappush(
                    candidates,
                    (d, neighbor)
                )

        # Return k closest
        results.sort()

        return results[:k]