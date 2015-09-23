from functools import reduce
from six.moves import xrange
from matplotlib import pyplot as plt
from scipy import stats
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Alphabet import generic_dna
from Bio.Alphabet import IUPAC

test_seq = 'AGCTCGCTCGCTGCGTATAAAATCGCATCGCGCGCAGC'
dna_seq='ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTG'
protein_seq = 'IRTNGTHMQPLLKLMKFQKFLLELFTLQKRKPEKGYNLPIISLNQ'


def test_bio():
	my_dna = Seq(test_seq, generic_dna)
	print(my_dna.complement())
	print(my_dna.reverse_complement())
	print(my_dna.transcribe())


def test_match_dna_profile():
	profile = {
		'A': [61, 16, 352, 3, 354, 268, 360, 222, 155, 56, 83, 82, 82, 68, 77],
		'C': [145, 46, 0, 10, 0, 0, 3, 2, 44, 135, 147, 127, 118, 107, 101],
		'G': [152, 18, 2, 2, 5, 0, 10, 44, 157, 150, 128, 128, 128, 139, 140],
		'T': [31, 309, 35, 374, 30, 121, 6, 121, 33, 48, 31, 52, 61, 75, 71]}

	score, position = match_dna_profile(test_seq, profile)
	print(score, position, test_seq[position:position + len(profile['A'])])


def test_gc_content():
	gcResults = calc_gc_content(test_seq)
	print(gcResults)
	plt.hist(gcResults)
	plt.show()


def test_entropy_search():
	dnaScores = relative_entropy_search(dna_seq, 6)
	proteinScores = relative_entropy_search(protein_seq, 10, True)
	plt.plot(dnaScores)
	plt.plot(proteinScores)
	plt.show()


def test_bio_input():
	with open("demoSequences.fasta", "rU") as file:
		for protein in SeqIO.parse(file, 'fasta'):
			print(protein.id)
			print(protein.seq)

	with open("output.fasta", "w") as file:
		protein_seq='MFADRWLFSTNHKDIGTLYLLFGAWAGVLGTALSLLIRAELGQPG'
		seq_obj = Seq(protein_seq, IUPAC.protein)
		protein_obj = SeqRecord(seq_obj, id="TEST")
		SeqIO.write([protein_obj,], file, 'fasta')


def match_dna_profile(seq, profile):
	best_score = 0
	best_position = None
	width = len(profile['A'])
	for i in xrange(len(seq) - width):
		score = sum([profile[seq[i + j]][j] for j in xrange(width)])

		if score > best_score:
			best_score = score
			best_position = i

	return best_score, best_position


def calc_gc_content(seq, win_size=10):
	return [
		len([x for x in seq[i:i + win_size] if x == 'C' or x == 'G']) / float(win_size)
		for i in xrange(len(seq) - win_size)]


def calc_relative_entropy(seq, res_codes):

	from math import log

	N = float(len(seq))
	base = 1.0 / len(res_codes)
	prop = {r: 0 for r in res_codes}
	for r in seq:
		prop[r] += 1

	for r in res_codes:
		prop[r] /= N

	return sum([prop[r]* log(prop[r]/base, 2.0) for r in res_codes if prop[r] != 0.0])


def relative_entropy_search(seq, win_size, is_protein=False):
	len_seq = len(seq)
	extra_seq = seq[:win_size]
	seq += extra_seq
	if is_protein:
		res_codes = 'ACDEFGHIKLMNPQRSTVWY'
	else:
		res_codes = 'GCAT'

	scores = [calc_relative_entropy(seq[i:i + win_size], res_codes) for i in xrange(len_seq)]
	return scores

if __name__ == '__main__':
	test_bio_input()
	pass
