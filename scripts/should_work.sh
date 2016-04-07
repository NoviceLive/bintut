#!/usr/bin/env bash


./bintut.py plain -b0.1 -v &&
    ./bintut.py plain -b0.1 -6 -v &&
    ./bintut.py nop-slide -b0.1 -v &&
    ./bintut.py nop-slide -b0.1 -6 -v &&
    ./bintut.py jmp-esp -b0.1 -v &&
    ./bintut.py jmp-esp -b0.1 -6 -v &&
    ./bintut.py ret2lib -b0.1 -v &&
    ./bintut.py frame-faking -b0.1 -v
