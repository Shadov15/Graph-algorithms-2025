import time
from pathlib import Path
from dimacs import readSolution, loadWeightedGraph
from lexBFS import lexBFS, Node, gen_nodes_list

def reindex(E):
    for i, (u, v, w) in enumerate(E):
        E[i] = (u-1, v-1, w)


def chromatic_number(path):  # zwraca rozmiar największej kliki
    V, E = loadWeightedGraph(path)
    reindex(E)
    G = gen_nodes_list(V, E)
    order = lexBFS(G, V)

    color = [0] * V
    for u in order:
        used = {color[v] for v in G[u].out}
        u_color = 1
        while u_color in used:
            u_color += 1
        color[u] = u_color

    return max(color)

### ========================================== ###

def solve(path):
    return chromatic_number(path)

def main():
    i = passed = 0
    total_start = time.time()
    for file in Path("coloring").iterdir():
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
