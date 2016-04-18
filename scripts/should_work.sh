#!/usr/bin/env bash


python ./bintut.py plain -b0.1 "${@}" &&
    python ./bintut.py plain -b0.1 -6 "${@}" &&
    python ./bintut.py nop-slide -b0.1 "${@}" &&
    python ./bintut.py nop-slide -b0.1 -6 "${@}" &&
    python ./bintut.py jmp-esp -b0.1 "${@}" &&
    python ./bintut.py jmp-esp -b0.1 -6 "${@}" &&
    python ./bintut.py ret2lib -b0.1 "${@}" &&
    python ./bintut.py frame-faking -b0.1 "${@}"
