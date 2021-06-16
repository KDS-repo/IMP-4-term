import logging

logging.basicConfig(level=logging.INFO)


def main():
    c = [[], [], [], [], []]
    c[0] = [0.2, 0, 0.2, 0, 0]
    c[1] = [0, 0.2, 0, 0.2, 0]
    c[2] = [0.2, 0, 0.2, 0, 0.2]
    c[3] = [0, 0.2, 0, 0.2, 0]
    c[4] = [0, 0, 0.2, 0, 0.2]
    k = 12

    for row in c:
        for index, elem in enumerate(row):
            logging.info(str(elem) + " " + str(k) + " " + str(round(elem*k, 1)))
            row[index] = round(elem*k, 1)

    logging.info(c)
    logging.info(c[0][2])


if __name__ == "__main__":
    main()
