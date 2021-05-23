#!/bin/bash -x

g++ --version

for fname in ./test/*.c
do
    base=`basename $fname`
    f=${base%.*}

    # Expected
    gcc ${fname} -o ./out/${f}_expected.exe
    ./out/${f}_expected.exe > ./out/${f}_expected.txt

    # Answer
    ./run_8cc.py x86 ${fname} -o ./out/${f}_cpp.exe
    chmod +x ./out/${f}_cpp.exe
    ./out/${f}_cpp.exe > ./out/${f}_cpp.txt

    (diff -u ./out/${f}_expected.txt ./out/${f}_cpp.txt > ./out/${f}.diff) || (cat ./out/${f}.diff; exit 1)
done
