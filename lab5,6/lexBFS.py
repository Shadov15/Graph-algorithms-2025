from checker import checkBFS


class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()  # zbiór sąsiadów

    def connect_to(self, v):
        self.out.add(v)


def gen_nodes_list(V, L):
    G = [Node(i) for i in range(0, V)]  # żeby móc indeksować numerem wierzchołka

    for (u, v, _) in L:
        G[u].connect_to(v)
        G[v].connect_to(u)

    return G


# O(V^2)
def lexBFS(G, V):
    sets_list = [set(range(0, V))]
    ord = []

    while sets_list:
        s = sets_list[-1].pop()
        ord.append(s)
        # teraz trzeba dzielić zbiory na lewe - bez sąsiadów s oraz prawe - z sąsiadami s
        tmp_list = []
        for z in sets_list:
            if not z: continue
            r = z & G[s].out  # przecięcie zbiorów - sąsiedzi
            l = z - r  # różnica zbiorów - nie-sąsiedzi
            if l:
                tmp_list.append(l)
            if r:
                tmp_list.append(r)

        sets_list = tmp_list

    return ord


def main(V, L):
    G = gen_nodes_list(V, L)
    return G, lexBFS(G, V)


if __name__ == '__main__':
    checkBFS(main)