from functools import reduce

transitions = {
	'b': {'+': 0.5, '-': 0.5, 'b': 0},
	'+': {'+': 0.8, '-': 0.2, 'b': 0},
	'-': {'+': 0.3, '-': 0.7, 'b': 0},
}

emission = {
	'b': {'0': 0, '1': 0},
	'+': {'0': 0.5, '1': 0.5},
	'-': {'0': 0.9, '1': 0.1}
}

# transitions = {
# 	'b': {'+': 0.5, '-': 0.5, 'b': 0},
# 	'+': {'+': 0.7, '-': 0.3, 'b': 0},
# 	'-': {'+': 0.3, '-': 0.7, 'b': 0},
# }
#
# emission = {
# 	'b': {'0': 0, '1': 0},
# 	'+': {'0': 0.9, '1': 0.1},
# 	'-': {'0': 0.2, '1': 0.8}
# }


def print_max_probability(seq):
	assert isinstance(seq, str)

	forward_matrix = build_forward_matrix(seq)
	backward_matrix = build_backward_matrix(seq)

	normalizer = sum([forward_matrix[key][-1] * transitions['b'][key] for key in transitions.keys()])

	for key in forward_matrix.keys():
		for i in range(len(forward_matrix[key])):
			forward_matrix[key][i] *= backward_matrix[key][i] / normalizer

	print(reduce(lambda base, x: base + ' ' + x, [str(p) for p in forward_matrix['+']][1:], '+'))
	print(reduce(lambda base, x: base + ' ' + x, [str(p) for p in forward_matrix['-']][1:], '-'))


def build_forward_matrix(seq):
	assert isinstance(seq, str)

	matrix = {state: [0] * (len(seq) + 1) for state in transitions.keys()}
	matrix['b'][0] = 1

	for i in range(1, len(seq) + 1):
		for cur_state in transitions.keys():
			sum_probability= sum(matrix[prev_state][i - 1] * transitions[prev_state][cur_state] for prev_state in transitions.keys())
			matrix[cur_state][i] = sum_probability * emission[cur_state][seq[i - 1]]

	return matrix


def build_backward_matrix(seq):
	assert isinstance(seq, str)

	matrix = {state: [0] * (len(seq) + 1) for state in transitions.keys()}
	for key in transitions.keys():
		matrix[key][-1] = transitions['b'][key]

	for i in range(len(seq) - 1, 0, -1):
		for cur_state in transitions.keys():
			matrix[cur_state][i] = sum(matrix[end_state][i + 1] * transitions[cur_state][end_state] * emission[end_state][seq[i]]
									   for end_state in transitions.keys())

	return matrix


#AAAGAATTCA
#AAATCA
#
if __name__ == '__main__':
	# string = input()
	# string = '00100'
	string = '010001'
	# print(get_max_probability(string))
	print_max_probability(string)