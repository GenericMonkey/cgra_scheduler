//outer product boyz
#include <stdlib.h>
#include <stdio.h>

int n = 64;

int kernel(int  vec_a[n],int  vec_b[n], int result[n]) { 
    int i = 0, j = 0, k = 0;  
	int dot = 0;
    int numiter = 64;
    //multiply
    for (i = 0; i < numiter; ++i) {
    	result[i] = vec_a[i] * vec_b[i];
		dot += result[i];
    }
    return dot;
}



int main() {
	int n = 64;
	int i = 0;
	int vec_a[n], vec_b[n], result[n];
	for (i = 0; i < n; ++i) {
		vec_a[i] = rand() % 64;
		vec_b[i] = rand() % 64;
		result[i] = 0;
	}

    kernel(vec_a,vec_b,result);

}
