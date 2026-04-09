import time
from pathlib import Path
from dimacs import readSolution, loadWeightedGraph
from lexBFS import lexBFS, Node, gen_nodes_list

def reindex(E):
    for i, (u, v, w) in enumerate(E):
        E[i] = (u-1, v-1, w)


def maxclique(path):  # zwraca rozmiar największej kliki
    n, E = loadWeightedGraph(path)
    reindex(E)
    G = gen_nodes_list(n, E)
    order = lexBFS(G, n)
    og_idx_to_order = [None] * (n)
    for i in range(n):
        og_idx_to_order[order[i]] = i

    RN_plus_v = [set() for _ in range(n)]
    max_len = 0

    for i in range(1, n):  # nie ma sensu sprawdzać pierwszego elementu order, bo wszystko puste
        v = order[i]
        for u in G[v].out:
            u_idx = og_idx_to_order[u]
            if u_idx < i:
                RN_plus_v[v].add(u)

        RN_plus_v[v].add(v)
        k = len(RN_plus_v[v])
        if k > max_len:
            max_len = k

    return max_len


### ========================================== ###

def solve(path):
    return maxclique(path)

def main():
    i = passed = 0
    total_start = time.time()
    for file in Path("maxclique").iterdir():
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
    print(' ============================== ')
    print("Passed: " + str(passed) + " / " + str(i))
    print(f"Total time: {time.time() - total_start:.4f} s")

if __name__ == '__main__':
    main()
