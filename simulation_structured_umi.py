#!/usr/bin/env python

import itertools
import sys
import random
import argparse

def parseArgs():
    parser = argparse.ArgumentParser( description = "Script for simulation of N structured UMIs and the number of overlaps \
                                                     within all N*N pairs of UMIs")
    parser.add_argument('-u', '--umi-structure', dest='umi_structure', help='structure of the UMI, e.g. NNNTTNNNCCNNNGGNNN. \
                                                                             Default = %(default)s', default = 'NNNNNNNNNNNN')
    parser.add_argument('-l', '--label', dest='label', help='Label of the simulation for output. Default is UMI structure')

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
    if args.label==None:
        args.label=args.umi_structure
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

def create_groups(sequence):
    groups=itertools.groupby(sequence)
    return([(label, len(list(group))) for label,group in groups])

def insert_batman(a,groups):
    b=''
    for label,n in groups:
        if label=='N':
            b+=a[0:n]
            a=a[n:]
        #elif label =='S':
        #    b+= ''.join([random.choice(['G','C']) for _ in range(n)])
        #elif label=='W':
        #    b+=''.join([random.choice(['A','T']) for _ in range(n)])
        else:
            b+=label*n
    return(b)

def main(args):
    label=args.label
    umi_pattern=args.umi_structure
    #pattern='NNNNAAANNANNAAANNNN'
    #pattern2='NNANNNNANNNNANN'
    groups=create_groups(umi_pattern)
    window_size = int(args.window_size)
    n_samples = args.n_samples
    gc_count_cutoff = int(args.gc_cutoff)
    output_file = args.output_file
    
    bases=['A','C','T', 'G']
    ul=umi_pattern.count('N')
    l = [list(bases)]*ul
    prods = itertools.product(*l)
    prodlist=["".join(x) for x in prods]
    prodssample=random.sample(prodlist,n_samples)
    n=0
    collisions=0
    gc_pass=0
    prodssample_new=[]
    for s in prodssample:
        s=insert_batman(s,groups)
        prodssample_new.append(s)

    for i,j in itertools.combinations(prodssample_new, 2):
        n+=1
        irev=reverse_complement(i)
        jrev=reverse_complement(j)
        if not i==j:
            interaction,gc_count=check_interactions(i,jrev, window_size)
            if interaction > 0:
                collisions+=1
                if gc_count >= gc_count_cutoff:
                        gc_pass+=1
                next
            else:
                interaction2, gc_count2=check_interactions(j,irev, window_size)
                if interaction2 > 0:
                    collisions+=1
                    if gc_count2 >= gc_count_cutoff:
                        gc_pass+=1
                    next
    if output_file=='-':
        f=sys.stdout
    else: 
        f=open(output_file,'a')
    f.write('\t'.join([label, str(n), str(collisions), str(gc_pass),str(1.0*collisions/n), str(1.0*gc_pass/n)])+'\n')
    if not output_file=='-':
        f.close()


if __name__=='__main__':
    args=parseArgs()
    main(args)
