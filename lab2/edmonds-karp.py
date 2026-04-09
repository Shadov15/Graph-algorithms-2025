from dimacs import loadDirectedWeightedGraph, readSolution
from pathlib import Path
from collections import deque
import time

def reindex_graph(G):
    for i in range(len(G)):
        u, v, w = G[i]
        u -= 1
        v -= 1
        G[i] = (u, v, w)

def convert_graph(E, n):
    graph = [[] for _ in range(n)]
    residual_graph = [[0]*n for _ in range(n)]
    for i in range(len(E)):
        u, v, w = E[i]
        graph[u].append(v)
        graph[v].append(u)
        residual_graph[u][v] = w
    return graph, residual_graph


def BFS(G, residual_graph, s, t, parent):
    visited = [False] * len(G)
    queue = deque()
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.popleft()
        if u == t:
            return True
        for v in G[u]:
            if not visited[v] and residual_graph[u][v] > 0:
                visited[v] = True
                queue.append(v)
                parent[v] = u

    return False

def edmond_karps(path):
    n, E = loadDirectedWeightedGraph(path)
    reindex_graph(E)
    G, residual_graph = convert_graph(E, n)

    s, t = 0, n - 1
    max_flow = 0
    parent = [None] * n

    while BFS(G, residual_graph, s, t, parent):
        current_flow = float('inf')

        v = t
        while v != s:
            u = parent[v]
            current_flow = min(current_flow, residual_graph[u][v])
            v = u

        v = t
        while v != s:
            u = parent[v]
            residual_graph[u][v] -= current_flow  # Zmniejszamy w przód
            residual_graph[v][u] += current_flow  # Zwiększamy w tył
            v = u

        max_flow += current_flow
        parent = [None] * n

    return max_flow


### ========================================== ###

def solve(path):
    return edmond_karps(path)


def main():
    i = 0; passed = 0
    total_start = time.time()
    for file in Path("graphs-lab2/flow").iterdir():
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
        print(solution)
    print("Passed: " + str(passed))
    print("Failed: " + str(i - passed))
    print(f"Total time: {time.time() - total_start:.4f} s")

if __name__ == '__main__':
    main()