from subprocess import call
from _collections_abc import Iterable

from six.moves import xrange
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import IUPAC
from Bio import SeqIO


def get_consensus(profile, probability_level):
	assert isinstance(probability_level, float)
	assert isinstance(profile, Iterable)

	res = ''
	for p in profile:
		val = max(p.items(), key = lambda x: x[1])
		res += val[0] if val[1] >= probability_level else 'X'

	return res


def get_profile(sequences):
	assert isinstance(sequences, list)

	max_len = max([len(s) for s in sequences])
	profile = []
	for i in xrange(max_len):
		dict = {}
		sum = 0.0
		for seq in sequences:
			if i >= len(seq):
				continue

			if seq[i] in dict:
				dict[seq[i]] += 1
			else:
				dict[seq[i]] = 1

			sum += 1.0

		profile.append({x[0]: x[1] / sum for x in dict.items()})

	return profile


def run_clustal(sequences, fasta_filename, align_filename):
	records = [SeqRecord(Seq(seq, IUPAC.protein), id='test%d' % i, description='my_desc')
				for i, seq in enumerate(sequences)]

	with open(fasta_filename, 'w') as file:
		SeqIO.write(records, file, 'fasta')

	cmdArgs = ['clustalw',
	'-INFILE=' + fasta_filename,
	'-OUTFILE=' + align_filename]
	call(cmdArgs)


if __name__ == '__main__':
	profile = get_profile(['SRPAPVVLIILCVMAGVIGTILLISYGIRLLIK',
						   'TVPAPVVIILIILCVMAGIIGTILLLIISYTIRRLIK',
							'HHFSEPEITLIIFGVMAGVIGTILLLIISYGIRLIK',
							'HFSELVIALIIFGVMAGVIGTILFISYGSRLIK'])
	print(profile)
	consensus = get_consensus(profile, 0.25)
	print(consensus)
	run_clustal(['SRPAPVVLIILCVMAGVIGTILLISYGIRLLIK',
				'TVPAPVVIILIILCVMAGIIGTILLLIISYTIRRLIK',
				'HHFSEPEITLIIFGVMAGVIGTILLLIISYGIRLIK',
				'HFSELVIALIIFGVMAGVIGTILFISYGSRLIK'],
				'myfasta.fasta',
				'res')