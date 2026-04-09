# Wykonujemy algorytm Dijkstry zmieniając metrykę wartości wierzchołków na max z minimum wag krawędzi
# w ścieżce które dochodzą do wierzchołka. Do PriorityQueue dodajemy wartości ujemne, żeby najpierw wyciągać
# najcięższe krawędzie. Jako wartość wierzchołka ustawiamy min(wartość dotychczasowa ścieżki, nowa krawędź).

from dimacs import loadWeightedGraph, readSolution
from pathlib import Path
from queue import PriorityQueue
import time


def Dijkstra(G, s, t):
    n = len(G)
    val = [0] * n
    val[s] = float('inf')  # W źródle mamy nieskończony przepływ

    queue = PriorityQueue()
    queue.put((-float('inf'), s))

    while not queue.empty():
        w, u = queue.get()
        w = -w

        if u == t:
            return w

        if w < val[u]:
            continue

        for v, edge_weight in G[u]:
            new_limit = min(w, edge_weight)

            if new_limit > val[v]:
                val[v] = new_limit
                queue.put((-new_limit, v))

    return val[t]

def reindex_graph(G):
    for i in range(len(G)):
        u, v, w = G[i]
        u -= 1
        v -= 1
        G[i] = (u, v, w)

def convert_graph(G, n):
    graph = [[] for _ in range(n)]
    for i in range(len(G)):
        u, v, w = G[i]
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph

def solve(path):
    n, E = loadWeightedGraph(path)
    reindex_graph(E)
    G = convert_graph(E, n)
    return Dijkstra(G, 0, 1)


def main():
    i = 0; passed = 0
    for file in Path("graphs-lab1").iterdir():
        print("Test: " + str(i) + ", " + file.name)
        start = time.time()
        flag = False
        if int(solve(str(file))) == int(readSolution(str(file))):
            passed += 1
            flag = True
        print("\t" + "Passed\t" if flag else "Failed\t" + str(time.time() - start))
        i += 1
    print("Passed: " + str(passed))
    print("Failed: " + str(i - passed))


if __name__ == '__main__':
    main()