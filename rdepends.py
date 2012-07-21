#!/usr/bin/env python3
from __future__ import print_function
import os
#import sys
import threading
import collections
import termcolor
import argparse
import logging
from time import sleep

logging.basicConfig(level=logging.WARN, format='%(asctime)s - %(levelname)s - %(message)s')


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


class RdependsFinder:

    lock = threading.Lock()

    def __init__(self, recur_depth=1, max_workers=4):
        self._already_visited_packages = set()
        self._all_rdepends = set()
        self._pkg2rdep = collections.OrderedDict()
        self.recur_depth = recur_depth
        self.sema = threading.BoundedSemaphore(max_workers)

    @property
    def all_rdepends(self):
        while threading.active_count() > 1:
            sleep(1)
        return self._all_rdepends

    @property
    def pkg2rdep(self):
        while threading.active_count() > 1:
            sleep(1)
        return self._pkg2rdep

    def list_rdepends(self, package, recur=None):
        """print all the reverse depends of a package"""
        print
        if recur == None:
            recur = self.recur_depth
        logging.debug("locking...")
        RdependsFinder.lock.acquire()
        logging.debug(package)
        logging.debug("locked!")
        if package in self._already_visited_packages:
            logging.debug("releasing...")
            RdependsFinder.lock.release()
            logging.debug("released!")
            return
        else:
            self._already_visited_packages.add(package)
        logging.debug("releasing...")
        RdependsFinder.lock.release()
        logging.debug("released!")
        rdepends = os.popen("""LANGUAGE=en_US pacman -Sii {0} | grep -im"""
                """ 1 "required by" | sed -r 's/^.+://'""".format(package)).read().strip()
        if rdepends == "None":
            #logging.debug("releasing...")
            #RdependsFinder.lock.release()
            #logging.debug("released!")
            return
        rdepends = rdepends.split()
        logging.debug("locking...")
        RdependsFinder.lock.acquire()
        logging.debug("locked!")
        self._all_rdepends = self._all_rdepends.union(set(rdepends))
        self._pkg2rdep[package] = rdepends
        logging.debug("releasing...")
        RdependsFinder.lock.release()
        logging.debug("released!")
        if recur:
            for pac in rdepends:
                #self.sema.acquire()  # FIXME
                threading.Thread(None, target=self.list_rdepends, args=(pac, recur - 1)).start()
                #self.sema.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recursively list"
            " all rdepends of a package.")
    parser.add_argument("pname", metavar="<package name>", help="The name of the package.")
    parser.add_argument("--recdepth", "-r", help="The recursion depth"
            " (listing rdepends of rdepends)",
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
