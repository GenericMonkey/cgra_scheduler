; ModuleID = 'output.bc'
source_filename = "simple_bf.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-pc-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define void @kernel(i32*, i32*, i32*, i32*) #0 {
  br label %5

; <label>:5:                                      ; preds = %28, %4
  %storemerge = phi i32 [ 0, %4 ], [ %29, %28 ]
  %6 = icmp slt i32 %storemerge, 1024
  br i1 %6, label %7, label %30

; <label>:7:                                      ; preds = %5
  %8 = sext i32 %storemerge to i64
  %9 = getelementptr inbounds i32, i32* %0, i64 %8
  %10 = load i32, i32* %9, align 4
  %11 = sub nsw i32 128, %10
  %12 = sext i32 %storemerge to i64
  %13 = getelementptr inbounds i32, i32* %1, i64 %12
  %14 = load i32, i32* %13, align 4
  %15 = sub nsw i32 64, %14
  %16 = sext i32 %storemerge to i64
  %17 = getelementptr inbounds i32, i32* %2, i64 %16
  %18 = load i32, i32* %17, align 4
  %19 = add nsw i32 %18, 32
  %20 = mul nsw i32 %11, %11
  %21 = mul nsw i32 %15, %15
  %22 = mul nsw i32 %19, %19
  %23 = add nsw i32 %20, %21
  %24 = add nsw i32 %23, %22
  %25 = ashr i32 %24, 2
  %26 = sext i32 %storemerge to i64
  %27 = getelementptr inbounds i32, i32* %3, i64 %26
  store i32 %25, i32* %27, align 4
  br label %28

; <label>:28:                                     ; preds = %7
  %29 = add nsw i32 %storemerge, 1
  br label %5

; <label>:30:                                     ; preds = %5
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
!1 = !{!"clang version 6.0.0-1ubuntu2~16.04.1 (tags/RELEASE_600/final)"}
