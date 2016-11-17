#!/bin/bash -x

for fname in ./test/*.c
do
    base=`basename $fname`
    f=${base%.*}

    # Expected
    sed "1d" ./test/putchar.c | sed "s/)\"//" > ./out/${f}_raw.c
    gcc ./out/${f}_raw.c -o ./out/${f}_raw.exe
    ./out/${f}_raw.exe > ./out/${f}_raw.txt

    # Answer
    ./run_8cc.py x86 ${fname} -o ./out/${f}_cpp.exe
    chmod +x ./out/${f}_cpp.exe
    ./out/${f}_cpp.exe > ./out/${f}_cpp.txt

    (diff -u ./out/${f}_raw.txt ./out/${f}_cpp.txt > ./out/${f}.diff) || (cat ./out/${f}.diff; exit 1)
done
