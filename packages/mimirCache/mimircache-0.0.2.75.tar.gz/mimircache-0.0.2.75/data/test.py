# coding=utf-8
DAT = "trace.vscsi"
DAT = "w38_vscsi1.vscsitrace"

import mimircache as m
import math
from collections import defaultdict, OrderedDict
def test1():
    c = m.cachecow() 
    c.vscsi(DAT)
    d = {}
    for t, r in enumerate(c):
        if r in d:
            d[r].append(t)
        else: 
            d[r] = [t]

    print("total dic size: {}, average len: {}".format(len(d), t/len(d)))
    d_len_count = defaultdict(int)

    with open('out', 'w') as ofile:
        with open("out2", 'w') as ofile2:
            for key, value in d.items():
                if len(value) > 3:
                    ofile.write("{}: {}\n".format(key, value))
                    ofile2.write("{}: {}\n".format(key, [ int(math.log10(value[i+1]-value[i])) for i in range(len(value)-1)]))
                d_len_count[len(value)] += 1
    print(d_len_count)


def find_seq(regexS):
    import re 
    regex = re.compile(regexS)
    with open("out2") as ifile:
        for line in ifile:
            if regex.match(line):
                print(line)
test1()
find_seq("\d+: \[\d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+, \d+\]")