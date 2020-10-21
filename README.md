# shpulya: recover your sequence data from corrupted achives

When transmitting gzipped data via ftp in text form, you can get corrupted data at the output. Ideally, check md5 after transfer, but this is sometimes forgotten. And after a lot of time someone can notice that the data is corrupted. Shpulya tries to recover the maximum amount of correct data from such data for further analysis.

Shpylya consists of three steps:

1) unpacking a damaged archive using gzrecover (https://github.com/arenn/gzrt);
2) removing the garbage from the unpacked data;
3) recovery of paired and corresponding index file, if there is such a file, for example, 10Х data for scRNA.

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
python shpulya.py -1 corrupted_R1_L001.fastq.gz -2 corrupted_R2_L001.fastq.gz -i -2 corrupted_I1_L001.fastq.gz -o ouput_file_prefix --minlength 50 --maxlength 160
```

- **ouput_file_prefix** - prefix to which will be added _R1_L001.fastq, _R2_L001.fastq, and _I1_L001.fastq.

## Known issues

Final Q-string can contain some unexpected symbols.

## Copyright Notice

shpulya written by Aleksey Komissarov (ad3002@gmail.com)
Copyright (c) 2020 Aleksey Komissarov. 

This code is licensed under the same GNU General Public License v2
(or at your option, any later version).  See
http://www.gnu.org/licenses/gpl.html
