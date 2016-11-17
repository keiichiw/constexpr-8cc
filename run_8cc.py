#!/usr/bin/python3

import os.path
import sys
import subprocess
import argparse

## Utility
def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def call(*cmd):
  try:
    print(subprocess.list2cmdline(cmd))
    if subprocess.call(cmd):
      exit(1)
  except Exception as e:
    eprint(e)
    exit(1)

def redirect(cmd, dst):
  with open(dst, 'w') as f:
    try:
      print('{} > {}'.format(cmd, dst))
      if subprocess.call(cmd, stdout=f):
        exit(1)
    except Exception as e:
      eprint(e)
      exit(1)

def escape(s):
  return s.replace('/', '\/')

## Argument Parser
DIR = os.path.dirname(__file__)
TARGET_LIST = ['eir', 'rb', 'py', 'js', 'el',
               'vim', 'tex', 'cl', 'sh', 'java',
               'c', 'cpp', 'x86', 'i', 'ws',
               'bef', 'bf', 'pietasm', 'piet', 'unl']

argparser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                    description='Example:\n$ {}/%(prog)s x86 ./test/putchar.c -o ./putchar.exe'.format(DIR))
argparser.add_argument('target',
                       choices=TARGET_LIST,
                       metavar='target',
                       help='target language of compilation\n[%(choices)s]')
argparser.add_argument('infile',
                       metavar='file',
                       help='input C file')
argparser.add_argument('-o',
                       metavar='<file>',
                       help='set output file name')

## Main
O_DIR = "{}/out".format(DIR)
config_hpp = '{}/config.hpp'.format(DIR)
cc_cpp = '{}/8cc.cpp'.format(DIR)
elc_cpp = '{}/elc.cpp'.format(DIR)

args = argparser.parse_args()

target = args.target
infile = args.infile
fname, _ = os.path.splitext(infile)
bname = os.path.basename(fname)
eirfile = '{}/out/{}.eir'.format(DIR, bname)
outfile = args.o

if outfile == None:
  if target == 'x86':
    outfile = fname + '.exe'
  else:
    outfile = fname + target

call('sed', '-i', 's/EIGHT_CC_INPUT_FILE .*/EIGHT_CC_INPUT_FILE   \\"{}\\"/'.format(escape(infile)), config_hpp)
call('g++', '-std=c++14', '-o', '{}/{}_eir.exe'.format(O_DIR, bname), cc_cpp)

if target == 'eir':
  redirect('{}/{}_eir.exe'.format(O_DIR, bname), outfile)
  exit(0)

redirect('{}/{}_eir.exe'.format(O_DIR, bname), eirfile)

call('sed', '-i', '1iR\\"({}'.format(target),  eirfile)
call('sed', '-i', '$a )\"',  eirfile)
call('sed', '-i', 's/ELC_INPUT_FILE .*/ELC_INPUT_FILE   \\\"{}\\\"/'.format(escape(eirfile)),  config_hpp)

call('g++', '-std=c++14', '-o', '{}/{}_out.exe'.format(O_DIR, bname), elc_cpp)
redirect('{}/{}_out.exe'.format(O_DIR, bname), outfile)
