#!/usr/bin/python3

import os.path
import sys
import subprocess
import argparse

## Utility
def pr(*args):
  print("INFO:", *args)

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

def get_compiler_cmds():
  try:
    out = subprocess.run(['g++', '-v', '--help'], capture_output=True)
  except Exception:
    eprint('Error: g++ is not installed.')
    exit(1)

  cmd = ['g++']

  # If constexpr-*-limit flags are supported, set to the maximum number.
  if b'fconstexpr-loop-limit' in out.stdout:
    cmd.append('-fconstexpr-loop-limit={}'.format(2**31 - 1))
  if b'fconstexpr-ops-limit' in out.stdout:
    cmd.append('-fconstexpr-ops-limit={}'.format(2**31 - 1))

  return cmd

def redirect(cmd, dst):
  with open(dst, 'w') as f:
    try:
      print('{} > {}'.format(cmd, dst))
      if subprocess.call(cmd, stdout=f):
        exit(1)
    except Exception as e:
      eprint(e)
      exit(1)

def to_cpp_string(fname, target=''):
  pr('Convert the content of "{}" into C++ string literal'.format(fname))
  with open(fname, 'r') as f:
    s = f.read()
  s = 'R"(' + target + s + ')"\n'
  with open(fname, 'w') as f:
    f.write(s)

def replace_line(fname, var, new_str):
  pr('Change the value of "{}" in "{}"'.format(var, fname))
  with open(fname, 'r') as f:
    ls = f.readlines()
  with open(fname, 'w') as f:
    for l in ls:
      if var in l:
        f.write(new_str)
      else:
        f.write(l)

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
infile_txt = infile + ".txt"
fname, _ = os.path.splitext(infile)
bname = os.path.basename(fname)
eirfile = '{}/out/{}.eir'.format(DIR, bname)
outfile = args.o

if outfile == None:
  if target == 'x86':
    outfile = fname + '.exe'
  else:
    outfile = fname + target

compiler_cmds = get_compiler_cmds()

pr("Start compilation from \"{}\" to \"{}\"".format(infile, outfile))
pr("Convert C program into C++ string literal")
call('cp', infile, infile_txt)
to_cpp_string(infile_txt)
replace_line(config_hpp,
                 '#define EIGHT_CC_INPUT_FILE', '#define EIGHT_CC_INPUT_FILE  "{}"\n'.format(infile_txt))

pr("Compile C into ELVM IR")
args = compiler_cmds + ['-std=c++14', '-o', '{}/{}_eir.exe'.format(O_DIR, bname), cc_cpp]
call(*args)

if target == 'eir':
  redirect('{}/{}_eir.exe'.format(O_DIR, bname), outfile)
  exit(0)

redirect('{}/{}_eir.exe'.format(O_DIR, bname), eirfile)

pr("Convert ELVM IR into C++ string literal")
to_cpp_string(eirfile, target + '\n')
replace_line(config_hpp,
             '#define ELC_INPUT_FILE', '#define ELC_INPUT_FILE  "{}"\n'.format(eirfile))

pr("Compile ELVM IR into {} file".format(target))
args = compiler_cmds + ['-std=c++14', '-o', '{}/{}_out.exe'.format(O_DIR, bname), elc_cpp]
call(*args)
redirect('{}/{}_out.exe'.format(O_DIR, bname), outfile)

pr("\"{}\" was generated successfully".format(outfile))
