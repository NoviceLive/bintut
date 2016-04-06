#!/usr/bin/env bash


./bintut.py plain -b0.1
./bintut.py plain -b0.1 -6

./bintut.py nop-slide -b0.1
./bintut.py nop-slide -b0.1 -6

./bintut.py jmp-esp -b0.1
./bintut.py jmp-esp -b0.1 -6

./bintut.py ret2lib -b0.1

./bintut.py frame-faking -b0.1
