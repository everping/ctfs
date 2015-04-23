__author__ = 'Ping'


def load_data():
    """
    Load input data from file
    :return: ciphertext and public key
    """
    f1 = open('pubkey.txt', 'r')
    f2 = open('ciphertext.txt', 'r')
    pub_keys = f1.read().strip()[1:-1].split(', ')
    ciphertext = int(long(f2.read().strip()))
    f1.close()
    f2.close()
    return pub_keys, ciphertext


def create_matrix_from_knapsack(ciphertext, pub_keys):
    """
    Create the matrix from input data of the form http://goo.gl/aOQE7J
    """
    last_col = []
    for p in pub_keys:
        last_col.append(int(long(p)))

    last_col.append(ciphertext)
    last_row = [1 for i in pub_keys]

    # I use sagemath to do this
    my_matrix = MatrixSpace(ZZ, len(pub_keys))(2)
    m_last_row = matrix(ZZ, 1, len(last_row), last_row)
    m_last_col = matrix(ZZ, len(last_col), 1, last_col)

    my_matrix = my_matrix.stack(m_last_row)
    my_matrix = my_matrix.augment(m_last_col)

    return my_matrix


def is_short_vector(vector):
    """
    Is short vector?
    :return: True/False
    """
    for v in vector:
        if v != 1 and v != -1 and v != 0:
            return False
    return True


def find_short_vector(matrix):
    """
    Find short vector from matrix was applied LLL algorithms
    """
    for row in matrix:
        if is_short_vector(row):
            return row


def main():
    pub_keys, cipher = load_data()
    my_matrix = create_matrix_from_knapsack(cipher, pub_keys)

    # Apply LLL algorithm to matrix
    new_matrix = my_matrix.LLL()

    # Get short vector
    short_vector = find_short_vector(new_matrix)

    # Change 1 to 0 and -1 to 1 to get solution vector
    solution_vector = []
    for v in short_vector:
        if v == 1:
            solution_vector.append(0)
        elif v == -1:
            solution_vector.append(1)

    # and we get flag
    flag = hex(int(''.join([str(i) for i in solution_vector])[::-1], 2))[2:-1].decode('hex')

    print flag


if __name__ == '__main__':
    main()









