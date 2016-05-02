#!/usr/bin/env bash


gdb --batch --eval-command 'pi print(__import__("sys").version)'
