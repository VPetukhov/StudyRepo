import matplotlib.pyplot as plt

if __name__ == "__main__":
	futures = []
	dates = []
	with open('usd.txt') as file:
		futures = [float(s.split()[-1])/1000 for s in file]

	with open('usd.txt') as file:
		dates = [s.split()[2] for s in file]

	spot = []
	with open('rub.txt') as file:
		spot = [float(s.split()[-1]) for s in file]

	# print([x - y for x, y in (usd, rub)])
	diff = list(map(lambda x, y: x - y, spot, futures))
	plt.plot(diff)
	plt.grid()
	plt.show()
	# input();