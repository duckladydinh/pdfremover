#!/usr/bin/python3

######################################
# Author: Lam Gia Thuan (duckladydinh)
# Time: October 11, 2018
# Place: Frankfurt, Germany
######################################

import subprocess
import argparse
import shutil
import os
import re
import shlex


def usage():
    return '''
####################################################################################
    Please follow this syntax:
        ./pdfremover.py -f INPUT.PDF [-o OUTPUT[.PDF]] -s STR1 STR2 ... STRn [-r]
    , in which:
        -f: 1 PDF Input File
        -o: 1 PDF Output File Name (without/without extension)
        -s: the strings to be removed
        -r: should we use regular expression?
    Please avoid strings that contain special character like space... since, for example,
    Why? Since, for example, the number of visible spaces may be a lot more than it looks 
#####################################################################################

Example:
./pdfremover.py -f APT-NET.pdf -s "Free ebooks ==>   www.Ebook777.com" "www.Ebook777.com"

           '''


def process(args: argparse.Namespace):
    if os.path.isfile(args.file):
        file_pattern = re.compile(pattern='^.+\.pdf$', flags=re.IGNORECASE)
        if not file_pattern.match(args.file):
            print('Warning: Input file does not end in *.pdf')
        if args.output:
            if not file_pattern.match(args.output):
                print('Warning: Output file does not end in *.pdf [Automatically added]')
                args.output += '.pdf'
        else:
            args.output = 'edited_' + args.file

        try:
            subprocess.check_call(shlex.split("qpdf --qdf --object-streams=disable " + args.file + " " + args.output))
        except subprocess.CalledProcessError as e:
            print("Possible problems in running QPDF")

        with open(args.output, 'rb') as input:
            content = input.read()

        if not args.regex:
            patterns = list(map(re.escape, args.strings))
        else:
            patterns = args.strings

        pattern = '(' + '|'.join(patterns) + ')'
        content = re.sub(pattern=str.encode(pattern), repl=b'', string=content)

        with open(args.output, 'wb') as output:
            output.write(content)


if __name__ == '__main__':
    if shutil.which('qpdf'):
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument('-f', '--file')
        parser.add_argument('-o', '--output')
        parser.add_argument('-s', '--strings', nargs='*')
        parser.add_argument('-h', '--help', action='store_true')
        parser.add_argument('-r', '--regex', action='store_true')

        args = parser.parse_args()
        if args.help:
            print(usage)
        elif args.file and args.strings:
            process(args)
        else:
            print('Insufficient arguments. ' + usage())
    else:
        print('Please install QPDF')