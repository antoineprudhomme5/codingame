import string

alphabet = string.ascii_uppercase

def col_from_row(n):
    letter = alphabet[(n-1) % 26]
    next_n = (n-1) // 26
    if next_n > 0:
        return col_from_row(next_n) + letter
    else:
        return letter

n = int(input())
transformed = []

for label in input().split():
    # row to column
    if label.isdigit():
        transformed.append(col_from_row(int(label)))
    # column to row
    else:
        len_label = len(label)
        row = 0
        for i in range(len_label):
            row += (alphabet.index(label[i]) + 1) * (26**(len_label - i - 1))
        transformed.append(str(row))

print(' '.join(transformed))
