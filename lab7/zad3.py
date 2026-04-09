from pathlib import Path
import networkx as nx
import time

from dimacs import readSolution, loadCNFFormula

def read_fulfilling_valuation(G, SCC):
    pass

def find_flow(path):
    n, F = loadCNFFormula(path)

    G = nx.DiGraph()
    # budowa grafu implikacji, x or y -> -x => y oraz -y => x
    for a, b in F:
        G.add_edge(-a, b)
        G.add_edge(-b, a)

    SCC = nx.strongly_connected_components(G)
    for v in G.nodes():
        for S in SCC:
            # jeśli wierzchołek i jego zaprzeczenie jest w tej samej SCC to formuła jest niespełnialna
            if v in S and -v in S:
                return False

    return True


### ========================================== ###

def solve(path):
    return find_flow(path)


def main():
    i = passed = 0
    total_start = time.time()
    for file in Path("sat").iterdir():
        print("Test: " + str(i) + ", " + file.name)
        start = time.time()
        flag = False
        result = int(solve(str(file)))
        solution = int(readSolution(str(file))[-1])
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
