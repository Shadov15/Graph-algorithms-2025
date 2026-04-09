from dimacs import readSolution, loadDirectedWeightedGraph
from collections import deque, defaultdict
from pathlib import Path
import time


def reindex_graph(E):
    for i in range(len(E)):
        u, v, w = E[i]
        E[i] = (u-1, v-1, w)


def build_graph(E, n):
    residual_graph = [defaultdict(int) for _ in range(n)]
    for u, v, _ in E:
        residual_graph[u][v] = 1
        residual_graph[v][u] = 1
    return residual_graph


def BFS(residual_graph, s, t, parent):
    n = len(residual_graph)
    # Reset parentów i visited
    for i in range(n):
        parent[i] = None

    visited = [False] * n
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        if u == t:
            return True

        for v, capacity in residual_graph[u].items():
            if not visited[v] and capacity > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)
    return False


def edmonds_karp(path):
    n, E = loadDirectedWeightedGraph(path)
    reindex_graph(E)
    s = 0
    min_cut = float('inf')

    # Tablica parent alokowana raz, ale czyszczona w BFS
    parent = [None] * n

    for t in range(1, n):
        rg = build_graph(E, n)

        connection = 0

        while BFS(rg, s, t, parent):
            path_flow = float('inf')
            v = t
            while v != s:
                u = parent[v]
                path_flow = min(path_flow, rg[u][v])
                v = u

            connection += path_flow

            v = t
            while v != s:
                u = parent[v]
                rg[u][v] -= path_flow
                rg[v][u] += path_flow
                v = u

        min_cut = min(min_cut, connection)

    return min_cut

### ================================================== ###

def solve(path):
    return edmonds_karp(path)

def main():
    i = 0; passed = 0
    total_start = time.time()
    for file in Path("graphs-lab2/connectivity").iterdir():
        print("Test: " + str(i) + ", " + file.name)
        start = time.time()
        flag = False
        result = int(solve(str(file)))
        solution = int(readSolution(str(file)))
        if result == solution:
            passed += 1
            flag = True
        print("Passed\t" + str(time.time() - start) if flag else "Failed\t" + str(time.time() - start))
        i += 1
        print("\tResult: " + str(result))
        print("\tSolution: " + str(solution) + "\n")
    print("Passed: " + str(passed) + " / " + str(i))
    print(f"Total time: {time.time() - total_start:.4f} s")

if __name__ == '__main__':
    main()