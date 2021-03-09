//
// Created by sylwia on 3/9/21.
//

#include <stdio.h>
#include <gsl/gsl_ieee_utils.h>

int main (void) {
    float x = 10.0;
    int precision = 50;
    int idx = 0;
    while(x != 0.0) {
        printf("%d\n", idx);
        printf("C float type: %.*f\n", precision, x);
        printf("IEEE754 repr:");
        gsl_ieee_printf_float(&x);
        printf("\n\n");
        x /= 5.0;
        idx++;
    }

    return 0;
}
