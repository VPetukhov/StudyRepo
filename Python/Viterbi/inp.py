penalty = -1
alignment_price = 1
skip_penalty = -1

base_prices = {
	'A': {'A': alignment_price, 'T': penalty, 'G': penalty, 'C': penalty},
	'T': {'A': penalty, 'T': alignment_price, 'G': penalty, 'C': penalty},
	'G': {'A': penalty, 'T': penalty, 'G': alignment_price, 'C': penalty},
	'C': {'A': penalty, 'T': penalty, 'G': penalty, 'C': alignment_price},
}

complex_prices = {
	'A': {'A': 1, 'T': -1, 'G': -1, 'C': -1},
	'T': {'A': -2, 'T': 1, 'G': -1, 'C': -1},
	'G': {'A': -1, 'T': -1, 'G': 1, 'C': -1},
	'C': {'A': -1, 'T': -1, 'G': -1, 'C': 1},
}


class Cell:
	__skip_penalty__ = {
		False: skip_penalty,
		True: -1,
	}

	def __init__(self, value, dir='', level=0):
		self.value = value
		self.dir = dir
		self.level = level

	def with_vert_skip(self):
		return Cell(self.value + Cell.__skip_penalty__[self.level == 1], 'U', 1)

	def with_hor_skip(self):
		return Cell(self.value + Cell.__skip_penalty__[self.level == -1], 'L', -1)

	def without_skip(self, price):
		return Cell(self.value + price, 'D', 0)


# Как выводить выравнивание?
def get_local_alignment(seq1, seq2, prices):
	assert isinstance(seq1, str)
	assert isinstance(seq2, str)

	matrix = build_matrix(prices, seq1, seq2, True)

	for row in matrix:
		print([c.value for c in row])

	max_row, max_col = 0, 0
	for row in range(len(seq2)):
		for col in range(len(seq1)):
			if matrix[row][col].value > matrix[max_row][max_col].value:
				max_row, max_col = row, col

	# if (max_row == len(seq2) - 1 and max_col == len(seq1) - 1):
	# 	max_col += 1
	# 	max_row += 1

	res1 = ''
	res2 = ''
	row, col = max_row, max_col
	while row > 0 and col > 0 and matrix[row][col].value >= 0:
		if matrix[row][col].dir == 'U':
			res1 = '-' + res1
			res2 = seq2[row - 1] + res2
			row -= 1
		elif matrix[row][col].dir == 'L':
			res1 = seq1[col - 1] + res1
			res2 = '-' + res2
			col -= 1
		else:
			res1 = seq1[col - 1] + res1
			res2 = seq2[row - 1] + res2
			col -= 1
			row -= 1

	return res1, res2


def get_global_alignment(seq1, seq2, prices):
	assert isinstance(seq1, str)
	assert isinstance(seq2, str)

	matrix = build_matrix(prices, seq1, seq2, False)

	for row in matrix:
		print([c.value for c in row])
	res1 = ''
	res2 = ''
	row, col = len(seq2), len(seq1)
	while row > 0 and col > 0:
		if matrix[row][col].dir == 'U':
			res1 = '-' + res1
			res2 = seq2[row - 1] + res2
			row -= 1
		elif matrix[row][col].dir == 'L':
			res1 = seq1[col - 1] + res1
			res2 = '-' + res2
			col -= 1
		else:
			res1 = seq1[col - 1] + res1
			res2 = seq2[row - 1] + res2
			col -= 1
			row -= 1

	while col > 0:
		res1 = seq1[col - 1] + res1
		res2 = '-' + res2
		col -= 1

	while row > 0:
		res1 = '-' + res1
		res2 = seq2[row - 1] + res2
		row -= 1

	return res1, res2


def build_matrix(prices, seq1, seq2, is_local):
	assert isinstance(seq1, str)
	assert isinstance(seq2, str)
	assert isinstance(is_local, bool)

	matrix = [[Cell(0) for _ in range(len(seq1) + 1)] for _ in range(len(seq2) + 1)]
	matrix[0] = [Cell(skip_penalty * x) for x in range(len(seq1) + 1)]
	for y in range(len(seq2) + 1):
		matrix[y][0].value = y * skip_penalty
	for row in range(1, len(seq2) + 1):
		for col in range(1, len(seq1) + 1):
			cell = max(matrix[row - 1][col].with_vert_skip(),
						matrix[row][col - 1].with_hor_skip(),
						matrix[row - 1][col - 1].without_skip(prices[seq1[col - 1]][seq2[row - 1]]),
						key=lambda x: x.value)

			if is_local and cell.value < 0:
				cell.value = 0

			matrix[row][col] = cell

	return matrix


if __name__ == '__main__':
	str1 = input()
	str2 = input()
	# res1, res2 = get_global_alignment(str1, str2, base_prices)
	res1, res2 = get_local_alignment(str1, str2, complex_prices)
	#res1, res2 = get_global_alignment('ACTGATTGCT', 'ATATG', complex_prices)
	print(res1)
	print(res2)

# AAATTTGCCGC
# AAACCCTGCGG

# AAATTGC
# AA-T--C