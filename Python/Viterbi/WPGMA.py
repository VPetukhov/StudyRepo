import subprocess
import os
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

def get_min_keys(m):
	min_dist = 100000000
	min_keys = ()
	for key1 in m:
		for key2 in m[key1]:
			if min_dist > m[key1][key2]:
				min_keys = key2, key1
				min_dist = m[key1][key2]

	return min_dist, min_keys


def get_wpgma_dist_row(keys):
	key1, key2 = keys
	row = {}
	for key in matrix:
		if key == key1 or key == key2:
			continue

		row[key] = (matrix[key][key1] + matrix[key][key2]) / 2

	return row


def get_upgma_dist_row(keys):
	key1, key2 = keys
	row = {}
	for key in matrix:
		if key == key1 or key == key2:
			continue

		sheets_count_1 = key1.count(',') + 1
		sheets_count_2 = key2.count(',') + 1

		row[key] = (matrix[key][key1] * sheets_count_1 + matrix[key][key2] * sheets_count_2) / (sheets_count_1 + sheets_count_2)

	return row


def delete_keys(keys):
	key1, key2 = keys
	del matrix[key1]
	del matrix[key2]

	for key in matrix:
		del matrix[key][key1]
		del matrix[key][key2]


def insert_row(ins_key, row):
	for key in matrix:
		matrix[key][ins_key] = row[key]

	matrix[ins_key] = row


def wpgma():
	lens = {key: 0 for key in matrix}
	while len(matrix) > 1:
		dist, min_keys = get_min_keys(matrix)
		row = get_wpgma_dist_row(min_keys)
		delete_keys(min_keys)
		ins_key = '(%s:%f, %s:%f)' % (min_keys[0], dist / 2 - lens[min_keys[0]], min_keys[1], dist / 2 - lens[min_keys[1]])
		insert_row(ins_key, row)
		lens[ins_key] = dist / 2


def upgma():
	lens = {key: 0 for key in matrix}
	while len(matrix) > 1:
		dist, min_keys = get_min_keys(matrix)
		row = get_upgma_dist_row(min_keys)
		delete_keys(min_keys)
		ins_key = '(%s:%f, %s:%f)' % (min_keys[0], dist / 2 - lens[min_keys[0]], min_keys[1], dist / 2 - lens[min_keys[1]])
		insert_row(ins_key, row)
		lens[ins_key] = dist / 2


if __name__ == '__main__':
	upgma()
	print(list(matrix)[0])
	with open('out.pt', 'w') as out:
		out.write(list(matrix)[0])

	os.chdir('/home/victor/biosoft/FigTree_v1.4.2/')
	subprocess.call(['/home/victor/biosoft/FigTree_v1.4.2/bin/figtree', '/home/victor/StudyRepo/Python/Viterbi/out.pt'])