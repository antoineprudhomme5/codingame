from math import floor

n, price = map(int, (input(), input()))
budgets = sorted(int(input()) for _ in range(n))

if sum(budgets) < price:
    # if not enought money, print impossible
    print("IMPOSSIBLE")
else:
    for i in range(n):
        d = min(price // (n-i), budgets[i])
        price -= d
        print(d)
