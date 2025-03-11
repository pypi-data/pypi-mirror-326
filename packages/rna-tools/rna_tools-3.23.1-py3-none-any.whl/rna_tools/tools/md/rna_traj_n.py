#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function
import argparse
from icecream import ic
import sys
ic.configureOutput(outputFunction=lambda *a: print(*a, file=sys.stderr))
ic.configureOutput(prefix='> ')


def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-s', "--start", help="inclusive", default=1, type=int)
    parser.add_argument('-e', "--end", help="inclusive", type=int)
    parser.add_argument("--rm-htm",
                        action="store_true", help="remove HETATM")
    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument("file", help="", default="") # nargs='+')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if list != type(args.file):
        args.file = [args.file]

    for f in args.file:
        print(f)

        npdb = ''
        c = 0

        nmodels = 0
        for l in open(f):
            if l.startswith('MODEL'):
                nmodels += 1
        print(nmodels)
