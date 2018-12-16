//===- HW1.cpp - Example code from "Writing an LLVM Pass" ---------------===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is distributed under the University of Illinois Open Source
// License. See LICENSE.TXT for details.
//
//===----------------------------------------------------------------------===//
//
// This file implements two versions of the LLVM "HW1" pass described
// in docs/WritingAnLLVMPass.html
//
//===----------------------------------------------------------------------===//
#include "llvm/ADT/Statistic.h"
#include "llvm/Analysis/AliasAnalysis.h"
#include "llvm/Analysis/AliasSetTracker.h"
#include "llvm/Analysis/BasicAliasAnalysis.h"
#include "llvm/Analysis/CaptureTracking.h"
#include "llvm/Analysis/ConstantFolding.h"
#include "llvm/Analysis/GlobalsModRef.h"
#include "llvm/Analysis/Loads.h"
#include "llvm/Analysis/LoopInfo.h"
#include "llvm/Analysis/LoopPass.h"
#include "llvm/Analysis/MemoryBuiltins.h"
#include "llvm/Analysis/MemorySSA.h"
#include "llvm/Analysis/OptimizationRemarkEmitter.h"
#include "llvm/Analysis/ScalarEvolution.h"
#include "llvm/Analysis/ScalarEvolutionAliasAnalysis.h"
#include "llvm/Analysis/TargetLibraryInfo.h"
#include "llvm/Analysis/ValueTracking.h"
#include "llvm/IR/CFG.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/IR/DerivedTypes.h"
#include "llvm/IR/Dominators.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IntrinsicInst.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/Metadata.h"
#include "llvm/IR/PredIteratorCache.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Support/Debug.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/Scalar.h"
#include "llvm/Transforms/Scalar/LoopPassManager.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"
#include "llvm/Transforms/Utils/Local.h"
#include "llvm/Transforms/Utils/LoopUtils.h"
#include "llvm/Transforms/Utils/SSAUpdater.h"
#include <algorithm>
#include <utility>
#include <iostream>
#include <unordered_map>
#include "llvm/ADT/Statistic.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Instruction.h"
#include "llvm/Pass.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Analysis/BranchProbabilityInfo.h"
#include "llvm/Analysis/BlockFrequencyInfo.h"
#include <set>
#include <iostream> 
using namespace llvm;

#define DEBUG_TYPE "hw1"



namespace {

    int recBBprint(BasicBlock * hotPtr, std::set<BasicBlock *> &seenSet, Loop * L){
        if(seenSet.find(hotPtr) != seenSet.end() || L->contains(hotPtr) == false)
            return 0;
        for( BasicBlock::iterator i_iter = hotPtr->begin(); i_iter != hotPtr->end(); ++i_iter) {
            Instruction * I = &(*i_iter);
            I->print(errs());
            errs() <<  "\n";
        }
        seenSet.emplace(hotPtr);
        TerminatorInst * ct = hotPtr->getTerminator();  
        unsigned ns = ct->getNumSuccessors();
        for (unsigned i = 0; i < ns; i++){
            recBBprint(ct->getSuccessor(i), seenSet, L); 
        }

    }

    // HW1 - The first implementation, without getAnalysisUsage.
    struct HW1 : public LoopPass{
        static char ID; // Pass identification, replacement for typeid
        HW1() : LoopPass(ID) {}
        bool runOnLoop(Loop * L, LPPassManager &LPM){
            BasicBlock *Header    = L->getLoopPreheader()->getSingleSuccessor(); 
            BasicBlock *Traversal = Header;
            std::set<BasicBlock *> seenset;
            recBBprint(Header, seenset,L);
        } 
    };

}

char HW1::ID = 0;
static RegisterPass<HW1> X("printLoops", "LoopPrinter");
