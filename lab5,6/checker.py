from dimacs import *
import os
from time import time


def checkBFS(f):
    def checkLexBFS(G, vs):  # funkcja do sprawdzania poprawności lexBFS z konspektu
        n = len(G)
        pi = [None] * n

        for i, v in enumerate(vs):
            pi[v] = i

        for i in range(n - 1):
            for j in range(i + 1, n - 1):
                Ni = G[vs[i]].out
                Nj = G[vs[j]].out

                verts = [pi[v] for v in Nj - Ni if pi[v] < i]
                if verts:
                    viable = [pi[v] for v in Ni - Nj]
                    if not viable or min(verts) <= min(viable):
                        return False
        return True

    dirs = os.listdir("")

    passed = failed = 0

    i = 0
    a = time()

    for folder in dirs:
        dir = os.listdir("" + folder)

        for graph in dir:
            print(graph)
            V, E = loadWeightedGraph("" + folder + '/' + graph)
            G, vs = f(V, E)
            if checkLexBFS(G, vs):
                print("Test " + str(i) + ": Passed")
                passed += 1
            else:
                print("Test " + str(i) + ": WRONG answer")
                failed += 1
            i += 1

    print("Time: " + str(time() - a) + " s")
    print("Passed: " + str(passed))
    print("Failed: " + str(failed))


def chordal_checker(f):
    passed = failed = 0

    dir = os.listdir("chordal")

    i = 0
    a = time()

    for graph in dir:
        print(graph)
        V, E = loadWeightedGraph("chordal/" + graph)
        sol = readSolution("chordal/" + graph)
        res = f(V, E)
        if int(res) == int(sol):
            print("Test " + str(i) + ": Passed")
            passed += 1
        else:
            print("Test " + str(i) + ": WRONG answer")
            failed += 1
        i += 1

    print("Time: " + str(time() - a) + " s")
    print("Passed: " + str(passed))
    print("Failed: " + str(failed))


def maxclique_checker(f):
    passed = failed = 0

    dir = os.listdir("maxclique")

    i = 0
    a = time()

    for graph in dir:
        print(graph)
        V, E = loadWeightedGraph("maxclique/" + graph)
        sol = readSolution("maxclique/" + graph)
        res = f(V, E)
        if int(res) == int(sol):
            print("Test " + str(i) + ": Passed")
            passed += 1
        else:
            print("Test " + str(i) + ": WRONG answer")
            failed += 1
        i += 1

    print("Time: " + str(time() - a) + " s")
    print("Passed: " + str(passed))
    print("Failed: " + str(failed))


def color_checker(f):
    passed = failed = 0

    dir = os.listdir("coloring")

    i = 0
    a = time()

    for graph in dir:
        print(graph)
        V, E = loadWeightedGraph("coloring/" + graph)
        sol = readSolution("coloring/" + graph)
        res = f(V, E)
        if int(res) == int(sol):
            print("Test " + str(i) + ": Passed")
            passed += 1
        else:
            print("Test " + str(i) + ": WRONG answer")
            failed += 1
        i += 1

    print("Time: " + str(time() - a) + " s")
    print("Passed: " + str(passed))
    print("Failed: " + str(failed))


def min_vcover_checker(f):
    passed = failed = 0

    dir = os.listdir("vcover")

    i = 0
    a = time()

    for graph in dir:
        print(graph)
        V, E = loadWeightedGraph("vcover/" + graph)
        sol = readSolution("vcover/" + graph)
        res = f(V, E)
        if int(res) == int(sol):
            print("Test " + str(i) + ": Passed")
            passed += 1
        else:
            print("Test " + str(i) + ": WRONG answer")
            failed += 1
        i += 1

    print("Time: " + str(time() - a) + " s")
    print("Passed: " + str(passed))
    print("Failed: " + str(failed))