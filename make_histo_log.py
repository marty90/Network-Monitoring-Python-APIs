#!/usr/bin/python3

import os
import sys
import numpy as np


#./make_histo.pl inter_time_samples.txt 1 0 3600000 10000000 > histo_tcp.txt

header="#bin\trange\ttot\tdist\tcum"
precision=6

def main():
    
    in_file=sys.argv[1]
    column = int(sys.argv[2])
    min_bin=int(sys.argv[3])
    max_bin=int(sys.argv[4])
    nb_bin=int(sys.argv[5])
    
    data =   [ float(row.split()[column-1]) for row in open(in_file,"r").read().splitlines() ]
    length= len (data)
    (num, bins ) = np.histogram(data, bins=[0] + list(np.logspace(min_bin, max_bin, nb_bin)) )
    
    print(header)
    last=0
    for i in range(nb_bin):

        print (i, round(bins[i], precision) , round(num[i], precision), round(num[i]/length, precision), round(num[i]/length+last, precision), sep='\t')
        last=num[i]/length+last

if __name__ == "__main__":
    main()







