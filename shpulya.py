#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 10.10.2020
#@author: Aleksey Komissarov
#@contact: ad3002@gmail.com

import sys
import argparse
import os
import subprocess

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Shpulya: recover your sequence data from corrupted achives.')
    parser.add_argument('-1','--input1', help='Fastq file 1', required=True)
    parser.add_argument('-2','--input2', help='Fastq file 2', required=True)
    parser.add_argument('-i','--index', help='10x or other index file', required=False, default=None)
    parser.add_argument('-o','--ouput', help='Output prefix', required=True)
    parser.add_argument('--minlength', help='Maximal read length', required=True)
    parser.add_argument('--maxlength', help='Maximal read length', required=True)
    parser.add_argument('--indexlength', help='Index length (default 8)', required=False, default=None)
    args = vars(parser.parse_args()) 

    fastq1_file_gz = args["input1"]
    fastq2_file_gz = args["input2"]
    index_file_gz = args["index"]
    output_prefix = args["ouput"]
    min_read_length = int(args["minlength"])
    max_read_length = int(args["maxlength"])
    index_read_length = int(args["indexlength"])

    if not fastq1_file_gz.endswith(".gz"):
        print("File %s should be with .gz extension." % fastq1_file_gz)
        sys.exit(10)
    if not fastq2_file_gz.endswith(".gz"):
        print("File %s should be with .gz extension." % fastq2_file_gz)
        sys.exit(10)
    if index_file_gz:
        if not index_file_gz.endswith(".gz"):
            print("File %s should be with .gz extension." % index_file_gz)
            sys.exit(10)

    fastq1_file = ".".join(fastq1_file_gz.split(".")[:-1])
    fastq2_file = ".".join(fastq2_file_gz.split(".")[:-1])
    if index_file_gz:
        index_file = ".".join(index_file_gz.split(".")[:-1])


    fastq1_file_orph = ".".join(fastq1_file_gz.split(".")[:-1]) + ".with_orphans"
    fastq2_file_orph = ".".join(fastq2_file_gz.split(".")[:-1]) + ".with_orphans"
    if index_file_gz:
        index_file_orph = ".".join(index_file_gz.split(".")[:-1]) + ".with_orphans"

    ### check gzrecover
    working_folder = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(working_folder, "gzrt/gzrecover")
    step1_path = os.path.join(working_folder, "fastq_fix_corrupted_file.py")
    step2_path = os.path.join(working_folder, "fastq_remove_orphans.py")
    make_dir = os.path.join(working_folder, "gzrt")
    if not os.path.isfile(exe_path):
        subprocess.Popen(["make"], cwd=make_dir, shell=True)

    ### step 1. gzrecover
    temp_file = output_prefix + ".temp"

    with open(temp_file, "w") as fw:
        fw.write("%s -o %s %s\n" % (exe_path, fastq1_file, fastq1_file_gz))
        fw.write("%s -o %s %s\n" % (exe_path, fastq2_file, fastq2_file_gz))
        if index_file_gz:
            fw.write("%s -o %s %s" % (exe_path, index_file_gz, index_file))
    command = "less %s | xargs -P 3 -I {} sh -c '{}'" % temp_file
    print(command)
    subprocess.check_call(command, shell=True)

    ### step 2. Remove junk
    with open(temp_file, "w") as fw:
        fw.write("python %s -i %s -o %s -l %s -m %s\n" % (step1_path, fastq1_file, fastq1_file_orph, min_read_length, max_read_length))
        fw.write("python %s -i %s -o %s -l %s -m %s\n" % (step1_path, fastq2_file, fastq2_file_orph, min_read_length, max_read_length))
        if index_file_gz:
            fw.write("python %s -i %s -o %s -l %s -m %s" % (step1_path, index_file_orph, index_file, index_read_length, index_read_length))
    command = "less %s | xargs -P 3 -I {} sh -c '{}'" % temp_file
    print(command)
    subprocess.check_call(command, shell=True)

    os.unlink(fastq1_file)
    os.unlink(fastq2_file)
    if index_file_gz:
        os.unlink(index_file)

    ### step 3. Fix orphans
    if index_file_gz:
        command = "python %s -1 %s -2 %s -i %s -o %s" % (step2_path, fastq1_file_orph, fastq2_file_orph, index_file_orph, output_prefix)
    else:
        command = "python %s -1 %s -2 %s -o %s" % (step2_path, fastq1_file_orph, fastq2_file_orph, output_prefix)
    print(command)
    subprocess.check_call(command, shell=True)

    os.unlink(temp_file)
    os.unlink(fastq1_file_orph)
    os.unlink(fastq2_file_orph)
    if index_file_gz:
        os.unlink(index_file_orph)



