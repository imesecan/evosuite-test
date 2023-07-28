from util import read_file_lines, write_file_lines

target_class = "Main"
target_function = ".process"
target_return = "int"
lines = [0] * 3
lines[0] = "   @org.junit.jupiter.api.Test\n"
lines[1] = "import static org.junit.jupiter.api.Assertions.*;\n"
lines[2] = "public class MainTest {\n"


def prepare_unit_test(tid:int, prs: list, exp_val:str):
    """
        Prepare a unit test given parameters and expected values
        :param tid: test id
        :param prs: list of parameters
        :param exp_val: expected value
        :return: list
    """
    ut_lines = [0]*5
    ut_lines[0] = lines[0]
    ut_lines[1] = "    void test"+str(tid)+"(){\n"
    ut_lines[2] = "        "+target_return+" res = "+target_class+target_function+"("
    lp = len(prs)
    for i in range(lp):
        param = prs[i]
        ut_lines[2] += param
        if i < lp - 1:
            ut_lines[2] += ", "

    ut_lines[2] += ");\n"
    ut_lines[3] = "        assertEquals("+exp_val+", res);\n"
    ut_lines[4] = "    }\n"

    return ut_lines


def main():
    input_lines = read_file_lines("driver-input.txt")
    functional = input_lines[0].split()
    expected = input_lines[1].split()
    len_exp = len(expected)
    ppt = len(functional) // len_exp  # params per test
    for i in range(len_exp):
        params = functional[i*ppt : (i+1)*ppt]
        utl = prepare_unit_test(i + 1, params, expected[i])
        for l in utl:
            lines.append(l)

    lines.append("}")
    f_name = "../../test/java/" + target_class + "Test.java"
    write_file_lines(f_name, lines[1:])


if __name__ == '__main__':
    main()