#!/usr/bin/env bash


#
# Copyright 2015-2016 Gu Zhengxiong <rectigu@gmail.com>
#


TARGET=./miscbin/auto


for time in {1..4}; do
    printf '%s ' "$(2>&1 ${TARGET})"
    printf '%s ' "$(2>&1 setarch $(uname -m) -R ${TARGET})"
    printf '%s\n' "$(2>&1 >/dev/null gdb ${TARGET} --batch -ex 'run')"
done
