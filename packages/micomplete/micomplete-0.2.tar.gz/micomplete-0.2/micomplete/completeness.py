# Copyright (c) Eric Hugoson.
# See LICENSE for details.

"""
Module investigates the completeness of a given genome with respect to a given 
set of HMM makers, in so far as it runs HMMer and parses the output. 


"""

from __future__ import print_function, division
from distutils import spawn
from collections import defaultdict
from termcolor import cprint
import sys
import math
import subprocess
import re
import os


class calcCompleteness():
    def __init__(self, fasta, baseName, hmms, evalue=1e-10, weights=None, 
            hlist=False, linkage=False, debug=False):
        self.baseName = baseName
        self.evalue = "-E %s" % (str(evalue))
        self.tblout = "%s.tblout" % (self.baseName)
        self.hmms = hmms
        self.fasta = fasta
        self.linkage = linkage
        self.weights = weights
        self.hlist = hlist
        self.debug = debug
        print("Starting completeness for " + fasta, file=sys.stderr)
        self.hmmNames = set({})
        with open(self.hmms) as hmmfile:
            for line in hmmfile:
                if re.search('^NAME', line):
                    name = line.split(' ')
                    self.hmmNames.add(name[2].strip())
        if self.debug:
            print(self.hmmNames)

    def hmm_search(self):
        """
        Runs hmmsearch using the supplied .hmm file, and specified evalue.
        Produces an output table from hmmsearch, function returns its name.
        """
        hmmsearch = ["hmmsearch", self.evalue, "--tblout", self.tblout,
                self.hmms, self.fasta]
        if self.debug:
            print(hmmsearch)
        if sys.version_info > (3, 4):
            compProc = subprocess.run(hmmsearch, stdout=subprocess.DEVNULL)
            errcode = compProc.returncode
        else:
            errcode = subprocess.call(hmmsearch, stdout=open(os.devnull, 'wb'),
                    stderr=subprocess.STDOUT)
        if errcode > 0:
            cprint("Warning:", 'red', end=' ', file=sys.stderr)
            print("Error thrown by HMMER, is %s empty?" % self.fasta, file=sys.stderr)
        return self.tblout, errcode

    def get_completeness(self):
        """
        Reads the out table of hmmer to find which hmms are present, and
        which are duplicated. Duplicates are only considered duplicates if
        the evalue of the secondary hit is within the squareroot of the best 
        hit.

        Returns: Dict of all hmms found with evalues for best and possible 
        deulicates, list of hmms with duplicates, and names of all hmms 
        which were searched for.
        """
        tblout, errcode = self.hmm_search()
        if errcode > 0:
            return 0, 0, 0
        self.hmmMatches = defaultdict(list)
        self.seenHmms = set()
        # gather gene name and evalue in dict by key[hmm]
        for hmm in self.hmmNames:
            with open(self.tblout) as hmmTable:
                for foundHmm in hmmTable:
                    if re.match("#$", foundHmm):
                        break
                    if re.search("^" + hmm + "$", foundHmm.split()[2]):
                        #slice notation gathers column 0 and 4
                        self.hmmMatches[hmm].append(foundHmm.split()[0:5:4])
                        self.seenHmms.add(hmm)
        if self.debug:
            print(self.hmmMatches)
            print(len(self.hmmMatches))
        self.filledHmms = defaultdict(list)
        # section can be expanded to check for unique gene matches
        for hmm, geneMatches in self.hmmMatches.items():
            # sort by lowest eval to fill lowest first
            for gene in sorted(geneMatches, key=lambda ev: float(ev[1])):
                if hmm not in self.filledHmms:
                    self.filledHmms[hmm].append(gene)
                elif float(gene[1]) < pow(float(self.filledHmms[hmm][0][1]), 1/2):
                    self.filledHmms[hmm].append(gene)
        self.dupHmms = [ hmm for hmm, genes in self.filledHmms.items()
                if len(genes) > 1 ]
        if self.hlist and not self.linkage:
            self.print_hmm_lists()
        return self.filledHmms, self.dupHmms, self.hmmNames

    def quantify_completeness(self):
        """
        Function returns the number of found markers, duplicated markers, and 
        total number of markers.
        """
        filledHmms, dupHmms, hmmNames = self.get_completeness()
        try:
            numFoundHmms = len(filledHmms)
            numHmms = len(hmmNames)
        except TypeError:
            numFoundHmms = 0
            numTotalHmms = 0
            numHmms = 0
            return numFoundHmms, numTotalHmms, numHmms
        allDupHmms = [ len(genes) for hmm, genes in self.filledHmms.items() ]
        numTotalHmms = sum(allDupHmms)
        return numFoundHmms, numTotalHmms, numHmms

    def print_hmm_lists(self):
        """Prints the contents of found, duplicate and and not found markers"""
        hlistName = "%s_hmms.list" % (self.baseName)
        with open(hlistName, 'w+') as seenList:
            for eachHmm in self.seenHmms:
                seenList.write("%s\n" % eachHmm)
        dupListName = "%s_hmms_duplicate.list" % (self.baseName)
        with open(dupListName, 'w+') as dupList:
            for eachDup in self.dupHmms:
                dupList.write("%s\n" % eachDup)
        missingListName = "%s_hmms_missing.list" % (self.baseName)
        with open(missingListName, 'w+') as missingList:
            for hmm in self.hmmNames:
                if hmm not in self.seenHmms:
                    missingList.write("%s\n" % hmm)
        return hlistName

    def attribute_weights(self, numHmms):
        """Using the markers found and duplicates from get_completeness(), and
        provided weights, adds up weight of present and duplicate markers"""
        weightedComplete = 0
        weightedRedun = 0
        for hmm in self.seenHmms:
            with open(self.weights, 'r') as weights:
                for eachWeight in weights:
                    if re.match(hmm + "\s", eachWeight):
                        weightedComplete += float(eachWeight.split()[1])
        for hmm in self.dupHmms:
            with open(self.weights, 'r') as weights:
                for eachWeights in weights:
                    if re.match(hmm + "\t", eachWeights):
                        weightedRedun += float(eachWeights.split()[1])
        weightedRedun = round(((weightedRedun + weightedComplete) /
            weightedComplete), 3)
        weightedComplete = round(weightedComplete, 3)
        return weightedComplete, weightedRedun


