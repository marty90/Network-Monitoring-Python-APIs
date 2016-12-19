#!/usr/bin/python3

import argparse
import numpy as np
import statistics

parser = argparse.ArgumentParser( formatter_class=argparse.RawDescriptionHelpFormatter,
    description="Compute simple statistics about distribution of set of samples.\n\
    Can configure which indicators to print using the second argument.\n\
    It is possible to use mean, stdev, median, minim, maxim, perc_X (X must in {1,2,5,10,25,50,75,90,95,98,99} ).\n\
    The variables samples is samples list itself.\n\
    Output format must be a python expression.",
    epilog="Example:\n\
    \t./samples_statistics.py samples.txt 'perc_25, median, perc_75'\n\
    prints 25, 50 and 75 percentile of the input distribution.\
    "
    )
                                                      
parser.add_argument('input_file', metavar='input_file', type=str, 
                   help='Input file. Must be organized in rows and colums')
parser.add_argument('output_format', metavar='output_format', type=str, 
                   help='Format for output.  Python expression')                    
parser.add_argument('-c', '--column', metavar='column', type=int,default=1,
                       help='Input log files path.') 
parser.add_argument('-s', '--separator', metavar='separator', type=str, default=" ", 
                       help='Separator field in input file.')


args = vars(parser.parse_args())
input_file=args["input_file"]
output_format=args["output_format"]
column=args["column"] -1 
separator=args["separator"]

samples=[]
for row in open(input_file, "r"):
    try:
        s = float(row.split(separator)[column] )
        samples.append(s)
    except:
        continue

ss_numpy=np.array(samples)
perc_1 = np.percentile(ss_numpy, 1)
perc_2 = np.percentile(ss_numpy, 2)
perc_5 = np.percentile(ss_numpy, 5)
perc_10 = np.percentile(ss_numpy, 10)
perc_25 = np.percentile(ss_numpy, 25)
perc_50 = np.percentile(ss_numpy, 50)
perc_75 = np.percentile(ss_numpy, 75)
perc_90 = np.percentile(ss_numpy, 90)
perc_95 = np.percentile(ss_numpy, 95)
perc_98 = np.percentile(ss_numpy, 98)
perc_98 = np.percentile(ss_numpy, 99)

median = perc_50
mean=statistics.mean(samples)
stdev=statistics.stdev(samples)
maxim = max(samples)
minim = min(samples)

eval("print( " + output_format + ")")


