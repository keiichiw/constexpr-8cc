#!/bin/bash -eux

if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew update
    brew tap homebrew/versions
    brew install gcc6
fi

if [[ "$TRAVIS_OS_NAME" == "linux" ]]; then
    sudo add-apt-repository --yes ppa:ubuntu-toolchain-r/test
    sudo apt-get update
    sudo apt-get install g++-6
fi
