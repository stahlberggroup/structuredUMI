#!/usr/bin/env python

import itertools
import sys
import random
import argparse

def parseArgs():
    parser = argparse.ArgumentParser( description = "Script for simulation of N structured UMIs and the number of overlaps \
                                                     within all N*N pairs of UMIs")
    parser.add_argument('-b', '--barcode-design', dest='barcode_design', help='Barcode design I, II or III (See manuscript, fig 1). \
                                                                             Default = %(default)s', default = 'I')
    parser.add_argument('-n', '--n-samples', dest='n_samples', help='Number of sampled (simulated) UMIs. Default = %(default)s',
                         default=1000)
    parser.add_argument('-w', '--window_size', dest='window_size', help='The window size used for overlap, \
                                                                        i.e. minimum required overlap. Default = %(default)s',
                                                                        default = 6)
    parser.add_argument('-gc', '--gc-cutoff', dest='gc_cutoff', help='Number of GC bases within the window to be reported \
                                                                      as a gc-rich sub-sequence. Default = %(default)s',
                                                                      default = 3)
    parser.add_argument('-o','--output-file', dest='output_file', help="Output file. Note that the output file can be appended \
                                                                        with new simulations if an existing file is specified. \
                                                                        Default is to write to stdout ('-').", default='-')

    args=parser.parse_args(sys.argv[1:])
    return(args)

def reverse_complement(sequence):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    rc = "".join(complement.get(base, base) for base in reversed(sequence))
    return(rc)

def gc_count(substr):
    return(substr.count('G')+substr.count('C'))

def check_interactions(a,b,window_size):
    interaction=False
    gc=0
    for k in range(len(a)-window_size+1):
        if b.find(a[k:k+window_size])>-1:
            interaction=True
            gc=gc_count(a[k:k+window_size])
            break
    return(interaction,gc)

def generate_combinations_list(umi):
    bases = ['A','C','T', 'G']
    sbases = ['G','C']
    wbases = ['A','T']
    l=[]
    for s in umi:
        if s=='N':
            l = l + [list(bases)]
        elif s=='S':
            l = l + [list(sbases)]
        elif s=='W':
            l = l + [list(wbases)]
        else:
            l = l + [list(s)]
    return(l)

def main(args):
    window_size = int(args.window_size)
    gc_count_cutoff = int(args.gc_cutoff)
    n_samples = int(args.n_samples)
    barcode_design = args.barcode_design
    output_file = args.output_file
    if barcode_design=='I': #NNNNNWWNNNNN
        umi="NNNNNWWNNNNN"
    elif barcode_design=='II': #SSWSWWWSWWSWSS
        umi="SSWSWWWSWWSWSS"
    elif barcode_design=='III' or barcode_design=='IV': #SWSSWWWSSWSWWWSWWSWSS
        umi="SWSSWWWSSWSWWWSWWSWSS"
    elif barcode_design=='V': # SWSSWSSWWWSSWSWWWSWWSWSS
        umi="SWSSWSSWWWSSWSWWWSWWSWSS"
    elif barcode_design=='VI':
        umi="SWSWSWSWSWSWSWSWSWSWSWSW"
    elif barcode_design=='VII':
        umi="SSWWSSWWSSWWSSWWSSWWSSWW"
    else:
        print('Please choose a barcode design between I,II or III, IV, V, VI, VII')
        sys.exit(1)
    l=generate_combinations_list(umi)
    prods = itertools.product(*l)
    prodlist=["".join(x) for x in prods]
    prodssample=random.sample(prodlist,n_samples)
    n=0
    collisions=0
    gc_pass=0
    for i,j in itertools.combinations(prodssample,2):
        n+=1
        i=''.join(i)
        j=''.join(j)
        irev=reverse_complement(i)
        jrev=reverse_complement(j)
        if not i==j:
            interaction,gc_count=check_interactions(i,jrev,window_size)
            if interaction>0:
                collisions+=1
                if gc_count >= gc_count_cutoff:
                    gc_pass+=1    
                next
            else:
                interaction2, gc_count2 = check_interactions(j,irev,window_size)
                if interaction2>0:
                    collisions+=1
                    if gc_count2 >= gc_count_cutoff:
                        gc_pass+=1
                    next
    if output_file=='-':
        f=sys.stdout
    else:
        f=open(output_file,'a')
    f.write('\t'.join( [barcode_design, str(n), str(collisions), str(gc_pass), str(1.0*collisions/n), str(1.0*gc_pass/n)]) + '\n' )

if __name__=='__main__':
    args=parseArgs()
    main(args)
