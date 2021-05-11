from itertools import combinations


def g(sys, idx):
    return sys[idx % 18] if isinstance(idx, int) else [g(sys, i) for i in idx]


def s(sys, idx, val):
    return [val if i in [j % 18 for j in idx] else g(sys, i) for i in range(18)]


def C(sys):
    num = 0
    nxt = order[order.index(C) + 1]
    idx = [i for i in (2, 3, 5, 7, 11, 13, 17) if not g(sys, i)]
    for i, j in combinations(idx, 2):
        num += nxt(s(sys, (i, j), 'C'))
    return num


def A(sys):
    num = 0
    nxt = order[order.index(A) + 1]
    idx = [i for i in range(18) if not g(sys, i) and not g(sys, i + 1)]
    for i, j in combinations(idx, 2):
        num += 0 if j - \
            i in (1, 17) else nxt(s(sys, (i, i + 1, j, j + 1), 'A'))
    return num


def D(sys):
    num = 0
    nxt = order[order.index(D) + 1]
    idx = [i for i in range(18) if not g(sys, i) and not g(
        sys, i + 5) and 'X' not in g(sys, range(i - 1, i + 7))]
    for i in idx:
        jdx = [j for j in range(i + 1, i + 5) if not g(sys, j)]
        for j, k in combinations(jdx, 2):
            num += nxt(s(sys, (i, j, k, i + 5), 'D'))
    return num


def G(sys):
    num = 0
    nxt = order[order.index(G) + 1]
    idx = [i for i in range(18) if not g(sys, i) and (
        'E' not in sys or 'E' in g(sys, (i - 1, i + 1)))]
    for i, j in combinations(idx, 2):
        num += nxt(s(sys, (i, j), 'G'))
    return num


def E(sys):
    num = 0
    nxt = order[order.index(E) + 1]
    idx = [i for i in range(18) if not g(sys, i)]
    for i, j, k, l, m in combinations(idx, 5):
        if 'G' in sys and g(sys, {(z - 1) % 18 for z in (i, j, k, l, m)} | {(z + 1) % 18 for z in (i, j, k, l, m)}).count('G') < 2:
            continue
        num += nxt(s(sys, (i, j, k, l, m), 'E'))
    return num


def X(sys):
    num = 0
    nxt = order[order.index(X) + 1]
    idx = [i for i in range(18) if not g(
        sys, i) and 'D' not in g(sys, (i - 1, i + 1))]
    for i in idx:
        num += nxt(s(sys, [i], 'X'))
    return num


def end(sys):
    return 1


order = (C, A, D, G, E, X, end)


def count():
    return order[0]([None] * 18)
