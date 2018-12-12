; ModuleID = 'output.bc'
source_filename = "simple_bf.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define void @kernel(i32*, i32*, i32*, i32*) #0 {
  br label %5

; <label>:5:                                      ; preds = %31, %4
  %6 = phi i32 [ 0, %4 ], [ %25, %31 ]
  %7 = phi i32 [ 0, %4 ], [ %24, %31 ]
  %8 = phi i32 [ 0, %4 ], [ %23, %31 ]
  %storemerge = phi i32 [ 0, %4 ], [ %32, %31 ]
  %9 = icmp slt i32 %storemerge, 1024
  br i1 %9, label %10, label %33

; <label>:10:                                     ; preds = %5
  %11 = sext i32 %storemerge to i64
  %12 = getelementptr inbounds i32, i32* %0, i64 %11
  %13 = load i32, i32* %12, align 4
  %14 = sub nsw i32 128, %13
  %15 = sext i32 %storemerge to i64
  %16 = getelementptr inbounds i32, i32* %1, i64 %15
  %17 = load i32, i32* %16, align 4
  %18 = sub nsw i32 64, %17
  %19 = sext i32 %storemerge to i64
  %20 = getelementptr inbounds i32, i32* %2, i64 %19
  %21 = load i32, i32* %20, align 4
  %22 = add nsw i32 %21, 32
  %23 = mul nsw i32 %14, %14
  %24 = mul nsw i32 %18, %18
  %25 = mul nsw i32 %22, %22
  %26 = add nsw i32 %23, %24
  %27 = add nsw i32 %26, %25
  %28 = ashr i32 %27, 2
  %29 = sext i32 %storemerge to i64
  %30 = getelementptr inbounds i32, i32* %3, i64 %29
  store i32 %28, i32* %30, align 4
  br label %31

; <label>:31:                                     ; preds = %10
  %32 = add nsw i32 %storemerge, 1
  br label %5

; <label>:33:                                     ; preds = %5
  %.lcssa4 = phi i32 [ %6, %5 ]
  %.lcssa2 = phi i32 [ %7, %5 ]
  %.lcssa = phi i32 [ %8, %5 ]
  %storemerge.lcssa = phi i32 [ %storemerge, %5 ]
  ret void
}

; Function Attrs: noinline nounwind uwtable
define i32 @main() #0 {
  %1 = alloca [1024 x i32], align 16
  %.sub = getelementptr inbounds [1024 x i32], [1024 x i32]* %1, i64 0, i64 0
  %2 = alloca [1024 x i32], align 16
  %.sub1 = getelementptr inbounds [1024 x i32], [1024 x i32]* %2, i64 0, i64 0
  %3 = alloca [1024 x i32], align 16
  %.sub2 = getelementptr inbounds [1024 x i32], [1024 x i32]* %3, i64 0, i64 0
  %4 = alloca [1024 x i32], align 16
  %.sub3 = getelementptr inbounds [1024 x i32], [1024 x i32]* %4, i64 0, i64 0
  br label %5

; <label>:5:                                      ; preds = %20, %0
  %storemerge = phi i32 [ 0, %0 ], [ %21, %20 ]
  %6 = icmp slt i32 %storemerge, 1024
  br i1 %6, label %7, label %22

; <label>:7:                                      ; preds = %5
  %8 = call i32 @rand() #1
  %9 = srem i32 %8, 64
  %10 = sext i32 %storemerge to i64
  %11 = getelementptr inbounds [1024 x i32], [1024 x i32]* %1, i64 0, i64 %10
  store i32 %9, i32* %11, align 4
  %12 = call i32 @rand() #1
  %13 = srem i32 %12, 64
  %14 = sext i32 %storemerge to i64
  %15 = getelementptr inbounds [1024 x i32], [1024 x i32]* %2, i64 0, i64 %14
  store i32 %13, i32* %15, align 4
  %16 = call i32 @rand() #1
  %17 = srem i32 %16, 64
  %18 = sext i32 %storemerge to i64
  %19 = getelementptr inbounds [1024 x i32], [1024 x i32]* %3, i64 0, i64 %18
  store i32 %17, i32* %19, align 4
  br label %20

; <label>:20:                                     ; preds = %7
  %21 = add nsw i32 %storemerge, 1
  br label %5

; <label>:22:                                     ; preds = %5
  %storemerge.lcssa = phi i32 [ %storemerge, %5 ]
  call void @kernel(i32* nonnull %.sub, i32* nonnull %.sub1, i32* nonnull %.sub2, i32* nonnull %.sub3)
  ret i32 0
}

; Function Attrs: nounwind
declare i8* @llvm.stacksave() #1

; Function Attrs: nounwind
declare i32 @rand() #2

; Function Attrs: nounwind
declare void @llvm.stackrestore(i8*) #1

attributes #0 = { noinline nounwind uwtable "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-jump-tables"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }
attributes #1 = { nounwind }
attributes #2 = { nounwind "correctly-rounded-divide-sqrt-fp-math"="false" "disable-tail-calls"="false" "less-precise-fpmad"="false" "no-frame-pointer-elim"="true" "no-frame-pointer-elim-non-leaf" "no-infs-fp-math"="false" "no-nans-fp-math"="false" "no-signed-zeros-fp-math"="false" "no-trapping-math"="false" "stack-protector-buffer-size"="8" "target-cpu"="x86-64" "target-features"="+fxsr,+mmx,+sse,+sse2,+x87" "unsafe-fp-math"="false" "use-soft-float"="false" }

!llvm.module.flags = !{!0}
!llvm.ident = !{!1}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{!"clang version 6.0.1 (tags/RELEASE_601/final)"}
