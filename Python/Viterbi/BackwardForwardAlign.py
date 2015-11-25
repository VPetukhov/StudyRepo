
# BLOSUM62 = {'A': {'A': 4, 'C': 0, 'G': 0, 'T': 0},
#             'C': {'A': 0, 'C': 9, 'G': -3, 'T': -1},
#             'G': {'A': 0, 'C': -3, 'G': 6, 'T': 2},
#             'T': {'A': 0, 'C': -1, 'G': -2, 'T': 5}
#             }

gap_probs = {'A': 0.25, 'C': 0.25, 'G': 0.25, 'T': 0.25}

emission = {'A': {'A': 0.34, 'C': 0.21, 'G': 0.21, 'T': 0.21},
            'C': {'A': 0.21, 'C': 0.55, 'G': 0.08, 'T': 0.16},
            'G': {'A': 0.21, 'C': 0.08, 'G': 0.59, 'T': 0.12},
            'T': {'A': 0.21, 'C': 0.16, 'G': 0.12, 'T': 0.51}
            }


p_gap_open = 0.10
p_gap_continue = 0.15
p_end = 0.1
p_gap_match = 1 - p_gap_continue - p_end
p_match_match = 1 - 2 * p_gap_open - p_end

transitions = {'I': {'I': p_gap_continue, 'D': 0, 'M': p_gap_match},
               'D': {'I': 0, 'D': p_gap_continue, 'M': p_gap_match},
               'M': {'I': p_gap_open, 'D': p_gap_open, 'M': p_match_match},
               }


def print_max_probability(seq1, seq2):
    assert isinstance(seq1, str)
    assert isinstance(seq2, str)

    forward_matrix = build_forward_matrix(seq1, seq2)
    backward_matrix = build_backward_matrix(seq1, seq2)
    normalizer = sum([forward_matrix[-2][-2][key] for key in transitions.keys()]) * p_end

    result_matrix = [
        [forward_matrix[row][col]['M'] * backward_matrix[row][col]['M'] / normalizer for col in range(1, len(seq2) + 1)]
        for row in range(1, len(seq1) + 1)]

    print(normalizer)
    print()
    for row in backward_matrix:
        print([c for c in row])

    print()
    for row in forward_matrix:
        print([c for c in row])

    print()
    for row in result_matrix:
        print(row)
        # print(reduce(lambda base, x: base + ' ' + x, [str(p) for p in forward_matrix['+']][1:], '+'))
        # print(reduce(lambda base, x: base + ' ' + x, [str(p) for p in forward_matrix['-']][1:], '-'))


def build_forward_matrix(seq1, seq2):
    assert isinstance(seq1, str)
    assert isinstance(seq2, str)

    matrix = [[{state: 0 for state in transitions.keys()} for _ in range(len(seq2) + 2)] for _ in range(len(seq1) + 2)]
    matrix[0][0] = {'M': 1, 'I': 0, 'D': 0}

    # index "-1" is normal
    for row in range(len(seq1) + 1):
        for col in range(len(seq2) + 1):
            if row == 0 and col == 0:
                continue

            match_prob = sum(matrix[row - 1][col - 1][prev_state] * transitions[prev_state]['M'] for prev_state in
                             transitions.keys())
            ins_prob = sum(matrix[row - 1][col][prev_state] * transitions[prev_state]['I'] for prev_state in
                           transitions.keys())
            del_prob = sum(matrix[row][col - 1][prev_state] * transitions[prev_state]['D'] for prev_state in
                           transitions.keys())

            matrix[row][col]['M'] = match_prob * emission[seq1[row - 1]][seq2[col - 1]]
            matrix[row][col]['I'] = ins_prob * gap_probs[seq1[row - 1]]
            matrix[row][col]['D'] = del_prob * gap_probs[seq2[col - 1]]

    return matrix


def build_backward_matrix(seq1, seq2):
    assert isinstance(seq1, str)
    assert isinstance(seq2, str)

    matrix = [[{state: 0 for state in transitions.keys()} for _ in range(len(seq2) + 2)] for _ in range(len(seq1) + 2)]
    matrix[len(seq1)][len(seq2)] = {'M': p_end, 'I': p_end, 'D': p_end}

    # index "len(seq) + 2" is normal
    for row in range(len(seq1), 0, -1):
        for col in range(len(seq2), 0, -1):
            if row == len(seq1) and col == len(seq2):
                continue

            m_prob = matrix[row + 1][col + 1]['M'] * transitions['M']['M'] * emission[seq1[row - 1]][seq2[col - 1]] + \
                     matrix[row + 1][col]['I'] * transitions['M']['I'] * gap_probs[seq1[row - 1]] + \
                     matrix[row][col + 1]['D'] * transitions['M']['D'] * gap_probs[seq2[col - 1]]

            i_prob = matrix[row + 1][col + 1]['M'] * transitions['I']['M'] * emission[seq1[row - 1]][seq2[col - 1]] + \
                     matrix[row + 1][col]['I'] * transitions['I']['I'] * gap_probs[seq1[row - 1]]

            d_prob = matrix[row + 1][col + 1]['M'] * transitions['D']['M'] * emission[seq1[row - 1]][seq2[col - 1]] + \
                     matrix[row][col + 1]['D'] * transitions['D']['D'] * gap_probs[seq2[col - 1]]

            matrix[row][col]['M'] = m_prob
            matrix[row][col]['I'] = i_prob
            matrix[row][col]['D'] = d_prob

    return matrix


# AAAGAATTCA
# AAATCA
#
if __name__ == '__main__':
    # string = input()
    # print(get_max_probability(string))
    print_max_probability('ACGTAGC', 'ACGTTTAGC')
