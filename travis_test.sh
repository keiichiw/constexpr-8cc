#!/bin/bash -x

g++-6 --version

for fname in ./test/*.c
do
    base=`basename $fname`
    f=${base%.*}

    # Expected
    gcc ${fname} -o ./out/${f}_expected.exe
    ./out/${f}_expected.exe > ./out/${f}_expected.txt

    # Answer
    if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
        ./run_8cc.py py ${fname} -o ./out/${f}_cpp.py
        python ./out/${f}_cpp.py > ./out/${f}_cpp.txt
    else
        ./run_8cc.py x86 ${fname} -o ./out/${f}_cpp.exe
        chmod +x ./out/${f}_cpp.exe
        ./out/${f}_cpp.exe > ./out/${f}_cpp.txt
    fi

    (diff -u ./out/${f}_expected.txt ./out/${f}_cpp.txt > ./out/${f}.diff) || (cat ./out/${f}.diff; exit 1)
done
