def read_file_lines(fname: str):
    """
    Read file including empty lines
    :param fname: file name
    :return: lines from the file
    """
    try:
        file = open(fname, "r")
        lines = file.readlines()
        file.close()
    except:
        return []

    return lines


def write_file_lines(fname: str, lines):
    """
    Write given lines to the file
    :param fname: file name
    :param lines: list  of lines to write
    """
    try:
        file = open(fname, "w")
        for line in lines:
            file.write(line)
        file.close()
    except Exception:
        return


def rem_first(line, key):
    pos = line.find(" ")
    if pos < 0 or line[:pos] != key:
        return line, False

    return line[pos+1:], True


def get_set(lines, k):
    res, key, ll = '', 'entropy', len(lines)
    line = lines[k]
    line, _ = rem_first(line, key)
    found = False
    while not found:
        res += line[:-1] + ' '
        k += 1
        if k >= ll: break
        line, found = rem_first(lines[k], key)

    return res, k


def read_data(read_entropy=True):
    """
    Reads data from driver-input.txt and
        returns functional, expected, and entropy sets
    driver-input.txt format
        Line 0: 2 integers; numTests and inputLength
        line 1: expected array; numTests integers
        line 2..k: functional test set; numTests x inputLength integers
        line k till end of file: entropy set
    @param read_entropy: (Boolean) Whether to read entropy data or not
    @return: a tuple
      inputLength (int): # of inputs for each test
      numTests (int): number of functional tests.
                      For each test, test subject is provided inputLength inputs
      functional (string): is the functional input
      expected (int[]): is the expected value array
      entropy (string): is the entropy input
    """
    lines = read_file_lines("driver-input.txt")

    l0 = lines[0].split()
    inputLength = int(l0[1])
    numTests = int(l0[0])
    expected = lines[1].split()
    expected = expected[:-1]
    functional, k = get_set(lines, 2)
    entropy = []
    if read_entropy:
        entropy, k = get_set(lines, k)

    return inputLength, numTests, functional, expected, entropy


def invalidResult(n: int, invalid: int) -> str:
    """
    This function prepares invalid result string
    @param n: (int) the number of values
    @param invalid: (int) invalid value
    @return: (str) returns a string composed of n invalid values
    """
    res = ""
    for _ in range(n):
        res += f"{invalid} "

    return res
