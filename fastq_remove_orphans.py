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
    parser.add_argument('-1','--input1', help='Fastq file 1', required=True)
    parser.add_argument('-2','--input2', help='Fastq file 2', required=True)
    parser.add_argument('-i','--index', help='10x index file 2', required=False, default=None)
    parser.add_argument('-o','--ouput', help='Output prefix', required=True)
    args = vars(parser.parse_args())

    fastq1_file = args["input1"]
    fastq2_file = args["input2"]
    index_file = args["index"]
    output_prefix = args["ouput"]
    
    output1_file = output_prefix + "_1.fastq"
    output2_file = output_prefix + "_2.fastq"

    if index_file:
        output1_file = output_prefix + "_R1_001.fastq"
        output2_file = output_prefix + "_R2_001.fastq"
        output_index = output_prefix + "_I1_001.fastq"

    print("Create header index for R1")
    headers_r1 = set()
    with open(fastq1_file) as fh:
        while True:
            header = fh.readline()
            if not header:
                print("Completed.")
                break
            headers_r1.add(header.split()[0])
            fh.readline()
            fh.readline()
            fh.readline()
    print("Create header index for R2")
    headers_r2 = set()
    with open(fastq2_file) as fh:
        while True:
            header = fh.readline()
            if not header:
                print("Completed.")
                break
            headers_r2.add(header.split()[0])
            fh.readline()
            fh.readline()
            fh.readline()
    if index_file:
        print("Create header index for I1")
        headers_i1 = set()
        with open(index_file) as fh:
            while True:
                header = fh.readline()
                if not header:
                    print("Completed.")
                    break
                headers_i1.add(header.split()[0])
                fh.readline()
                fh.readline()
                fh.readline()
    print("Indexing results:")
    print("\t fastq1 %s reads" % len(headers_r1))
    print("\t fastq2 %s reads" % len(headers_r2))
    if index_file:
        print("\t index %s reads" % len(headers_i1))
    print("Intersection:")
    positive_list = headers_r1.intersection(headers_r2).intersection(headers_i1)
    print("Result: %s reads remains" % len(positive_list))

    print("Saving fastq1 reads...")
    with open(output1_file, "w") as fw:
        with open(fastq1_file) as fh:
            while True:
                header = fh.readline()
                if not header:
                    print("Completed.")
                    break
                seq = fh.readline()
                strand = fh.readline()
                Q = fh.readline()

                key = header.split()[0]
                if not key in positive_list:
                    continue
                fw.write(header)
                fw.write(seq)
                fw.write(strand)
                fw.write(Q)

    print("Saving fastq2 reads...")
    with open(output2_file, "w") as fw:
        with open(fastq2_file) as fh:
            while True:
                header = fh.readline()
                if not header:
                    print("Completed.")
                    break
                seq = fh.readline()
                strand = fh.readline()
                Q = fh.readline()

                key = header.split()[0]
                if not key in positive_list:
                    continue
                fw.write(header)
                fw.write(seq)
                fw.write(strand)
                fw.write(Q)

    if index_file:
        print("Saving index reads...")
        with open(output_index, "w") as fw:
            with open(index_file) as fh:
                while True:
                    header = fh.readline()
                    if not header:
                        print("Completed.")
                        break
                    seq = fh.readline()
                    strand = fh.readline()
                    Q = fh.readline()

                    key = header.split()[0]
                    if not key in positive_list:
                        continue
                    fw.write(header)
                    fw.write(seq)
                    fw.write(strand)
                    fw.write(Q)
