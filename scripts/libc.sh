#!/usr/bin/env bash


# Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>


stop() {
    printf '\n\n\n'
}


cat /etc/ld.so.conf /etc/ld.so.conf.d/*
stop
realpath "$(gcc --print-file-name libc.so.6 -m64)"
realpath "$(gcc --print-file-name libc.so.6 -m32)"
stop
ldd ./bintut/courses/targets/fread-nx_on-canary_off-x86
