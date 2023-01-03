"""
Sample Run
   python3 get_tests.py --trg_function calculate --trg_project 22-Package-Example --jobid 122
"""
from argparse import ArgumentParser


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


def save_file(file_name, lines):
    """
    Save string[] to the file (fname)
    :param string file_name: file name
    :param string[] lines: file in the form of lines
    :rtype: void
    """
    f = open(file_name, "w")
    for line in lines:
        f.write(line+"\n")
    f.close()


def main(args):
    trg_project = args.trg_project + "-" + args.jobid
    fname = trg_project + "/tests" + args.jobid + ".txt"
    lines = read_file(fname)
    res = []
    for line in lines:
        pos = line.find(args.trg_function)
        if pos>=0:
            pos1 = line.find("(", pos+1)
            pos2 = line.find(");", pos1+1)
            if (pos1+1) == pos2: continue
            res.append(line[pos1+1:pos2])

    save_file(trg_project + "/clean-tests"+args.jobid+".txt", res)


if __name__ == "__main__":
    parser = ArgumentParser(description='LeakReducer collect test cases')
    parser.add_argument('--trg_project', type=str)
    parser.add_argument('--trg_function', type=str, default='process')
    parser.add_argument('--jobid', type=str, default='111')

    arg_prs = parser.parse_args()
    main(arg_prs)
