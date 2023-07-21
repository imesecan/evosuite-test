import argparse


def save_file(file_name, expected, functional):
    """
    Save expected and functional tests arrays to the file 'file_name'
    @param string file_name: file name
    @param string[] expected: expected values array
    @param string[] functional: functional tests array
    @rtype: void
    """
    num_tests = len(expected)
    num_inputs = len(functional[0].split())
    try:
        f = open(file_name, "w")
        f.write(f"{num_tests} {num_inputs} \t# number of functional tests, number of inputs per test\n")
        for val in expected:
            f.write(f"{val} ")
        f.write("expected\n")

        for test in functional:
            f.write(f"{test} ")
        f.write("\nentropy ")
        f.close()
    except IOError:
        print("Couldn't save results to the file.")


def read_file(file_name):
    """
    Read given file and return string[]
    :param string file_name: file name
    :rtype: string[]
    """
    f = open(file_name, "r")
    lines = [line for line in f if line.strip("\n")]
    f.close()

    return lines


def get_values(line, remove_txt):
    for rem in remove_txt:
        line = line.replace(rem, "")

    return line


def main():
    parser = argparse.ArgumentParser(description='Collect Functional Tests')
    parser.add_argument('--trg_prj', type=str, default="01-Aliasing-ControlFlow-insecure", help='Target project folder name')
    parser.add_argument('--trg_cls', type=str, default="Main", help='Target class name')
    parser.add_argument('--trg_function', type=str, default="process", help='Target function name')
    parser.add_argument('--jobid', type=int, default=0, help='A unique identifier to define current run')
    args = parser.parse_args()

    trg_prj = args.trg_prj
    trg_cls = args.trg_cls
    trg_function = args.trg_function
    jobid = args.jobid

    print(f"Target Project: {trg_prj}, Target class: {trg_cls}, Target function: {trg_function}, jobid: {jobid}")

    package = "org/leakreducer"
    assert_txt = "assertEquals("
    latxt = len(assert_txt)
    remove_txt = ["(", ")", ";", ","]

    trg_call = f" {trg_cls}.{trg_function}("
    lcall = len(trg_call)
    # sample evosuite-tests/Classify-112/org/leakreducer/Classify_ESTest.java
    target = f"evosuite-tests/{trg_prj}-{jobid}/{package}/{trg_cls}_ESTest.java"
    lines = read_file(target)
    functional = []
    expected = []
    for line in lines:
        pos = line.find(trg_call)
        if pos > 0:
            functional.append(get_values(line[pos + lcall:-1], remove_txt))
        pos = line.find("assertEquals(")
        if pos > 0:
            pos2 = line.find(", ", pos)
            expected.append(get_values(line[pos+latxt: pos2], remove_txt))
    file_name = f"evosuite-tests/{trg_cls}-{jobid}-driver-input.txt"
    save_file(file_name, expected, functional)


if __name__ == "__main__":
    main()
