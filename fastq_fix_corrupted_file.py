#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2020
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
import argparse
import os

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Fix messed fastq files')
    parser.add_argument('-i','--input', help='Input fastq file', required=True)
    parser.add_argument('-o','--ouput', help='Output fastq file', required=True)
    parser.add_argument('-l','--minlength', help='Maximal read length', required=True)
    parser.add_argument('-m','--maxlength', help='Maximal read length', required=True)
    args = vars(parser.parse_args())

    fastq1_file = args["input"]
    output1_file = args["ouput"]
    min_read_length = int(args["minlength"])
    max_read_length = int(args["maxlength"])
    
    fw1 = open(output1_file, "w")
    i = 0
    with open(fastq1_file) as fh1:
        while fh1:
            header = fh1.readline()
            if not header:
                print("Completed for %s." % fastq1_file)
                break
            if not header.startswith("@"):
                continue
            seq = fh1.readline()
            l = len(seq.strip())
            if l < min_read_length or l > max_read_length:
                continue
            if len([x for x in seq.strip() if not x in ["A","T","G","C","N"]]):
                continue
            strand = fh1.readline()
            if strand and strand[0] not in ["+", "-"]:
                continue
            Q = fh1.readline()
            if not len(Q) == len(seq):
                continue
            fw1.write(header)
            fw1.write(seq)
            fw1.write(strand)
            fw1.write(Q)
            i += 1
            if i % 1000000 == 0:
                print("Saved: %sM reads for %s" % (i//1000000, fastq1_file))
    fw1.close()


