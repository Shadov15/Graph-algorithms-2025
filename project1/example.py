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


def add_weighted_edge(graph, u, v, weight):
    # graph[u] to lista krawędzi wychodzących z u
    # Krawędź: [v, capacity, rev_index]
    graph[u].append([v, weight, len(graph[v])])
    graph[v].append([u, 0, len(graph[u]) - 1])


def bfs(graph, level, s, t):
    # Reset leveli (-1 oznacza nieodwiedzony)
    for i in range(len(graph)):
        level[i] = -1
    level[s] = 0
    queue = deque([s])

    while queue:
        u = queue.popleft()
        if u == t:
            return True
        for v, cap, _ in graph[u]:
            # Warunek z Twojego kodu: cap > 0 (dla floatów warto dać > 1e-9, ale trzymam się wzorca)
            # W Twoim kodzie było `cap > 0` w BFS i `cap > 0` w DFS, ale w solve `1e-9`.
            # Dla bezpieczeństwa przy floatach daję tu 1e-9, żeby BFS nie chodził po "zerowych" krawędziach.
            if cap > 1e-9 and level[v] == -1:
                level[v] = level[u] + 1
                queue.append(v)

    return level[t] != -1


def dfs(graph, ptr, level, u, t, pushed):
    if pushed == 0 or u == t:
        return pushed

    # Pętla wykorzystująca ptr[u] do pamiętania ostatniej krawędzi
    while ptr[u] < len(graph[u]):
        v, cap, rev = graph[u][ptr[u]]

        if cap > 1e-9 and level[v] == level[u] + 1:
            found_flow = dfs(graph, ptr, level, v, t, min(pushed, cap))
            if found_flow > 0:
                # Aktualizacja przepływów
                graph[u][ptr[u]][1] -= found_flow
                graph[v][rev][1] += found_flow
                return found_flow

        ptr[u] += 1
    return 0


def dinic_max_flow(graph, s, t):
    n = len(graph)
    level = [-1] * n

    while bfs(graph, level, s, t):
        ptr = [0] * n
        while True:
            pushed = dfs(graph, ptr, level, s, t, float('inf'))
            if pushed == 0:
                break



def create_graph(scores):
    s = 0
    t = 1

    graph = [[], []]
    node_labels = [None, None]  # Odpowiednik mapowania odwrotnego (idx -> label)

    # Mapa: (base, power) -> index wierzchołka
    num_map = {}

    for div, luck in scores:
        # 1. Węzeł dla liczby (Parent)
        parent_idx = len(graph)
        graph.append([])  # add_node
        node_labels.append(None)

        num_map[div] = parent_idx  # To w sumie nadpisuje, jeśli liczby się powtarzają, ale w Dinicu to OK
        add_weighted_edge(graph, s, parent_idx, luck)

        prime_divs = get_divisors(div)

        for base, power in prime_divs:
            node = (base, power)

            if node not in num_map:
                # 2. Węzeł dla potęgi liczby pierwszej
                idx = len(graph)
                graph.append([])  # add_node
                node_labels.append(node)
                num_map[node] = idx

                # Krawędź do ujścia (Koszt)
                cost = 5 * math.log10(base)
                add_weighted_edge(graph, idx, t, cost)

                if power > 1:
                    prev_node = (base, power - 1)
                    if prev_node in num_map:
                        prev_idx = num_map[prev_node]
                        add_weighted_edge(graph, idx, prev_idx, float('inf'))

            p_idx = num_map[node]
            add_weighted_edge(graph, parent_idx, p_idx, float('inf'))

    return graph, node_labels, s, t


def solve(scores):
    graph, node_labels, s, t = create_graph(scores)
    dinic_max_flow(graph, s, t)

    # BFS po grafie rezydualnym (Rekonstrukcja wyniku)
    visited = [False] * len(graph)
    queue = deque([s])
    visited[s] = True

    while queue:
        u = queue.popleft()
        for v, cap, _ in graph[u]:
            if cap > 1e-9 and not visited[v]:
                visited[v] = True
                queue.append(v)

    answer = 1
    for idx, label in enumerate(node_labels):
        if label is not None and visited[idx]:
            answer *= label[0]

    return answer


runtests(solve)