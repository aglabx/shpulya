# shpulya: recover your sequence data from corrupted achives

When transmitting gzipped data via ftp in text form, you can get corrupted data at the output. Ideally, check md5 after transfer, but this is sometimes forgotten. And after a lot of time someone can notice that the data is corrupted. Shpulya tries to recover the maximum amount of correct data from such data for further analysis.

Shpylya consists of three steps:

1) unpacking a damaged archive using gzrecover (https://github.com/arenn/gzrt);
2) removing the garbage from the unpacked data;
3) recovery of paired and corresponding index file, if there is such a file, for example, 10Х data for scRNA.
