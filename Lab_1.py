import logging

logging.basicConfig(level=logging.INFO)

def main():
	c = [[1/5, 0, 0.2, 0, 0], [0, 0.2, 0, 0.2, 0], [0.2, 0, 0.2, 0, 0.2], [0, 0.2, 0, 0.2, 0], [0, 0, 0.2, 0, 0.2]]
	k=12

	for row in c:
		for index, elem in enumerate(row):
			print(elem, k, round(elem*k, 1))
			row[index]=round(elem*k, 1)

	logging.info(c)
	logging.info(c[0][2])

if __name__ == "__main__":
	main()
