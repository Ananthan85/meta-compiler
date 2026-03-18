#!/bin/bash

export GOROOT=/home/feyd/sdk/go1.22.12
export PATH=/home/feyd/sdk/go1.22.12/bin:$PATH

# tried gcc first but the ir output was messy
# gcc -S -emit-llvm target.c 

echo "compiling c to IR..."
clang -S -emit-llvm -O0 target.c -o target_c.ll

echo "gompiling go to IR..."
tinygo build -opt=0 -o target_go.ll target.go

echo "linking files..."
llvm-link -S target_c.ll target_go.ll -o polyglot_unified.ll

echo "running verifiction..."
python3 verify.py polyglot_unified.ll
