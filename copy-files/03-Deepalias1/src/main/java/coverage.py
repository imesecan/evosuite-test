import sys
import os
sys.path.append('../../../')

from util import read_file_lines, write_file_lines, read_data

# Modify the following inpu
package = "package org.leakreducer;"
target_path = "org/leakreducer/"
target_class = "Program"
target_function = "drive"
trg_return = "boolean"
prm_types = ['int']

# Common input
lines = ['x'] * 3
lines[0] = "\n    @org.junit.jupiter.api.Test\n"
lines[1] = package + "\nimport static org.junit.jupiter.api.Assertions.*;\n\n"
lines[2] = f"public class {target_class}Test " + "{\n"


def prepare_unit_test(tid: int, prs: list, exp_val: str):
    """
        Prepare a unit test given parameters and expected values
        :param tid: test id
        :param prs: list of parameters
        :param exp_val: expected value
        :return: list
    """
    ut_lines = ['']*5
    ut_lines[0] = lines[0]
    ut_lines[1] = "    void test"+str(tid)+"(){\n"
    ut_lines[2] = f"\t\t{trg_return} res = {target_class}.{target_function}("
    lp = len(prs)
    for i in range(lp):
        param = prs[i]
        prm_type = prm_types[i]
        ut_lines[2] += f"({prm_type}){param}"
        if i < lp - 1:
            ut_lines[2] += ", "

    ut_lines[2] += ");\n"
    ut_lines[3] = f"\t\tassertEquals(({trg_return}){exp_val}, res);\n"
    # ut_lines[3] = "        assertEquals("+exp_val+", res);\n"
    ut_lines[4] = "    }\n"

    return ut_lines


def main():
    i_len, num_tests, functional, expected, _ = read_data(False)
    functional = functional.split()

    for i in range(num_tests):
        params = functional[i*i_len:(i+1)*i_len]
        unit_test = prepare_unit_test(i + 1, params, expected[i])
        for ut in unit_test:
            lines.append(ut)

    lines.append("}\n")
    f_name = "../../test/java/" + target_path + target_class + "Test.java"
    os.system("mkdir -p " + "../../test/java/" + target_path)
    write_file_lines(f_name, lines[1:])


if __name__ == '__main__':
    main()
