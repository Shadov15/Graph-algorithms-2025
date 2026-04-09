from pathlib import Path

from testy import *


def read_problem(name):
    path = Path("problems") / name

    prices = []
    friends = []

    with Path(path).open() as f:
        solution = int(f.readline().strip())
        size = int(f.readline().strip())

        for _ in range(size):
            line = f.readline().strip()
            prices.append(int(line))

        while line := f.readline().strip():
            u, v = map(int, line.split())
            friends.append((u, v))

    return {"arg": [friends, prices], "hint": solution}


files = [
    "simple-1",
    "simple-2",
    "simple-3",
    "simple-4",
    "simple-5",
    "simple-6",
    "simple-7",
    "simple-8",
    "simple-9",
    "clique-5",
    "clique-10",
    "clique-20",
    "clique-50",
    "clique-100",
    "clique-300",
    "clique-1000",
    "tree-10",
    "tree-20",
    "tree-30",
    "tree-50",
    "tree-100",
    "tree-500",
    "tree-2000",
    "tree-10000",
    "tree-50000",
    "tree-200000",
    *[f"random-{i}" for i in range(1, 39)]
]

problems = {name: read_problem(f"{name}") for name in files}


def printarg(friends, prices):
    print(f"{len(prices)} osób, {len(friends)} przyjaźni")


def printhint(hint):
    print("Wynik: {}".format(hint))


def printsol(sol):
    print("Uzyskany wynik: {}".format(sol))


def check(friends, prices, hint, sol):
    if hint == sol:
        print("Test zaliczony")
        return True
    else:
        print("NIEZALICZONY!")
        return False


def runtests(f):
    internal_runtests(printarg, printhint, printsol, check, problems, f)
