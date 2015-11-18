matrix = {
	'A': {'B': 5, 'C': 4, 'D': 7, 'E': 6, 'F': 8},
	'B': {'A': 5, 'C': 7, 'D': 10, 'E': 9, 'F': 11},
	'C': {'A': 4, 'B': 7, 'D': 7, 'E': 6, 'F': 8},
	'D': {'A': 7, 'B': 10, 'C': 7, 'E': 5, 'F': 9},
	'E': {'A': 6, 'B': 9, 'C': 6, 'D': 5, 'F': 8},
	'F': {'A': 8, 'B': 11, 'C': 8, 'D': 9, 'E': 8},
}

# matrix = {
# 	'K': {'L': 16, 'M': 16, 'N': 10},
# 	'L': {'K': 16, 'M': 8, 'N': 8},
# 	'M': {'K': 26, 'L': 8, 'N': 4},
# 	'N': {'K': 10, 'L': 8, 'M': 4},
# }

sum_dists = {key: sum(matrix[key].values()) for key in matrix}

def get_sum_dist(key):
	return sum_dists[key] / (2 * (len(matrix) - 2))


def get_min_keys():
	min_dist = 100000000
	min_keys = ()
	for key1 in matrix:
		for key2 in matrix[key1]:
			cur_dist = matrix[key1][key2] - get_sum_dist(key1) - get_sum_dist(key2)
			if min_dist > cur_dist:
				min_keys = key2, key1
				min_dist = cur_dist

	return min_dist, min_keys


def get_nj_dist_row(keys):
	key1, key2 = keys
	row = {}
	for key in matrix:
		if key == key1 or key == key2:
			continue

		row[key] = 0.5 * (matrix[key1][key] + matrix[key2][key] - matrix[key1][key2])

	return row


def delete_keys(keys):
	key1, key2 = keys
	del matrix[key1]
	del matrix[key2]
	del sum_dists[key1]
	del sum_dists[key2]

	for key in matrix:
		sum_dists[key] -= matrix[key][key1] + matrix[key][key2]
		del matrix[key][key1]
		del matrix[key][key2]


def insert_row(ins_key, row):
	for key in matrix:
		matrix[key][ins_key] = row[key]

	matrix[ins_key] = row
	sum_dists[ins_key] = sum(row.values())


def nj():
	while len(matrix) > 3:
		dist, min_keys = get_min_keys()
		row = get_nj_dist_row(min_keys)
		dist1 = 0.5 * (matrix[min_keys[0]][min_keys[1]] + get_sum_dist(min_keys[0]) - get_sum_dist(min_keys[1]))
		dist2 = 0.5 * (matrix[min_keys[0]][min_keys[1]] + get_sum_dist(min_keys[1]) - get_sum_dist(min_keys[0]))
		delete_keys(min_keys)
		ins_key = '(%s:%f, %s:%f)' % (min_keys[0], dist1, min_keys[1], dist2)
		insert_row(ins_key, row)


if __name__ == '__main__':
	nj()
	#print(list(matrix)[0])
	keys = list(matrix.keys())
	res = '(%s:%d, %s:%d, %s:%d)' % (keys[0], 0, keys[1], matrix[keys[1]][keys[0]], keys[2], matrix[keys[2]][keys[0]])
	print(res)