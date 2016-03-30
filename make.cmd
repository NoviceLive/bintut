rem cl /Fe:32.exe sources/fread.c /link /debug


cl sources/fread.c /GS- /link /debug /out:32.exe
move 32.exe bintut\courses\targets\nx_off-canary_off-x86.exe


rem /dynamicbase:no
