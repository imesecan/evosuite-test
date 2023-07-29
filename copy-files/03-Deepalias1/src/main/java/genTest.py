import argparse
import time
import queue
from random import randrange, seed
import math
from copy import deepcopy
import subprocess
import shlex
import sys
sys.path.append('../../../')
from util import read_data, invalidResult

INVALID_RESULT = -1
debug = 0
cnt = 0
pque = queue.PriorityQueue()
start = time.time()


class TestPair:
    def __init__(self,  sec=0, low=0):
        self.sec = sec
        self.low = low
        self.leak = 0
        self.input = ""
        self.secret = []
        self.output = []

    def __hash__(self):
        return hash((self.sec, self.low, tuple(self.output)))

    def reset_low(self, low, istr):
        self.low = low
        self.input = istr

    def __lt__(self, other):
        return self.leak < other.leak

    def __repr__(self):
        return f"{self.sec} {self.low} "


def insert(temp: TestPair):
    """
    Inserts the object temp into a priority queue. It keeps only 2 * nlow items
    with the largest entropy values.
    input temp (TestPair): TestPair contains a low input and a set of high inputs
    returns None
    """
    global pque
    pque.put(deepcopy(temp))
    if pque.qsize() > 2 * nlow:
        pque.get()


def process_map(mp):
    """
    Given a mp (map of string to integer):
        * calculates the probability of each string
        * calculates the entropy of the set using Shannon’s formula
    input mp (map of string to integer): the number of occurrences of each string
    returns total (float): entropy of the set using shannon's formula
    """
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
    """
    Calculates and returns amount of information leakage, given input and output probabilities
    imap (map of string to integer): input map, occurrences of input strings
    omap (map of string to integer): output map, occurrences of output strings
    returns (float): amount of information leaking
    """
    res_out = process_map(omap)
    res_in = process_map(imap)

    return res_out - res_in


