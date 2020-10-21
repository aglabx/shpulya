# shpulya: recover your sequence data from corrupted archives

When transmitting gzipped data via ftp in text form, you can get corrupted data at the output. Ideally, check md5 after transfer, but this is sometimes forgotten. And after a lot of time someone can notice that the data is corrupted. Shpulya tries to recover the maximum amount of correct data from such data for further analysis.

Shpylya consists of three steps:

1) unpacking a damaged archive using gzrecover (https://github.com/arenn/gzrt);
2) removing the garbage from the unpacked data;
3) recovery of paired and corresponding index file, if there is such a file, for example, 10Х data for scRNA.

## Installation

Clone this repository:

```
git clone https://github.com/aglabx/shpulya.git
cd shpulya
```

Compile gzrecover:

```
cd gzrt
make
```

If you have any issues with gzrecover installation, please read correspoing README file in gzrt folder.

## Usage

Command for usual pair ends data:

```
python shpulya.py -1 corrupted_1.fastq.gz -2 corrupted_2.fastq.gz -o ouput_file_prefix --minlength 50 --maxlength 160
```

where:

- **ouput_file_prefix** - prefix to which will be added _1.fastq and _2.fastq;
- **minlength** - minimal expected sequence length, shpulya will drop all reads shoter that minimal length;
- **minlength** - maximal expected sequence length, shpulya will drop all reads longer that maximal length.

Command for pair ends data + index file:

```
python shpulya.py -1 corrupted_R1_L001.fastq.gz -2 corrupted_R2_L001.fastq.gz -i corrupted_I1_L001.fastq.gz -o ouput_file_prefix --minlength 50 --maxlength 160 --indexlength 8
```

- **ouput_file_prefix** - prefix to which will be added _R1_L001.fastq, _R2_L001.fastq, and _I1_L001.fastq;
- **indexlength** - expected length of index sequenece (default value is 8), shpulya wikk drop all reads longer or shorter.

Most reads are lost if the index file is corrupted, then you can count PE reads separately as if there were no indexes, and the indexes are counted like this:

```
python fix_index_archive.py -i corrupted_I1_L001.fastq.gz -o corrupted_I1_L001.fastq --indexlength 8
```

But it should be kept in mind that then these data can only be used as paired reads, after the corresponding trimming of indexes from the beginning of each read.

## Known issues

Final Q-string can contain some unexpected symbols.

For large fastq files shpylya requeries some amount of memory, you can estimate it around 1/5 size of all processed files.

## Citation

## Copyright Notice

shpulya written by Aleksey Komissarov (ad3002@gmail.com)
Copyright (c) 2020 Aleksey Komissarov. 

This code is licensed under the same GNU General Public License v2
(or at your option, any later version).  See
http://www.gnu.org/licenses/gpl.html
