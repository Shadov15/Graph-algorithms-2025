from data import runtests

def build_graph(friends, n):
    graph = [[] for _ in range(n)]

    for u, v in friends:
        graph[u-1].append(v-1)
        graph[v-1].append(u-1)

    return graph

def lexBFS(graph, n):
    buckets = [[] for _ in range(n)]
    bucket_pos = [0] * n
    current_weight = [0] * n

    for i in range(n):
        buckets[0].append(i)
        bucket_pos[i] = i

    processed = [False] * n
    peo = []
    max_weight = 0

    for _ in range(n):
        # znajdujemy niepusty kubełek o największej wadze
        while max_weight >= 0 and not buckets[max_weight]:
            max_weight -= 1

        u = buckets[max_weight].pop()
        processed[u] = True
        peo.append(u)

        # aktualizacja sąsiadów
        for v in graph[u]:
            if not processed[v]:
                old_w = current_weight[v]

                # znajdujemy pozycję v i ostatni element w tym kubełku
                idx_v = bucket_pos[v]
                last_element = buckets[old_w][-1]

                if v != last_element:
                    buckets[old_w][idx_v] = last_element
                    bucket_pos[last_element] = idx_v  # aktualizujemy wskaźnik przeniesionego elementu

                buckets[old_w].pop()

                new_w = old_w + 1
                current_weight[v] = new_w

                buckets[new_w].append(v)
                bucket_pos[v] = len(buckets[new_w]) - 1

                if new_w > max_weight:
                    max_weight = new_w

    return peo[::-1]


def solve(friends, prices):
    n = len(prices)
    graph = build_graph(friends, n)
    peo = lexBFS(graph, n)

    dp = [0] * n
    processed = [False] * n
    neighbor_sum = [0] * n  # accumulator sumy dp przetworzonych sąsiadów, aktualizowany inkrementalnie

    for u in peo:
        # zamiast sumować dynamicznie, odczytujemy już zebrany sumator
        s = neighbor_sum[u]
        val = prices[u] - s
        val = max(0, val)
        dp[u] = val
        processed[u] = True

        # propagujemy dp[u] do nieprzetworzonych sąsiadów (jedna aktualizacja na krawędź)
        to_add = dp[u]
        if to_add > 0:
            for v in graph[u]:
                if not processed[v]:
                    neighbor_sum[v] += to_add

    return sum(prices) - sum(dp)


runtests(solve)
