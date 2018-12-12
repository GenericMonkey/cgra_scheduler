#include <stdlib.h>



void kernel(int * x, int * y, int * z, int * fake_dist){ 
    int size = 1024;
    int i = 0; 
    int x_comp = 0, y_comp = 0, z_comp = 0;
	for (i = 0; i < size; ++i) {
		x_comp = 128 - x[i];
		y_comp = 64 - y[i];
		z_comp = 32 + z[i];

		x_comp = x_comp * x_comp;
		y_comp = y_comp * y_comp;
		z_comp = z_comp * z_comp;

		fake_dist[i] = (x_comp + y_comp + z_comp) >> 2;
	}
}






int main() {
	int size = 1024;
	int i = 0;
	int x[size], y[size], z[size], fake_dist[size];
	for(i = 0; i < size; ++i) {
		x[i] = rand() % 64;
		y[i] = rand() % 64;
		z[i] = rand() % 64;
	}
	
	// you should see the label even in the assembly
    kernel(x,y,z,fake_dist);
}



