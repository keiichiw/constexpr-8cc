#!/bin/bash -eux

sudo add-apt-repository --yes ppa:ubuntu-toolchain-r/test
sudo apt-get update
sudo apt-get install g++-6
