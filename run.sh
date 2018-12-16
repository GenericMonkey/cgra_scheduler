# convert source code to bitcode (IR)
clang-6.0 -Xclang  -disable-O0-optnone  -emit-llvm -c $1.c -o $1.bc
# canonicalize natural loops
opt-6.0 -loop-simplify $1.bc -o $1.final.bc
# instrument profiler
#opt -pgo-instr-gen -instrprof $1.ls.bc -o $1.ls.prof.bc
## generate binary executable with profiler embedded
#clang -fprofile-instr-generate $1.ls.prof.bc -o $1.prof
## run the proram to collect profile data. After this run, a filed named default.profraw is created, which contains the profile data
## this run will also generate the correct output
#./$1.prof > correct_output
## convert the profile data so that we can use it in LLVM
#llvm-profdata merge -output=pgo.profdata default.profraw
## use the profile data as input, and apply the HW2 pass
#opt -pgo-instr-use -pgo-test-profile-file=pgo.profdata -block-placement $1.ls.bc > $1.final.bc
opt-6.0  -constprop -instcombine -adce -licm -adce $1.final.bc -o $1.end.bc
opt-6.0  -mem2reg -loop-simplify -deadargelim -adce -die $1.end.bc > output.bc
opt-6.0  -load ~/583/master/HW1/HW1PASS/LLVMHW1PASS.so -printLoops output.bc -o tw.bc &> output_loops
#opt -constprop $1.final.bc > $1.final.1.bc
#opt -instcombine $1.final.1.bc > $1.final.3.bc
#opt -deadargelim $1.final.3.bc > $1.final.4.bc 
#opt -dse $1.final.4.bc > $1.final.5.bc 
#opt -licm $1.final.5.bc > $1.final.6.bc 
#opt -adce $1.final.6.bc > $1.end.bc 
# generate binary executable after FPLICM
llvm-dis-6.0 $1.end.bc
llvm-dis-6.0 output.bc
llvm-dis-6.0 $1.bc
