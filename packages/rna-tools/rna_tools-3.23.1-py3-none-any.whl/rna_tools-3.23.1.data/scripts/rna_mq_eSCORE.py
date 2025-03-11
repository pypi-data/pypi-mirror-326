#!python
# -*- coding: utf-8 -*-
"""
Works on Ubuntu, on M1 a problem with libs.
"""
from __future__ import print_function
import argparse
from rna_tools.tools.mq.eSCORE.eSCORE import eSCORE 
import os

def get_parser():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

    #parser.add_argument('-', "--", help="", default="")

    parser.add_argument("-v", "--verbose",
                        action="store_true", help="be verbose")
    parser.add_argument("file", help="", default="", nargs='+')
    return parser


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    if list != type(args.file):
        args.file = [args.file]

    print('id,fn,escore')
    for i, f in enumerate(args.file):
        wrapper = eSCORE()
        result = wrapper.run(f, args.verbose)
        print(','.join([str(i + 1), os.path.basename(f), str(result)]))
