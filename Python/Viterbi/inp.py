begin = {'+': 0.5, '-': 0.5}

transitions = {
	'+': {'+': 0.5, '-': 0.5},
	'-': {'+': 0.5, '-': 0.5},
}

generation = {
	'+': {'0': 1, '1': 0},
	'-': {'0': 0, '1': 1}
	# '+': {'0': 0.99, '1': 0.01},
	# '-': {'0': 0.01, '1': 0.99}
}


class Cell:
	def __init__(self, probability, prev_state):
		assert isinstance(prev_state, str)
		assert isinstance(probability, (float, int))
		self.probability = probability
		self.prev_state = prev_state


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


def build_matrix(seq):
	assert isinstance(seq, str)

	matrix = [{state: Cell(0, '-') for state in transitions.keys()} for _ in seq]
	for state in begin.keys():
		matrix[0][state] = Cell(generation[state][seq[0]], 'b')

	for i in range(1, len(seq)):
		for cur_state in transitions.keys():
			test = [matrix[i - 1][prev_state].probability * transitions[prev_state][cur_state] for prev_state in transitions.keys()]
			best_state = max(transitions.keys(), key=lambda prev_state: matrix[i - 1][prev_state].probability * transitions[prev_state][cur_state])
			matrix[i][cur_state] = Cell(matrix[i - 1][best_state].probability * transitions[best_state][cur_state] * generation[best_state][seq[i]], best_state)

	return matrix

#TODO logarithms
if __name__ == '__main__':
	# str = input()
	string = '000111'
	print(get_states_sequence(string))