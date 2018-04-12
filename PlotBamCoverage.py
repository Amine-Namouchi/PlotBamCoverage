#!/usr/bin/env python

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but without
# any warranty; without even the implied warranty of merchantability or fitness
# for a particular purpose. See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

__licence__ = 'GPLv3'
__author__ = 'Amine Namouchi'
__author_email__ = 'bioinfosuite@gmail.com'

info =  __licence__ + " licence | " + __author__ + " | " + __author_email__

import sys
if sys.version_info[0] < 3:
    print('Python 3 is needed to run this script!')
    sys.exit(0)

from itertools import islice
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import subprocess
import argparse
import statistics
import tempfile


parser = argparse.ArgumentParser(description="Plot coverage from sorted bam file",epilog=info)
parser.add_argument('-i', dest='sortedbam', required=True, help='provide a sorted bam')
parser.add_argument('-w', dest='window_size', required=False, default=100, type=int, help='provide a sliding window size')
parser.add_argument('-c', dest='ID', required=True, help='provide a locus identifier (Chromosome name, plasmid name, contig) as indicated in your bam file (check your bam file header using the command "samtools view -H bamfile")')
parser.add_argument('-f', dest='formatfile', required=False, default='png', help='possible image output formats: eps, jpg, pdf, png')

args= parser.parse_args()
if args.window_size < 100:
    sys.exit('Please specify a window size equal or higher than 100 bp')

print ('please wait... ' + args.sortedbam + ' is being processed')

#First, run the command samtools depth and write the output on a temporary file. samtools depth -aa will returns the depth at each position.

tempF = tempfile.TemporaryFile()
cmd = ['samtools','depth','-aa','-r', args.ID, args.sortedbam]
proc = subprocess.Popen(cmd, stdout=tempF, stderr=subprocess.STDOUT)
proc.wait()
tempF.seek(0)

#Second, go through the temporary file and read N lines at the same time (N = sliding window) and compute the mean depth.

i = 0
DepthValues = []
coordiantesValues = []
AllDepthValues = []
for data in tempF:
    DepthValues.append(statistics.mean([int(x.strip().split()[-1]) for x in islice(tempF, args.window_size)]))
    coordiantesValues.append (i+args.window_size)
    i+=args.window_size

#Finally, create a pandas DataFrame (coordiantesValues,DepthValues) and plot the data.
#The plot is as follow:
#on the left a histogram with x axis as depth of coverage and y axis the number of bins (number of regions with a length equal to the specified window size)
#on the right a scatter plot showing the depth of coverage through the specified locus with the option -c

sns.set_style("ticks")
fig, axes= plt.subplots(figsize=(15,5), nrows=1, ncols=2, gridspec_kw = {'width_ratios':[1, 3]}, dpi=300)
df = pd.DataFrame(list(zip(coordiantesValues,DepthValues)),coordiantesValues,['coordinates','depth'])

df['depth'].plot(kind='hist',ax=axes[0], color='grey')
axes[0].set_xlabel('Depth of coverage')
axes[0].set_ylabel('Number of bins')

df.plot(kind = 'scatter', x='coordinates', y='depth', c='depth', alpha = .5, ax=axes[1], colormap='copper', colorbar=False)
axes[1].set_xlim((0,coordiantesValues[-1]+args.window_size))
axes[1].set_ylim(bottom=0)
axes[1].set_xlabel(args.ID + ' coordinates')
axes[1].set_ylabel('Depth of coverage')

plt.tight_layout()
plt.savefig(args.sortedbam.split('.')[0]+'_'+args.ID+'.'+args.formatfile)
tempF.close()
