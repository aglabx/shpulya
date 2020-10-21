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
    parser.add_argument('-i','--index', help='10x or other index file', required=False, default=None)
    parser.add_argument('-o','--ouput', help='Output index file name.', required=True)
    parser.add_argument('--indexlength', help='Index length (default 8)', required=False, default=8)
    args = vars(parser.parse_args()) 

    index_file_gz = args["index"]
    output_file = args["ouput"]
    index_read_length = int(args["indexlength"])

    if index_file_gz:
        if not index_file_gz.endswith(".gz"):
            print("File %s should be with .gz extension." % index_file_gz)
            sys.exit(10)

    index_file = ".".join(index_file_gz.split(".")[:-1]) + ".unpacked"

    ### check gzrecover
    working_folder = os.path.dirname(os.path.abspath(__file__))
    exe_path = os.path.join(working_folder, "gzrt/gzrecover")
    step1_path = os.path.join(working_folder, "fastq_fix_corrupted_file.py")
    step2_path = os.path.join(working_folder, "fastq_remove_orphans.py")
    make_dir = os.path.join(working_folder, "gzrt")
    if not os.path.isfile(exe_path):
        subprocess.Popen(["make"], cwd=make_dir, shell=True)

    ### step 1. gzrecover
    temp_file = output_file + ".temp"

    with open(temp_file, "w") as fw:
        fw.write("%s -o %s %s" % (exe_path, index_file, index_file_gz))
    command = "less %s | xargs -P 3 -I {} sh -c '{}'" % temp_file
    print(command)
    subprocess.check_call(command, shell=True)

    ### step 2. Remove junk
    with open(temp_file, "w") as fw:
        fw.write("python %s -i %s -o %s -l %s -m %s" % (step1_path, index_file, output_file, index_read_length, index_read_length))
    command = "less %s | xargs -P 3 -I {} sh -c '{}'" % temp_file
    print(command)
    subprocess.check_call(command, shell=True)
    os.unlink(index_file)
    os.unlink(temp_file)