def exec_cmd(cmd, t_out=15):
    """
    Given a command string (cmd), executes the command using a time limit of t_out seconds
    input cmd (string): any command line script to run with its parameters
    input t_out (int): time limit to run this command.

    returns stdout (string): from the execution of the command. If the command
            (cmd) does not finish in t_out seconds, the command is terminated
            and returns None
    """
    s_process = subprocess.Popen(
        shlex.split(cmd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    try:
        stdout, stderr = s_process.communicate(timeout=t_out)
        return stdout.decode("ascii")
    except subprocess.TimeoutExpired:
        s_process.send_signal(9)
        return None


def incrementMap(mp, key, val=1):
    """
    This function:
        if key does not exist in the map (mp), inserts the key into the map with a value of 1
        otherwise, it increments the number of occurrences of the key in the map
    input mp (map of string to integer): is the map to process
    input key (string): is the string key
    input val (integer): is the increment value, if it is 5, map is incremented 5 by 5
    returns mp (map)
    """
    if key in mp:
        mp[key] += val
    else:
        mp[key] = val

    return mp


def process_output(low_input, arr, results):
    """
    This function
        * receives a low_input, a set of high inputs (arr) and a set of low outputs (results)
        * calculates and returns the entropy of this set
        * and, it inserts this set into a priority queue based on the entropy of this set,
    input low_input (integer):
    input arr (string array): is a string array for high inputs
    input results (string array): is the string array of outputs when running the
            target program with this low and set of high inputs.
    """
    global cnt
    cnt += nhigh
    if debug:
        print(f"Run {cnt}: {arr} {results}")
    test = TestPair()
    imap, omap = dict(), dict()
    secret, output = [], []
    istr = str(low_input)
    test.reset_low(low_input, istr)
    imap = incrementMap(imap, istr, nhigh)
    for j in range(nhigh):
        sec = int(arr[j])
        secret.append(sec)
        out = results[j]
        output.append(out)
        ostr = out + "-" + istr
        omap = incrementMap(omap, ostr)

    test.leak = calculate_entropy(omap, imap)
    test.output = output
    test.secret = secret
    insert(test)

    return test.leak


def run(cmd, low_input):
    """
    Given a low input (e.g. 137) and two sets of high inputs in lower and upper halves
        of the current input space, e.g. '28 44 108 8 21   155 144 192 208 215 '
        this function runs the target program using current sets and returns the amount of
        information leaking from each.
    It uses ./GenTestRun.sh which is in TestSubject/src/main/java
        And GenTestRun uses org/leakreducer/GenTestDriver which must be compiled before starting
    input cmd (string): is 2-sets of space separated high inputs as a string
    input low_input (int): is an integer
    returns res (float): amount of information leaking when using low_input with the set of high
                        inputs from upper or lower halves
    """
    if len(cmd) == 0:
        return 0
    arr = cmd.split()
    cmd = f"./GenTestRun.sh \"{nhigh} {low_input} {cmd}\""
    if debug:
        print(cmd)
    results = exec_cmd(cmd).split()

    l_res = process_output(low_input, arr[:nhigh], results[:nhigh])
    u_res = process_output(low_input, arr[nhigh:], results[nhigh:])
    if debug:
        print(f"{l_res:.1f} {u_res:.1f}")

    return l_res, u_res


def generateHigh(lo, hi, begin=0):
    """
    Given low and high limits of the search range, it generates a set of (nhigh) high inputs
    input lo (integer): lower limit of input search range
    input hi (integer): upper limit of input search range
    returns secret (string): space separated high inputs
    """
    if lo >= hi:
        return invalidResult(nhigh, INVALID_RESULT)
    
    secret = ""
    for j in range(begin, nhigh):
        sec = randrange(lo, hi)
        secret += f"{sec} "

    return secret


def useFunctionalTests(i_len, num_tests, functional, lo, hi):
    """
    To improve entropy set search process, this function uses existing
        functional tests collected by EvoSuite, in their corresponding (lo, hi) bins
    @param i_len: input length (number of parameters in the function call)
    @param num_tests: number of tests
    @param functional: functional test set
    @param lo: lower limit of input search-space
    @param hi: upper limit of input search-space

    @return: entropy of current set items within the current input search space
    """
    l_sum, u_sum = 0, 0
    mid = lo + (hi - lo) // 2
    for k in range(num_tests):
        test = functional[k*i_len:(k+1)*i_len]
        sec, low = test[0], int(test[1])
        l_sec = invalidResult(nhigh, INVALID_RESULT)
        u_sec = invalidResult(nhigh, INVALID_RESULT)

        found = False
        if lo <= low < mid:
            found = True
            l_sec = f"{sec} " + generateHigh(lo, mid, begin=1)
        elif mid <= low < hi:
            found = True
            u_sec = f"{sec} " + generateHigh(mid, hi, begin=1)

        if found:
            l_val, u_val = run(l_sec + u_sec, low)
            l_sum += l_val
            u_sum += u_val
    
    return l_sum, u_sum


def compare(lsum, usum, lo, mid, hi):
    if lsum >= usum:
        return lo, mid

    return mid, hi


def run4high(low_input):
    """
    This function runs a randomized algorithm similar to binary search. For each low input, it
        * generates a set of highs in the upper and lower half of the search range,
        * calculates the total amount of information leaking in each half of the search range
        * then chooses and continues with the half which detected more leakage
    input low_input (integer): current low input
    returns total (float): amount of information leakage detected for this low input
    """
    total, lo, hi = 0, 0, INT_MAX
    while (hi - lo) > 2:
        mid = lo + (hi - lo) // 2
        l_inputs = generateHigh(lo, mid)
        h_inputs = generateHigh(mid, hi)
        l_sum, u_sum = run(l_inputs + h_inputs, low_input)
        total += max(l_sum, u_sum)
        lo, hi = compare(l_sum, u_sum, lo, mid, hi)

    return total


def run4low():
    """
    This function uses global inputs (nhigh, nlow, budget) and runs for all low inputs
    return: leak (float) the amount of leak detected
    """
    i_len, num_tests, functional, _, _ = read_data(False)
    functional = functional.split()

    lo, hi, k = 0, INT_MAX, 0
    leak = 0
    begin = time.time()
    while (hi - lo) > 2:
        k += 1
        print(f"lo: {lo} hi: {hi} ", end='')
        mid = lo + (hi - lo) // 2
        # l_sum / u_sum: sum of the leaks for the lower/upper half
        l_sum, u_sum = useFunctionalTests(i_len, num_tests, functional, lo, hi)
        
        for b in range(budget):
            for _ in range(nlow//2):
                low_input = randrange(lo, mid)
                l_sum += run4high(low_input)

        for b in range(budget):
            for _ in range(nlow//2):
                low_input = randrange(mid, hi)
                u_sum += run4high(low_input)

        leak += max(l_sum, u_sum)
        lo, hi = compare(l_sum, u_sum, lo, mid, hi)
            
        elapsed = time.time() - begin
        print(f"Elapsed: {elapsed:.0f} sec; - l_sum: {l_sum:.1f} - u_sum: {u_sum:.1f}")

    return leak


def main():
    """
    k (int): Instead of generating one large set of L (low),
             if we want to run multiple times on L generating
             multiple sets of low and accumulating the result set.
    res_set (set): is a set containing all unique TestPairs
    r_cnt (dic): is a dictionary containing possible output counts
    """
    res_set, res_cnt = set(), {}    
    global pque
    begin = time.time()
    leak = run4low()
    elapsed = time.time() - begin
    print(f"Elapsed: {elapsed:.0f} seconds - leak: {leak:.1f}")
    print("===   Entropy input set. Format for for every number pair: low, secret   ====")

    c = 0
    while not pque.empty() and c < nhigh * nlow:
        cur = pque.get()
        for k, h in enumerate(cur.secret):
            item = TestPair(h, cur.low)
            if k >= nhigh:
                break
            if not (item in res_set):
                c += 1
                res_set.add(deepcopy(item))
                res_cnt = incrementMap(res_cnt, cur.output[k])
                print(item, end='')
                if c % nhigh == 0:
                    print()
    print(res_cnt)


if __name__ == "__main__":
    """
    Main function 
        *) gets parameters from the user and 
        *) initializes a randomization seed using the jobid
        *) and starts the search process   
    """
    parser = argparse.ArgumentParser(description='Entropy test set generator')
    parser.add_argument('--nlow', type=int, default=20, help='Number of low inputs')
    parser.add_argument('--nhigh', type=int, default=10, help='Number of high inputs')
    parser.add_argument('--max', type=int, default=31, help='Power of 2 for INT_MAX')
    parser.add_argument('--budget', type=int, default=1, help='Budget multiplier')
    parser.add_argument('--jobid', type=int, default=0, help='A unique identifier to define current run')
    args = parser.parse_args()
    seed(args.jobid)

    nlow, nhigh = args.nlow, args.nhigh
    INT_MAX, budget = (2 ** args.max), args.budget

    print(f"nlow: {nlow}, nhigh: {nhigh}, MAX: {INT_MAX}, budget: {budget}")
    main()
