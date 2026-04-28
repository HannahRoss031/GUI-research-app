#!/bin/python
###
#   name    | mary lauren benton
#   created | 2017
#   updated | 2018.10.09
#           | 2018.10.11
#           | 2018.10.29
#           | 2019.02.01
#           | 2019.04.08
#           | 2019.06.10
#           | 2019.11.05
#           | 2021.02.24
#           | 2021.05.26
#           | 2025.05.28
#
#   depends on:
#       BEDtools v2.23.0-20 via pybedtools
#       taako : /storage/data/blacklist/[species]-blacklist.bed
#       ACCRE : ml Anaconda3 GCC MySQL-client
###

import os
import pickle
import sys, traceback
#import argparse
import datetime
import numpy as np
from functools import partial
from multiprocessing import Pool
import pybedtools
from pybedtools import BedTool
from pybedtools.helpers import BEDToolsError, cleanup, get_tempdir, set_tempdir

# FIXME: have to run directly from terminal!
#  source ~/bioenv/bin/activate
#  python enrichment.py file1.bed file2.bed -s hg38

###
#   functions
###
def loadConstants(species, custom=''):
    if custom is not None:
        return custom
    return {'hg19': "/storage/data/blacklist/hg19_blacklist_gap.bed",
            'hg38': "/storage/data/blacklist/hg38_blacklist_gap.bed",
            'mm10': "/storage/data/blacklist/mm10_blacklist_gap.bed",
            'dm3' : "/storage/data/blacklist/dm3-blacklist.bed",
            'dm6' : "/storage/data/blacklist/dm6-blacklist.bed",
            'sacCer3' : None
            }[species]


def calculateObserved(annotation, test, percent_overlap, elementwise, hapblock, strand):
    obs_sum = 0

    if elementwise:
        obs_sum = annotation.intersect(test, u=True, s=strand, f=percent_overlap[0], F=percent_overlap[1]).count()
    else:
        obs_intersect = annotation.intersect(test, wo=True, s=strand, f=percent_overlap[0], F=percent_overlap[1])

        if hapblock:
            obs_sum = len(set(x[-2] for x in obs_intersect))
        else:
            for line in obs_intersect:
                obs_sum += int(line[-1])

    return obs_sum


def calculateExpected(annotation, test, percent_overlap, elementwise, hapblock, species, custom, strand, iterations, iteration_index):
    BLACKLIST = loadConstants(species, custom)
    exp_sum = 0


    try:
        anno_bt = BedTool(annotation) # additions?
        test_bt = BedTool(test)
        if BLACKLIST is not None:
            rand_file = anno_bt.shuffle(genome=species, excl=BLACKLIST, chrom=True, noOverlapping=True)
        else:
            rand_file = anno_bt.shuffle(genome=species, chrom=True, noOverlapping=True)

        if elementwise:
            exp_sum = rand_file.intersect(test_bt, u=True, s=strand, f=percent_overlap[0], F=percent_overlap[1]).count()
        else:
            exp_intersect = rand_file.intersect(test_bt, s=strand, wo=True, f=percent_overlap[0], F=percent_overlap[1])

            if hapblock:
                exp_sum = len(set(x[-2] for x in exp_intersect))
            else:
                for line in exp_intersect:
                    exp_sum += int(line[-1])
    except BEDToolsError as e:
        print("Worker error:", repr(e))
        exp_sum = -999

    return exp_sum


def calculateEmpiricalP(obs, exp_sum_list):
    mu = np.mean(exp_sum_list)
    sigma = np.std(exp_sum_list)
    dist_from_mu = [exp - mu for exp in exp_sum_list]
    p_sum = sum(1 for exp_dist in dist_from_mu if abs(exp_dist) >= abs(obs - mu))

    # add pseudocount only to avoid divide by 0 errors
    if mu == 0:
        fold_change = (obs + 1.0) / (mu + 1.0)
    else:
        fold_change = obs / mu

    p_val = (p_sum + 1.0) / (len(exp_sum_list) + 1.0)

    return "%d\t%.3f\t%.3f\t%.3f\t%.3f" % (obs, mu, sigma, fold_change, p_val)


def main(annotation, test, pAnno, pTest, elementwise, hapblock, species, blackListFile, strand, threads, iterations):

    print("-------------------------NEW RUN-------------------------")

    # print header
    print('python {:s} {:s}'.format(' '.join(sys.argv), str(datetime.datetime.now())[:20]))
    print('Observed\tExpected\tStdDev\tFoldChange\tp-value')

    # run initial intersection and save
    obs_sum = calculateObserved(BedTool(annotation), BedTool(test), (pAnno, pTest),
                                elementwise, hapblock, strand)

    # create pool and run simulations in parallel
    #pool = Pool(threads)
    pool = Pool(int(threads) if threads and int(threads) > 0 else 1)
   # partial_calcExp = partial(calculateExpected, BedTool(annotation), BedTool(test), (pAnno, pTest),
   #                           elementwise, hapblock, species, blackListFile, strand)

    cs = pybedtools.chromsizes(species) # to account for dictionary of species in pybedtools

    partial_calcExp = partial(
        calculateExpected,
        annotation, test,
        (pAnno, pTest),
        elementwise,
        hapblock,
        cs,
        blackListFile,
        strand,
        iterations
        # iteration_index is supplied by pool.map
    )

    exp_sum_list = pool.map(partial_calcExp, [i for i in range(iterations)])

    # wait for results to finish before calculating p-value
    pool.close()
    pool.join()

    # remove iterations that throw bedtools exceptions
    final_exp_sum_list = [x for x in exp_sum_list if x >= 0]
    exceptions = exp_sum_list.count(-999)
    #print("Exceptions: {0:d}".format(exceptions))
    # calculate empirical p value
    if exceptions / iterations <= .1:
        result = (calculateEmpiricalP(obs_sum, final_exp_sum_list))
        #result2 = (f'iterations not completed: {exceptions}', file=sys.stderr)
        result2 = f'iterations not completed: {exceptions}'
    else:
        print(f'iterations not completed: {exceptions}\nresulted in nonzero exit status', file=sys.stderr)
        cleanup()
        sys.exit(1)

    if test is not None:
        with open(test, "w") as count_file:
            count_file.write('{}\n{}\n'.format(obs_sum, '\t'.join(map(str, exp_sum_list))))

    # clean up any pybedtools tmp files
    cleanup()

    return result, result2

if __name__ == "__main__":
    pass
