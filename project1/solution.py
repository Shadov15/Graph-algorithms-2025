import math
from collections import deque

from data import runtests

SIEVE_RANGE = 10000000
primes = [True] * SIEVE_RANGE


def create_sieve():
    global primes
    primes[0] = primes[1] = False
    for i in range(2, int(math.isqrt(SIEVE_RANGE)) + 1):
        if not primes[i]:
            continue
        primes[i] = True
        for j in range(i * i, SIEVE_RANGE, i):
            primes[j] = False
    primes = [idx for idx, p in enumerate(primes) if p]


create_sieve()


def get_divisors(n):
    global primes
    divs = []
    for p in primes:
        if p * p > n:
            break
        if n % p == 0:
            power = 0
            while n % p == 0:
                n //= p
                power += 1
                divs.append((p, power))

    if n > 1:
        p = primes[-1] + 2
        if p % 2 == 0: p += 1
        while p * p <= n:
            if n % p == 0:
                power = 0
                while n % p == 0:
                    n //= p
                    power += 1
                    divs.append((p, power))
            p += 2
    if n > 1:
        divs.append((n, 1))

    return divs


class Graph:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.level = []  # te tablice inicjalizują się dopiero w funkcjach: bfs, dfs, max_flow
        self.ptr = []
        self.num_map = {}

    def add_node(self):
        self.graph.append([])
        self.n += 1

    def add_weighted_edge(self, u, v, weight):
        self.graph[u].append([v, weight, len(self.graph[v])])
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def bfs(self, s, t, ):
        self.level = [-1] * self.n
        self.level[s] = 0
        queue = deque([s])

        while queue:
            u = queue.popleft()
            if u == t:
                return True
            for v, cap, _ in self.graph[u]:
                if cap > 0 and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)

        return self.level[t] != -1

    def dfs(self, u, t, pushed):
        if pushed == 0 or u == t:
            return pushed
        # używamy ptr, by kontynuować od ostatniej badanej krawędzi
        while self.ptr[u] < len(self.graph[u]):
            v, cap, rev = self.graph[u][self.ptr[u]]
            if cap > 0 and self.level[v] == self.level[u] + 1:
                found_flow = self.dfs(v, t, min(pushed, cap))
                if found_flow > 0:
                    # aktualizuj krawędzie (w przód i w tył)
                    self.graph[u][self.ptr[u]][1] -= found_flow
                    self.graph[v][rev][1] += found_flow
                    return found_flow
            self.ptr[u] += 1
        return 0

    def max_flow(self, s, t):
        while self.bfs(s, t):
            self.ptr = [0] * self.n
            while True:
                pushed = self.dfs(s, t, float('inf'))
                if pushed == 0:
                    break


def create_graph(scores):
    SCALE = 10 ** 6  # skalujemy float do inta dla szybszych obliczeń

    s = 0  # Źródło
    t = 1  # Ujście

    dinic = Graph(2)

    for div, luck in scores:
        # tworzymy wierzchołek dla każdego dzielnika i dodajemy krawędź od źródła o wadze luck
        parent_idx = dinic.n
        dinic.add_node()
        dinic.num_map[div] = parent_idx
        dinic.add_weighted_edge(s, parent_idx, int(luck * SCALE))

        prime_divs = get_divisors(div)

        for base, power in prime_divs:
            node = (base, power)
            if node not in dinic.num_map:  # sprawdzam, czy widzieliśmy takiego node
                # jeśli nie to tworzymy dla niego wierzchołek oraz dodajemy krawędzie od parenta
                idx = dinic.n
                dinic.add_node()
                dinic.num_map[node] = idx
                # krawędzie od dzielników do ujścia mają koszt równy 5log10(base)
                cost = int(5 * math.log10(base) * SCALE)
                dinic.add_weighted_edge(idx, t, cost)

                # jeśli znaleziona liczba pierwsza miała większą potęgę niż 1 to tworzymy jej łańcuch
                if power > 1:
                    prev_node = (base, power - 1)
                    # musi istnieć, bo idziemy od 1 w górę
                    prev_idx = dinic.num_map[prev_node]
                    # krawędź nieskończoności wymuszająca zależność
                    dinic.add_weighted_edge(idx, prev_idx, float('inf'))

            # krawędzie od parenta do dzielników są "darmowe"
            p_idx = dinic.num_map[node]
            dinic.add_weighted_edge(parent_idx, p_idx, float('inf'))

    return dinic, s, t


def solve(scores):
    dinic, s, t = create_graph(scores)
    dinic.max_flow(s, t)

    # bfs, żeby znaleźć użyte krawędzie, te liczby bierzemy
    visited = [False] * dinic.n
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v, cap, _ in dinic.graph[u]:
            if cap > 0 and not visited[v]:
                visited[v] = True
                queue.append(v)

    answer = 1
    for node_tuple, idx in dinic.num_map.items():
        if isinstance(node_tuple, tuple):
            if visited[idx]:
                answer *= node_tuple[0]

    return answer


runtests(solve)
