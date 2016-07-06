#!/usr/bin/env bash


PYTHON=python


${PYTHON} ./bintut.py plain -b0.1 "${@}" &&
    ${PYTHON} ./bintut.py plain -b0.1 -6 "${@}" &&
    ${PYTHON} ./bintut.py nop-slide -b0.1 "${@}" &&
    ${PYTHON} ./bintut.py nop-slide -b0.1 -6 "${@}" &&
    ${PYTHON} ./bintut.py jmp-esp -b0.1 "${@}" &&
    ${PYTHON} ./bintut.py jmp-esp -b0.1 -6 "${@}" &&
    ${PYTHON} ./bintut.py off-by-one -b0.1 "${@}" &&
    ${PYTHON} ./bintut.py off-by-one -b0.1 -6 "${@}" &&
    ${PYTHON} ./bintut.py ret2lib -b0.1 "${@}" &&
    ${PYTHON} ./bintut.py frame-faking -b0.1 "${@}"
