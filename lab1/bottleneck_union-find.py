# sortujemy listę krawędzi i dodajemy od tych z największą wagą, następnie sprawdzamy union-find
# czy istnieje połączenie s -> t
import time

from dimacs import loadWeightedGraph, readSolution
from pathlib import Path

def find(x, parent):
    if parent[x] != x:
        parent[x] = find(parent[x], parent)
    return parent[x]

def union(x, y, parent, rank):
    x_root = find(x, parent)
    y_root = find(y, parent)

    if x_root == y_root:
        return False

    if rank[x_root] < rank[y_root]:
        parent[x_root] = y_root
    elif rank[x_root] > rank[y_root]:
        parent[y_root] = x_root
    else:
        parent[y_root] = x_root
        rank[x_root] += 1

    return True

def reindex_graph(G):
    for i in range(len(G)):
        u, v, w = G[i]
        u -= 1
        v -= 1
        G[i] = (u, v, w)

def solve(path):
    n, E = loadWeightedGraph(path)
    reindex_graph(E)
    E.sort(key = lambda e: e[2], reverse = True)
    rank = [0]*n
    parent = [i for i in range(n)]

    for u, v, w in E:
        union(u, v, parent, rank)
        if find(0, parent) == find(1, parent):
            return str(w)

    return -1

def main():
    i = 0; passed = 0
    for file in Path("graphs-lab1").iterdir():
        print("Test: " + str(i) + ", " + file.name)
        start = time.time()
        flag = False
        if solve(str(file)) == readSolution(str(file)):
            passed += 1
            flag = True
        print("\t" + "Passed\t" if flag else "Failed\t" + str(time.time() - start))
        i += 1
    print("Passed: " + str(passed))
    print("Failed: " + str(i - passed))


if __name__ == '__main__':
    main()



