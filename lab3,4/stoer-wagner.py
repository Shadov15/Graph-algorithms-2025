import heapq, time

from dimacs import readSolution, loadWeightedGraph
from pathlib import Path


def reindex_graph(E):
    for i in range(len(E)):
        u, v, w = E[i]
        E[i] = (u-1, v-1, w)

def build_graph_dict(E, n):
    G = [{} for _ in range(n)]
    for u, v, w in E:
        G[u][v] = w
        G[v][u] = w
    return G


def merge_vertices(G, s, t):
    for u, w in list(G[t].items()):
        if u == s:
            continue
        # wierzchołek wspólny pomiędzy s i t
        if u in G[s]:
            G[s][u] += w
            G[u][s] += w
        # sąsiad t, ale nie s
        else:  # (u not in G[s])
            G[s][u] = w
            G[u][s] = w

        G[u].pop(t, None)

    # czyścimy całkiem t
    G[s].pop(t, None)
    G[t] = None


def min_cut_phase(G):
    n = len(G)
    n_active = sum(1 for u in G if u is not None)

    A = []  # stos
    visited = [False] * n
    weight = [0] * n
    queue = []

    heapq.heappush(queue, (0, 0))

    while len(A) < n_active and queue:
        _, u = heapq.heappop(queue)
        if visited[u]:
            continue
        visited[u] = True
        A.append(u)

        for v, w in G[u].items():
            if not visited[v]:
                weight[v] += w
                heapq.heappush(queue, (-weight[v], v))

    s = A[-2]
    t = A[-1]

    merge_vertices(G, s, t)

    return weight[t]


def stoer_wagner(path):
    n, E = loadWeightedGraph(path)
    reindex_graph(E)
    G = build_graph_dict(E, n)
    best_cut = float('inf')
    for _ in range(n-1):
        current_cut = min_cut_phase(G)
        best_cut = min(current_cut, best_cut)

    return best_cut


### ===================================================== ###

def solve(path):
    return stoer_wagner(path)

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
        print("Passed\t" + str(time.time() - start) if flag else "Failed\t" + str(time.time() - start))
        i += 1
        print("\tResult: " + str(result))
        print("\tSolution: " + str(solution) + "\n")
    print("Passed: " + str(passed) + " / " + str(i))
    print(f"Total time: {time.time() - total_start:.4f} s")

if __name__ == '__main__':
    main()