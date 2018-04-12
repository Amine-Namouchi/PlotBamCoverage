## 1. PlotBamCoverage.py

when you ran this script with the -h option, it will print this help message:
```
python PlotBamCoverage.py -h

usage: PlotBamCoverage.py [-h] -i SORTEDBAM [-w WINDOW_SIZE] -c ID
                          [-f FORMATFILE]

Plot coverage from sorted bam file

optional arguments:
  -h, --help      show this help message and exit
  -i SORTEDBAM    provide a sorted bam
  -w WINDOW_SIZE  provide a sliding window size
  -c ID           provide a locus identifier (Chromosome name, plasmid
                  name, contig) as indicated in your bam file (check your bam file
                  header using the command "samtools view -H bamfile")
  -f FORMATFILE   possible image output formats: eps, jpg, pdf, png
```

You can ran _PlotBamCoverage.py_ for example as follow:
```
python PlotBamCoverage.py -w 1000 -c Locus_ID -i sortedBamFile.bam
```
_PlotBamCoverage.py_ will generate a plot showing the mean coverage through the entire locus that the user specified on each window size of 1000 bp.
