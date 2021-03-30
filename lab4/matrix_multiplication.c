//
// Created by sylwia on 3/30/21.
//

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <sys/times.h>
#include <unistd.h>
#include <gsl/gsl_blas.h>


void naive_multiplication(int** A, int** B, int n){
    int* matrix[n];
    for (int i = 0; i < n; i++){
        matrix[i] = calloc(n, sizeof(int*));
    }

    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            matrix[i][j] = 0;
        }
    }

    for (int k = 0; k < n; k++){
        for (int j = 0; j < n; j++){  //col
            for (int i = 0; i < n; i++){  //row
                matrix[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

void better_multiplication(int** A, int** B, int n){
    int* matrix[n];
    for (int i = 0; i < n; i++){
        matrix[i] = calloc(n, sizeof(int*));
    }

    for (int i = 0; i < n; i++){
        for (int j = 0; j < n; j++){
            matrix[i][j] = 0;
        }
    }

    for (int i = 0; i < n; i++){  //row
        for (int j = 0; j < n; j++){  //col
            for (int k = 0; k < n; k++){
                matrix[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}


void BLAS_multiplication(double* a, double* b, int size){

    double* c = malloc(sizeof(double) * size * size);
    for (int i = 0; i < size * size; i++){
        c[i] = i;
    }

    gsl_matrix_view A = gsl_matrix_view_array(a, size, size);
    gsl_matrix_view B = gsl_matrix_view_array(b, size, size);
    gsl_matrix_view C = gsl_matrix_view_array(c, size, size);

    // Compute C = A B

    gsl_blas_dgemm (CblasNoTrans, CblasNoTrans,
                    1.0, &A.matrix, &B.matrix,
                    0.0, &C.matrix);


}



int** build_matrix(int rows, int cols){
    int* values = calloc(rows * cols, sizeof(int));
    int**  r = malloc(cols * sizeof(int*));

    for (int i = 0; i < cols; ++i)
        r[i] = values + i * rows;

    for (int i = 0; i < rows; i++){
        for (int j = 0; j < cols; j++){
            r[i][j] = rand() % 20;
        }
    }
    return r;
}

double* build_matrix_BLAS(int size){
    double* m = malloc(sizeof(double) * size);
    for (int i = 0; i < size; i++){
        m[i] = i;
    }
    return m;
}

long double time_sec(clock_t time){
    return (long double)(time) / sysconf(_SC_CLK_TCK);
}

int main(){
    srand(time(NULL));

    struct tms start_tms;
    struct tms end_tms;
    clock_t clock_start;
    clock_t clock_end;


    int n;  // number of rows/cols of square matrix
    int** A;
    int** B;
    double * a;
    double * b;

    FILE* fd;
    fd = fopen("results_C.csv", "w+");

    for (n = 50; n < 500; n+=30) {
        for (int i = 0; i < 10; i++) {
            fprintf(fd, "%d,%d,", n, i);

            A = build_matrix(n, n);
            B = build_matrix(n, n);
            a = build_matrix_BLAS(n * n);
            b = build_matrix_BLAS(n * n);

            clock_start = times(&start_tms);
            naive_multiplication(A, B, n);
            clock_end = times(&end_tms);
            fprintf(fd, "%Lf,", time_sec(clock_end - clock_start));

            clock_start = times(&start_tms);
            better_multiplication(A, B, n);
            clock_end = times(&end_tms);
            fprintf(fd, "%Lf,", time_sec(clock_end - clock_start));

            clock_start = times(&start_tms);
            BLAS_multiplication(a, b, n);
            clock_end = times(&end_tms);
            fprintf(fd, "%Lf\n", time_sec(clock_end - clock_start));
        }
    }

    fclose(fd);
    
    return 0;
}
