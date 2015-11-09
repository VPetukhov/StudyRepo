import math

# begin = {'+': 0.5, '-': 0.5}

# transitions = {
# 	'+': {'+': 0.5, '-': 0.5},
# 	'-': {'+': 0.5, '-': 0.5},
# }

# emission = {
# 	'+': {'0': 0.5, '1': 0.5},
# 	'-': {'0': 0.9, '1': 0.1}
# }

begin = {'M': 1.0, 'I': 0.0, 'D': 0.0}

transitions = {
	'M': {'M': [0.81, 0.54, 0.80, 0.81], 'I': [0.09, 0.27, 0.20, 0.19], 'D': [0.10, 0.19, 0.10, 0.00]},
	'I': {'M': [0.33, 0.60, 0.33, 0.50], 'I': [0.33, 0.20, 0.34, 0.50], 'D': [0.34, 0.20, 0.33, 0.00]},
	'D': {'M': [0.00, 0.50, 0.50, 0.50], 'I': [0.00, 0.00, 0.25, 0.50], 'D': [0.00, 0.50, 0.25, 0.00]},
}

emission = {
	'M': {'A': [0.00, 0.25, 0.54, 0.08], 'C': [0.00, 0.58, 0.18, 0.50], 'G': [0.00, 0.08, 0.09, 0.33], 'T': [0.00, 0.08, 0.18, 0.08]},
	'I': {'A': [0.25, 0.15, 0.25, 0.25], 'C': [0.25, 0.50, 0.25, 0.25], 'G': [0.25, 0.17, 0.25, 0.25], 'T': [0.25, 0.17, 0.25, 0.25]},
	'D': {'A': [0.00, 0.50, 0.50, 0.50], 'C': [0.00, 0.00, 0.25, 0.50], 'G': [0.00, 0.50, 0.25, 0.00], 'T': [0.00, 0.50, 0.25, 0.00]},
}


class Cell:
	def __init__(self, probability, prev_state):
		assert isinstance(prev_state, str)
		assert isinstance(probability, (float, int))
		self.probability = probability
		self.prev_state = prev_state

def get_max_probability(seq):
	assert isinstance(seq, str)

	matrix = build_matrix(seq, True)
	return max(matrix[len(seq)])

	# print(sorted(matrix[0].keys()))
	# for row in matrix:
	# 	print([row[c].probability for c in sorted(row.keys())])

	current_key = max(transitions.keys(), key=lambda key: matrix[-1][key].probability)
	res = '' + current_key
	for row in matrix[-2::-1]:
		res = current_key + res
		current_key = row[current_key].prev_state

	return res


def get_states_sequence(seq):
	assert isinstance(seq, str)

	matrix = build_matrix(seq)

	print(sorted(matrix[0].keys()))
	for row in matrix:
		print([row[c].probability for c in sorted(row.keys())])

	current_key = max(transitions.keys(), key=lambda key: matrix[-1][key].probability)
	res = '' + current_key
	for row in matrix[-2::-1]:
		res = current_key + res
		current_key = row[current_key].prev_state

	return res


def get_best_state(row, cur_state, number):
	return max(transitions.keys(), key=lambda prev_state: row[prev_state][cur_state][number].probability + math.log(transitions[prev_state][cur_state][number]))


def build_matrix(seq):
	assert isinstance(seq, str)

	matrix = [{state: Cell(0, '-') for state in transitions.keys()} for _ in seq]
	for state in begin.keys():
		matrix[0][state] = Cell(math.log(emission[state][seq[0]]), 'b')

	for i in range(1, len(seq)):
		for number in range(4):
			for cur_state in transitions.keys():
				best_state = get_best_state(matrix[i-1], cur_state, number)
				matrix[i][number][cur_state] = Cell(matrix[i - 1][number][best_state].probability + math.log(transitions[best_state][cur_state][number]) +
													0 if cur_state == 'D' else math.log(emission[cur_state][seq[i]]), best_state)

	return matrix


# def build_matrix(seq, is_forward = False):
# 	assert isinstance(seq, str)
# 	accumulate_func = sum if is_forward else max
#
# 	matrix = [{state: Cell(0, '-') for state in transitions.keys()} for _ in seq]
# 	for state in begin.keys():
# 		matrix[0][state] = Cell(math.log(emission[state][seq[0]]), 'b')
#
# 	for i in range(1, len(seq)):
# 		for cur_state in transitions.keys():
# 			best_state = accumulate_func(transitions.keys(), key=lambda prev_state: matrix[i - 1][prev_state].probability + math.log(get_prob(prev_state, cur_state)))
# 			matrix[i][cur_state] = Cell(matrix[i - 1][best_state].probability + math.log(get_prob(best_state, cur_state)) + math.log(emission[cur_state][seq[i]]), best_state)
#
# 	return matrix

#AAAGAATTCA
#AAATCA
#
if __name__ == '__main__':
	string = input()
	# string = '00110111'
	# print(get_max_probability(string))
	print(get_states_sequence(string))