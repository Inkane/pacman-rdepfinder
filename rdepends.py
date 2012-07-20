#!/usr/bin/env python2
from __future__ import print_function
import os
#import sys
#import threading
import multiprocessing
import collections
import termcolor
import argparse

pool = multiprocessing.Pool()


def pprint_list(l):
    charlen = 0
    print("\t", end="")
    for word in sorted(l):
        if charlen > 50:
            charlen = 0
            print("\t\n", end="\t")
        charlen += len(word) + 1
        print(word, end="\t")
    print()


class RdependsFinder(object):

    def __init__(self, recur_depth=1):
        self.already_visited_packages = set()
        self.all_rdepends = set()
        self.pkg2rdep = collections.OrderedDict()
        self.recur_depth = recur_depth

    def list_rdepends(self, package, recur=None):
        """print all the reverse depends of a package"""
        if recur == None:
            recur = self.recur_depth
        if package in self.already_visited_packages:
            return
        else:
            self.already_visited_packages.add(package)
        rdepends = os.popen("""LANGUAGE=en_US pacman -Sii {0} | grep -im"""
                """ 1 "required by" | sed -r 's/^.+://'""".format(package)).read().strip()
        if rdepends == "None":
            return
        rdepends = rdepends.split()
        self.all_rdepends = self.all_rdepends.union(set(rdepends))
        self.pkg2rdep[package] = rdepends
        if self.recur_depth:
            pool. rap(lambda x: self.list_rdepends(*x),
                zip(rdepends, len(rdepends) * [recur - 1]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively list"
            " all rdepends of a package.")
    parser.add_argument("pname", metavar="<package name>", help="The name of the package.")
    parser.add_argument("--recdepth", "-r", help="The recursion depth",
           type=int, default=0)
    args = parser.parse_args()
    rfinder = RdependsFinder(args.recdepth)
    rfinder.list_rdepends(args.pname)
    for k in rfinder.pkg2rdep:
        print(termcolor.colored(">> ", color="blue"), "rdepends of {} are: ".format(k))
        pprint_list(rfinder.pkg2rdep[k])
    print()
    print(termcolor.colored(">> ", color="blue"), "total number of rdepends "
       "checked (recursion level = {}):".format(rfinder.recur_depth), end="\t")
    print(len(rfinder.all_rdepends))
    print(termcolor.colored(">> ", color="blue"), "All rdepends:")
    pprint_list(rfinder.all_rdepends)
