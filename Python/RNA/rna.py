complementary = {
    'A': {'A': 0, 'U': 1, 'G': 0, 'C': 0},
    'U': {'A': 1, 'U': 0, 'G': 0, 'C': 0},
    'G': {'A': 0, 'U': 0, 'G': 0, 'C': 1},
    'C': {'A': 0, 'U': 0, 'G': 1, 'C': 0},
}


def get_backward(scores, seq):
    stack = [(0, len(scores) - 1)]
    base_pairs = []

    while len(stack) != 0:
        row, col = stack.pop()
        if row >= col:
            continue

        if scores[row + 1][col] == scores[row][col]:
            stack.append((row + 1, col))
        elif scores[row][col - 1] == scores[row][col]:
            stack.append((row, col - 1))
        elif scores[row + 1][col - 1] + complementary[seq[row]][seq[col]] == scores[row][col]:
            base_pairs.append((row, col))
            stack.append((row + 1, col - 1))
        else:
            for k in range(row + 1, col):
                if scores[row][k] + scores[k + 1][col] == scores[row][col]:
                    stack.append((k + 1, col))
                    stack.append((row, k))
                    break

    return base_pairs


def get_print_form(seq, base_pairs):
    out = ['.'] * len(seq)
    for pair in base_pairs:
        out[pair[0]] = '('
        out[pair[1]] = ')'

    return out


def get_rna(seq):
    scores = [[0] * len(seq) for _ in seq]
    scores[0][0] = 0
    for i in range(1, len(seq)):
        scores[i][i - 1] = 0
        scores[i][i] = 0

    for delta in range(1, len(seq)):
        for ind in range(len(seq) - delta):
            scores[ind][ind + delta] = max(
                scores[ind + 1][ind + delta],
                scores[ind][ind + delta - 1],
                scores[ind + 1][ind + delta - 1] + complementary[seq[ind]][seq[ind + delta]],
                0 if delta < 3 else max(
                    [scores[ind][k] + scores[k + 1][ind + delta] for k in range(ind + 1, ind + delta - 1)])
            )

    for row in scores:
        print(row)

    print()
    base_pairs = get_backward(scores, seq)
    print(base_pairs)
    return ''.join(get_print_form(seq, base_pairs))


def main():
    # res = get_rna('UACGGACCGUCGCGGUCCGU')
    # res = get_rna('GGGAAAUCC')
    res = get_rna('CGCUUCAUAUAAUCCUAAUGAUAUGGUUUGGGAGUUUCUACCAAGAGCCUUAAACUCUUGAUUAUGAAGUG')
    print(res)


if __name__ == '__main__':
    main()
