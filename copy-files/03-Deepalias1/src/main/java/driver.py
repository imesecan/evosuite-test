import time
import math
import subprocess
import shlex
import sys
sys.path.append('../../../')

from util import read_data

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


def process_input():
    inputLength, numTests, functional, expected, entropy = read_data()  # len_exp, linp
    functional = functional.replace("  ", " ")
    entropy = entropy.replace("  ", " ")
    total, failed = 0, 0
    cmd = f"./run.sh \"{numTests} {functional}\""
    output, stderr = exec_cmd(cmd)
    if output is None or stderr.find("error") >= 0 or stderr.find("dumped") >= 0 or stderr.find("fault") >= 0:
        return INF, INF

    output = output.split()
    len_out = len(output)
    ll = min(len_out, numTests)
    failed = abs(numTests - len_out)
    for j in range(ll):
        if output[j] != expected[j]:
            failed += 1

    omap = dict()
    imap = dict()
    earray = entropy.split()
    len_entropy = len(earray) // inputLength
    cmd = f"./run.sh \"{len_entropy} {entropy}\""
    output, stderr = exec_cmd(cmd)
    if output is None or stderr.find("error") >= 0 or stderr.find("dumped") >= 0 or stderr.find("fault") >= 0:
        return INF, INF

    output = output.split()
    for l in range(len_entropy):
        istr = earray[inputLength*l]
        if istr in imap:
            imap[istr] += 1
        else: imap[istr] = 1

        ostr = output[l] + "^" + istr
        if ostr in omap:
            omap[ostr] += 1
        else:
            omap[ostr] = 1
    total += calculate_entropy(omap, imap)

    return total, failed / numTests


if __name__ == '__main__':
    start = time.time()
    total, failed = process_input()
    if total == INF:
        print("error:")
    else:
        max_leak = 0.62638
        print("Leak: {:.3f} Failed: {:.3f}; Time elapsed: {:.2f} seconds"
              .format(total/max_leak, failed, time.time()-start))
