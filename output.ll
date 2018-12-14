; ModuleID = 'output.bc'
source_filename = "simple_bf.c"
target datalayout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"
target triple = "x86_64-unknown-linux-gnu"

; Function Attrs: noinline nounwind uwtable
define void @kernel(i32*, i32*, i32*, i32*) #0 {
  br label %5

; <label>:5:                                      ; preds = %5, %4
  %storemerge1 = phi i32 [ 0, %4 ], [ %47, %5 ]
  %6 = sext i32 %storemerge1 to i64
  %7 = getelementptr inbounds i32, i32* %0, i64 %6
  %8 = load i32, i32* %7, align 4
  %9 = sub nsw i32 128, %8
  %10 = sext i32 %storemerge1 to i64
  %11 = getelementptr inbounds i32, i32* %1, i64 %10
  %12 = load i32, i32* %11, align 4
  %13 = sub nsw i32 64, %12
  %14 = sext i32 %storemerge1 to i64
  %15 = getelementptr inbounds i32, i32* %2, i64 %14
  %16 = load i32, i32* %15, align 4
  %17 = add nsw i32 %16, 32
  %18 = mul nsw i32 %9, %9
  %19 = mul nsw i32 %13, %13
  %20 = mul nsw i32 %17, %17
  %21 = add nsw i32 %18, %19
  %22 = add nsw i32 %21, %20
  %23 = ashr i32 %22, 2
  %24 = sext i32 %storemerge1 to i64
  %25 = getelementptr inbounds i32, i32* %3, i64 %24
  store i32 %23, i32* %25, align 4
  %26 = add nuw nsw i32 %storemerge1, 1
  %27 = sext i32 %26 to i64
  %28 = getelementptr inbounds i32, i32* %0, i64 %27
  %29 = load i32, i32* %28, align 4
  %30 = sub nsw i32 128, %29
  %31 = sext i32 %26 to i64
  %32 = getelementptr inbounds i32, i32* %1, i64 %31
  %33 = load i32, i32* %32, align 4
  %34 = sub nsw i32 64, %33
  %35 = sext i32 %26 to i64
  %36 = getelementptr inbounds i32, i32* %2, i64 %35
  %37 = load i32, i32* %36, align 4
  %38 = add nsw i32 %37, 32
  %39 = mul nsw i32 %30, %30
  %40 = mul nsw i32 %34, %34
  %41 = mul nsw i32 %38, %38
  %42 = add nsw i32 %39, %40
  %43 = add nsw i32 %42, %41
  %44 = ashr i32 %43, 2
  %45 = sext i32 %26 to i64
  %46 = getelementptr inbounds i32, i32* %3, i64 %45
  store i32 %44, i32* %46, align 4
  %47 = add nuw nsw i32 %26, 1
  %48 = icmp ult i32 %47, 1024
  br i1 %48, label %5, label %49, !llvm.loop !2

; <label>:49:                                     ; preds = %5
  %.lcssa4 = phi i32 [ %41, %5 ]
  %.lcssa2 = phi i32 [ %40, %5 ]
  %.lcssa = phi i32 [ %39, %5 ]
  %storemerge.lcssa = phi i32 [ %47, %5 ]
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

; <label>:5:                                      ; preds = %5, %0
  %storemerge1 = phi i32 [ 0, %0 ], [ %31, %5 ]
  %6 = call i32 @rand() #1
  %7 = srem i32 %6, 64
  %8 = sext i32 %storemerge1 to i64
  %9 = getelementptr inbounds [1024 x i32], [1024 x i32]* %1, i64 0, i64 %8
  store i32 %7, i32* %9, align 4
  %10 = call i32 @rand() #1
  %11 = srem i32 %10, 64
  %12 = sext i32 %storemerge1 to i64
  %13 = getelementptr inbounds [1024 x i32], [1024 x i32]* %2, i64 0, i64 %12
  store i32 %11, i32* %13, align 4
  %14 = call i32 @rand() #1
  %15 = srem i32 %14, 64
  %16 = sext i32 %storemerge1 to i64
  %17 = getelementptr inbounds [1024 x i32], [1024 x i32]* %3, i64 0, i64 %16
  store i32 %15, i32* %17, align 4
  %18 = add nuw nsw i32 %storemerge1, 1
  %19 = call i32 @rand() #1
  %20 = srem i32 %19, 64
  %21 = sext i32 %18 to i64
  %22 = getelementptr inbounds [1024 x i32], [1024 x i32]* %1, i64 0, i64 %21
  store i32 %20, i32* %22, align 4
  %23 = call i32 @rand() #1
  %24 = srem i32 %23, 64
  %25 = sext i32 %18 to i64
  %26 = getelementptr inbounds [1024 x i32], [1024 x i32]* %2, i64 0, i64 %25
  store i32 %24, i32* %26, align 4
  %27 = call i32 @rand() #1
  %28 = srem i32 %27, 64
  %29 = sext i32 %18 to i64
  %30 = getelementptr inbounds [1024 x i32], [1024 x i32]* %3, i64 0, i64 %29
  store i32 %28, i32* %30, align 4
  %31 = add nuw nsw i32 %18, 1
  %32 = icmp ult i32 %31, 1024
  br i1 %32, label %5, label %33, !llvm.loop !4

; <label>:33:                                     ; preds = %5
  %storemerge.lcssa = phi i32 [ %31, %5 ]
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
!2 = distinct !{!2, !3}
!3 = !{!"llvm.loop.unroll.disable"}
!4 = distinct !{!4, !3}
