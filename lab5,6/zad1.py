import time
from pathlib import Path

from dimacs import readSolution, loadDirectedWeightedGraph
from lexBFS import lexBFS, Node, gen_nodes_list

def reindex(E):
    for i, (u, v, w) in enumerate(E):
        E[i] = (u-1, v-1, w)

def chordal_check(path):
    n, E = loadDirectedWeightedGraph(path)
    reindex(E)
    G = gen_nodes_list(n, E)
    order = lexBFS(G, n)
    og_idx_to_order = [None] * n
    for i in range(n):
        og_idx_to_order[order[i]] = i

    RN = [set() for _ in range(n)]
    parent = [None] * (n)

    for i in range(1, n):  # nie ma sensu sprawdzać pierwszego elementu order, bo wszystko puste
        v = order[i]
        last_idx = -1
        for u in G[v].out:
            u_idx = og_idx_to_order[u]
            if u_idx < i:
                RN[v].add(u)
                if u_idx > last_idx:
                    last_idx = u_idx

        parent[v] = order[last_idx] if last_idx != -1 else None

        if parent[v] is not None and not (RN[v] - {parent[v]} <= RN[parent[v]]):
            return False

    return True

### ========================================== ###

def solve(path):
    return chordal_check(path)

def main():
    i = passed = 0
    total_start = time.time()
    for file in Path("chordal").iterdir():
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
