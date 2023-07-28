import os, time, random
import queue, math, argparse
from copy import deepcopy
import subprocess, shlex
from util import read_file_lines, write_file_lines

MAX_BITS = 32   # for low and high priv. inputs
SEARCH_RANGE = (2 ** MAX_BITS)
RANGE = SEARCH_RANGE // 2
nlow = 6        # number of lows 50
nhigh = 20      # number of highs for every low 5
budget = 4      # total budget for every low-high pair 10

"""
    Que = priority queue of inputs according to the leakage.
    while(range > 2)
    {
        range = range / 2;
        # process for the lower_half
        sum_lower_half = 0
        For each budget: 
            For each low in the range of nlow
                // random side values within the range
                start, s1, s2 = generate_Low(range) 
                hset = Generate a set of high values (range, start)
                leak = Measure the leakage for the set (s1, s2, hset)
                sum_lower_half += leak
                Add this in to the priority queue (s1, s2, hset)

        # process for the upper_half
        sum_upper_half = 0
        For each budget: 
            For each low in the range of nlow
                // random side values within the range
                start, s1, s2 = generate_Low(range) 
                hset = Generate a set of high values (range, start)
                leak = Measure the leakage for the set (s1, s2, hset)
                sum_upper_half += leak
                Add this in to the priority queue (s1, s2, hset)

        Choose and continue with the half which has more leakage 
    }
"""


class Item:
    def __init__(self, sec, low):
        self.sec = sec
        self.low = low

    def __hash__(self):
        return hash((self.sec, self.low))

    def __eq__(self, other):
        """Overrides the default implementation"""
        if not isinstance(other, Item):
            return False
        return self.sec == other.sec and \
            self.low == other.low

    def __lt__(self, other):
        if self.sec != other.sec:
            return self.sec < other.sec
        
        return self.low < other.low


class TestPair:
    def __init__(self):
        self.leak = 0
        self.low = 0
        self.input = ""
        self.secret = []
        self.output = []
        self.cnt = 0

    def __lt__(self, other):
        return self.leak < other.leak


def print_obj(sec, st1):
    print("{} {}".format(sec, st1))


def generate_high(lb, ub):
    
    return random.randrange(lb, ub)


def generate_low(lb, ub):
    
    return random.randrange(lb, ub)


def insert(temp: TestPair):
    pque.put(deepcopy(temp))
    if pque.qsize() > nlow * 2:
        pque.get()


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


def exec_cmd(cmd, t_out=15):
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


def run4all(low: int, lb: int, ub: int):
    test = TestPair()
    omap = dict()
    imap = dict()
    test.s2 = low
    istr = str(low)
    test.input = istr
    inputs = ""
    secrets = []
    for h in range(nhigh):
        sec = generate_high(lb, ub)
        secrets.append(sec)
        inputs += (str(sec) + " " + str(low) + " ")
    cmd = "./run.sh \"{} {}\" ".format(nhigh, inputs)
    results = exec_cmd(cmd).split()
    
    if results is None:
        print(secrets, low, results)
        sys.exit(0)
    # print(cmd, results)
    for k in range(nhigh):
        res = results[k]
        ostr = res + "^" + istr
        if ostr in omap:
            omap[ostr] += 1
        else:
            omap[ostr] = 1
        if istr in imap:
            imap[istr] += 1
        else:
            imap[istr] = 1

    test.leak = calculate_entropy(omap, imap)
    test.low = low
    test.secret = secrets
    insert(test)
    return test.leak


def run4h(low: int, lb: int, ub: int):
    mid = lb + (ub - lb) // 2
    l_sum = 0  # sum of the leaks for the lower half
    for b in range(budget):
        for l in range(nlow):
            l_sum += run4all(low, lb, mid)

    u_sum = 0  # sum of the leaks for the upper half
    for b in range(budget):
        for l in range(nlow):
            u_sum += run4all(low, mid, ub)

    if l_sum > u_sum:
        return lb, mid, l_sum
    if l_sum < u_sum:
        return mid, ub, u_sum

    if random.randrange(0, 100) < 50:
        return lb, mid, l_sum
    
    return mid, ub, u_sum


def run_4h(low: int):
    total = 0
    lb = -RANGE
    ub = SEARCH_RANGE - RANGE
    start = time.time()
    while ub - lb >  32:
        lb, ub, tmp = run4h(low, lb, ub)
        total += tmp

    print(lb, ub, "{:.2f}".format(tmp), "{:.1f} s".format(time.time() - start))

    return total


def run_4l(lb, ub):
    mid = lb + (ub - lb) // 2
    l_sum = 0  # sum of the leaks for the lower half
    for b in range(budget):
        for l in range(nlow):
            low = generate_low(lb, mid)
            l_sum += run_4h(low)

    u_sum = 0  # sum of the leaks for the upper half
    for b in range(budget):
        for l in range(nlow):
            low = generate_low(mid, ub)
            u_sum += run_4h(low)

    if l_sum > u_sum:
        return lb, mid, l_sum
    if l_sum < u_sum:
        return mid, ub, u_sum

    if random.randrange(0, 100) < 50:
        return lb, mid, l_sum
    
    return mid, ub, u_sum


def main():
    result_set = set()
    k = 0
    lb = -RANGE
    ub = SEARCH_RANGE - RANGE
    start = time.time()
    while ub - lb > 32:
        k += 1
        lb, ub, tmp = run_4l(lb, ub)
        print(k, lb, ub, "{:.0f}".format(tmp),
            "{:.0f} seconds".format(time.time() - start))

    print(k)
    print("===        Start of Entropy input set for the driver.py             ====")
    print("===    Format for for every number triple: secret, side2, side3 ,   ====")

    total = cnt = 0
    pr_st = ""
    while not pque.empty():
        cur = pque.get()
        total += cur.leak
        for h in cur.secret:
            item = Item(h, cur.low)
            if not (item in result_set):
                cnt += 1
                result_set.add(deepcopy(item))
                if len(result_set) >= nhigh * nlow:
                    break
                pr_st += "{} {} ".format(h, cur.low)
                print("{} {} ".format(h, cur.low), end='')
                if cnt % 5 == 0: print()

    f_name = "driver-input.txt"
    input_lines = read_file_lines(f_name)
    len_il = len(input_lines)
    if len_il < 3:
        for i in range(3 - len_il):
            input_lines.append("\n")
    input_lines[2] = pr_st + "\n"
    write_file_lines(f_name, input_lines)

    print("\n{:.1f} bits {:.0f} seconds".format(total, time.time() - start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python script to generate hyper test set.')
    parser.add_argument('--seed', type=int, default=0, help='randomization seed')
    parser.add_argument('--bits', type=int, default=0, help='# max bits for the search space')
    parser.add_argument('--nlow', type=int, default=0, help='# low priv. inputs')
    parser.add_argument('--nhigh', type=int, default=0, help='# high priv. inputs')
    parser.add_argument('--budget', type=int, default=0, help='Budget for every low-high pair')
    args = parser.parse_args()

    if args.seed == 0:
        args.seed = time.time()     
    if args.bits > 0: 
        MAX_BITS = args.bits        
        SEARCH_RANGE = (2 ** MAX_BITS)
        RANGE = SEARCH_RANGE // 2
    if args.nlow > 0: 
        nlow = args.nlow            
    if args.nhigh > 0: 
        nhigh = args.nhigh          
    if args.budget > 0: 
        budget = args.budget        
    random.seed(args.seed)

    pque = queue.PriorityQueue()
    cmd = "./build.sh "
    exec_cmd(cmd)
    main()
    cmd = "./build.sh "
    print(exec_cmd(cmd))
