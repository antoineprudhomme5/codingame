from math import floor

n, price = map(int, (input(), input()))
budgets = sorted(int(input()) for _ in range(n))

# if not enought money, print impossible
if sum(budgets) < price:
    print("IMPOSSIBLE")
else:
    contributions = [0]*n

    i = 0
    while i < n:
        d = price / (n-i)
        if d > budgets[i]:
            contributions[i] = budgets[i]
            price -= contributions[i]
            i += 1
        elif floor(d) != d:
            contributions[i] = floor(d)
            price -= contributions[i]
            i += 1
        else:
            d = int(d)
            while i < n:
                contributions[i] = d
                i += 1

    for contribution in contributions:
        print(contribution)
