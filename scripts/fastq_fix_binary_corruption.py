#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 15.11.2021
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
import argparse


def iter_item_from_suspicious_fastq(fh):
    ''' Iterate over corrupted fastq file.
    '''
    
    header, seq, strand, Q = None, None, None, None

    while True:
        string = fh.readline()
        if not string:
            break
        if string.startswith("@"):
            header, seq, strand, Q = string, None, None, None
            continue
        if header and (seq is None) and max(string) == "T" and min(string[:-1]) == "A":
            seq = string
            continue
        if string == "+\n":
            strand = string
            continue
        if seq and strand and len(string) == len(seq):
            yield (header, seq, strand, string)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Restore corrupted FastQ dataset with Index file')
    parser.add_argument('-1','--input1', help='Fastq file 1', required=True)
    parser.add_argument('-2','--input2', help='Fastq file 2', required=True)
    parser.add_argument('-I','--index', help='Index file', required=True)
    parser.add_argument('-m','--mode', help='Mode', required=False, default="drop")
    parser.add_argument('-p', help='head_pattern', required=False, default=None)
    parser.add_argument('-o','--prefix', help='Output prefix', required=True)
    args = vars(parser.parse_args())

    fastq1_file = args["input1"]
    fastq2_file = args["input2"]
    index_file = args["index"]

    prefix = args["prefix"]
    head_pattern = args["p"]
    mode = args["mode"]

    output1_file = prefix + "_R1.fastq"
    output2_file = prefix + "_R2.fastq"
    outputI_file = prefix + "_I1.fastq"

    left_pairs = {}
    right_pairs = {}
    index_parts = {}

    print("Read files...")

    fh1 = open(fastq1_file, errors="replace")
    fh2 = open(fastq2_file, errors="replace")
    fhI = open(index_file, errors="replace")

    fw1 = open(output1_file, "w")
    fw2 = open(output2_file, "w")
    fwI = open(outputI_file, "w")

    i = 0

    dataset = {}

    iter1 = read_item_from_suspicious_fastq(fh1)
    iter2 = read_item_from_suspicious_fastq(fh2)
    iterI = read_item_from_suspicious_fastq(fhI)

    while True:

        i += 1
        if i % 1000000 == 0:
            print(i)

        try:
            header1, seq1, strand1, Q1 = next(iter1)
            header2, seq2, strand2, Q2 = next(iter2)
            headerI, seqI, strandI, QI = next(iterI)
        except:
            break

        name = header1.split()[0]
        dataset.setdefault(name, [None, None, None])
        dataset[name][0] = [header1, seq1, strand1, Q1]

        name = header2.split()[0]
        dataset.setdefault(name, [None, None, None])
        dataset[name][1] = [header2, seq2, strand2, Q2]

        name = headerI.split()[0]
        dataset.setdefault(name, [None, None, None])
        dataset[name][2] = [headerI, seqI, strandI, QI]


    for item in dataset:
        if item[0] and item[1] and item[2]:
            fw1.write("".join(item[0]))
            fw2.write("".join(item[1]))   
            if item[2][0] == item[0][0]:
                fw3.write(item[2])
            else:
                seqI = item[0][0].split(":")[-1]
                headerI = item[0][0]
                strandI = "+"
                q = "F"*(len(seqI)-1)
                QI = f"{q}\n"
                fwI.write("".join([headerI, seqI, strandI, QI]))

    fh1.close()
    fh2.close()
    fhI.close()

    fw1.close()
    fw2.close()
    fwI.close()
