from dimacs import readSolution, loadDirectedWeightedGraph
from collections import deque
from pathlib import Path
import time, copy

def reindex_graph(G):
    for i in range(len(G)):
        u, v, w = G[i]
        G[i] = (u-1, v-1, w)

def convert_graph(E, n):
    graph = [[] for _ in range(n)]
    residual_graph = [[0]*n for _ in range(n)]
    for i in range(len(E)):
        u, v, _ = E[i]
        if residual_graph[u][v] == 0:
            graph[u].append(v)
            graph[v].append(u)
        residual_graph[u][v] = 1
        residual_graph[v][u] = 1
    return graph, residual_graph


def BFS(residual_graph, s, t, parent):
    n = len(residual_graph)
    visited = [False] * n
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        if u == t:
            return True
        for v in range(n):
            if not visited[v] and residual_graph[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)
    return False

def edmonds_karp(path):
    n, E = loadDirectedWeightedGraph(path)
    reindex_graph(E)
    G, residual_graph = convert_graph(E, n)

    s = 0
    min_cut = float('inf')
    parent = [None] * n

    for t in range(1, n):
        rg = copy.deepcopy(residual_graph)
        connection = 0

        while BFS(rg, s, t, parent):
            v = t
            while v != s:
                u = parent[v]
                rg[u][v] -= 1
                rg[v][u] += 1
                v = u

            connection += 1
            parent = [None] * n

        min_cut = min(min_cut, connection)

    return min_cut


### ========================================== ###

def solve(path):
    return edmonds_karp(path)


def main():
    i = 0; passed = 0
    total_start = time.time()
    for file in Path("graphs-lab3").iterdir():
        print("Test: " + str(i) + ", " + file.name)
        start = time.time()
        flag = False
        result = int(solve(str(file)))
        solution = int(readSolution(str(file)))
        if result == solution:
            passed += 1
            flag = True
        print("\t" + "Passed\t" + str(time.time() - start) if flag else "Failed\t" + str(time.time() - start))
        i += 1
        print(result)
        print(str(solution) + "\n")
    print("Passed: " + str(passed) + " / " + str(i))
    print(f"Total time: {time.time() - total_start:.4f} s")

if __name__ == '__main__':
    main()