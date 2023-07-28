import time
import math
import subprocess
import shlex

nlow = 50  # number of lows
nhigh = 5  # number of highs for every low
INF = (2**31) - 1


def prepare_input(val):
    pos1 = val.find("_")
    pos2 = val.find("-")

    hex_res = val[:pos1]
    l1 = int(val[pos1+1:pos2])
    l2 = int(val[pos2+1:])

    return l1, l2, hex_res


def process_map(mp):
    numel = 0
    for count, elem in enumerate(mp):
        val = mp[elem]
        numel += val

    total = 0
    for count, elem in enumerate(mp):
        val = mp[elem]
        prob = val / numel
        total += (-prob * math.log(prob, 2))

    return total


def calculate_entropy(omap, imap):
    res_out = process_map(omap)
    res_in = process_map(imap)

    return res_out - res_in


def exec_cmd(cmd, t_out=1):
    s_process = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    try:
        stdout, stderr = s_process.communicate(timeout=t_out)
        return stdout.decode("ascii"), stderr.decode("ascii")
    except subprocess.TimeoutExpired:
        s_process.send_signal(9)

    return None, None


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
    except Exception:
        return []

    return lines


def get_data():
    lines = read_file_lines("driver-input.txt")
    functional = lines[0]
    expected = lines[1].split()
    lexp = len(expected)
    for i in range(lexp):
        expected[i] = int(expected[i])

    entropy = lines[2]
    return functional, expected, entropy, lexp


def process_input():
    fnctl, expected, entpy, len_exp = get_data()
    total = failed = 0
    fnctl2 = str(len_exp)+" " + fnctl;
    cmd = "./run.sh \"{}\" ".format(fnctl2)
    output, stderr = exec_cmd(cmd)
    if output is None or stderr.find("error") >= 0 or stderr.find("dumped") >= 0 or stderr.find("fault") >= 0:
        return INF, INF

    output = output.split("\n")
    k = 0
    for k in range(len(output) - 1):
        if int(output[k]) != expected[k]:
            failed += 1
        k += 1
        if k == len(output):
            failed += (len_exp - k)
            break

    omap = dict()
    imap = dict()
    earray = entpy.split(" ")
    len_entropy = len(earray)
    entpy2 = str(len_entropy)+" "+entpy
    cmd = "./run.sh \"{}\" ".format(entpy2)
    output, stderr = exec_cmd(cmd)
    if output is None or stderr.find("error") >= 0 or stderr.find("dumped") >= 0 or stderr.find("fault") >= 0:
        return INF, INF

    output = output.split("\n")
    earray = entpy.split(" ")
    for l in range(len_entropy // 2):
        istr = str(earray[2*l + 1])
        if istr in imap:
            imap[istr] += 1
        else: imap[istr] = 1

        ostr = output[l] + "^" + istr
        if ostr in omap:
            omap[ostr] += 1
        else:
            omap[ostr] = 1
    total += calculate_entropy(omap, imap)

    return total, failed / len_exp 


if __name__ == '__main__':
    start = time.time()
    total, failed = process_input()
    if total == INF:
        print("error:")
    else:
        max_leak = 1.0
        print("Leak: {:.4f} Failed: {:.3f}; Time elapsed: {:.2f} seconds"
              .format(total/max_leak, failed, time.time()-start))
