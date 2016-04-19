#!/usr/bin/env bash


# Copyright 2016 Gu Zhengxiong <rectigu@gmail.com>


cat /etc/ld.so.conf /etc/ld.so.conf.d/*
realpath "$(gcc --print-file-name libc.so.6 -m64)"
realpath "$(gcc --print-file-name libc.so.6 -m32)"
