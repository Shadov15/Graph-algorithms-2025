# sortujemy listę krawędzi, następnie wyszukiwaniem binarnym szukamy najlepszej wartości, dla której idąc po krawędziach
# o wadze większej lub równej tej wartości jesteśmy w stanie przejść z s do t. Takiego przejścia szukamy DFS

from dimacs import loadWeightedGraph, readSolution
from pathlib import Path
import sys, time

sys.setrecursionlimit(10**6)


def DFS(G, s, t, bound):
    visited = [False] * len(G)

    def DFS_Visit(s):
        visited[s] = True
        for u, w in G[s]:
            if not visited[u] and w >= bound:
                DFS_Visit(u)

    DFS_Visit(s)
    return visited[t]

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
    values_list = [w for _, _, w in E]
    values_list.sort()
    low, high = 0, len(values_list) - 1
    while low <= high:
        mid = (low + high) // 2
        bound = values_list[mid]
        if DFS(G, 0, 1, bound):
            low = mid + 1
        else:
            high = mid - 1

    return values_list[high]



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