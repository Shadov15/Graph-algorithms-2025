from pathlib import Path
import networkx as nx
import time

from dimacs import readSolution, loadWeightedGraph

def reindex(E):
    for i, (u, v, w) in enumerate(E):
        E[i] = (u-1, v-1, w)


def find_flow(path):
    n, E = loadWeightedGraph(path)
    reindex(E)

    G = nx.DiGraph()
    for u, v, w in E:
        G.add_edge(u, v, capacity=w)

    return nx.maximum_flow_value(G, 0, n-1)


### ========================================== ###

def solve(path):
    return find_flow(path)


def main():
    i = passed = 0
    total_start = time.time()
    for file in Path("flow").iterdir():
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
