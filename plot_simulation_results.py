#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

def parseArgs():
    parser = argparse.ArgumentParser( description = "Script for plotting simulation results of N structured UMIs and the number of overlaps \
                                                     within all N*N pairs of UMIs")
    parser.add_argument('-i' '--input', dest='results_file', help='Path to txt file generated from the simulation script, data to plot')
    parser.add_argument('-s','--save', dest='save_plot', action='store_true', help='Include this flag if the plot should be saved in a file')
    parser.add_argument('-p','--plot-file', dest='plot_filename', help='plot filename to save the plot. Default = %(default)s', default='output.png')
    args=parser.parse_args(sys.argv[1:])
    return(args)

def main(results_file, save_plot,  plot_file):
    labels=[]
    results={}
    results['interactions']=[]
    results['gc']=[]
    with open(results_file) as f:
        for line in f:
            line=line.rstrip()
            parts=line.split('\t')
            label=parts[0]
            percentage=float(parts[-2])*100.0
            gc_percentage=float(parts[-1])*100.0
            labels.append(label)
            results['interactions'].append(percentage)
            results['gc'].append(gc_percentage)

    x = np.arange(len(labels))  # the label locations
    width = 0.25
    multiplier = 0
    fig, ax = plt.subplots(layout='constrained')
    for typex,value in results.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, value, width, label=typex)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    ax.set_ylabel('Simulated UMI interactions (%)')
    ax.set_title('Simulation results')
    if len(labels)>3:
        ax.set_xticks(x + width, labels, rotation=30, ha='right')
    else:
        ax.set_xticks(x + width, labels)
    ax.legend(['Simulated interactions','GC-rich subsequences'],loc='upper left')
    ax.set_ylim(0, np.max(results['interactions'])+5)
    plt.show()
    if save_plot:
        plt.savefig(plot_file)

if __name__=='__main__':
    args=parseArgs()
    main(args.results_file,args.save_plot,args.plot_filename)
