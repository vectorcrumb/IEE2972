/*
 * File: main.c
 *
 * MATLAB Coder version            : 2.8
 * C/C++ source code generated on  : 12-Jul-2017 16:43:59
 */

/*************************************************************************/
/* This automatically generated example C main file shows how to call    */
/* entry-point functions that MATLAB Coder generated. You must customize */
/* this file for your application. Do not modify this file directly.     */
/* Instead, make a copy of this file, modify it, and integrate it into   */
/* your development environment.                                         */
/*                                                                       */
/* This file initializes entry-point function arguments to a default     */
/* size and value before calling the entry-point functions. It does      */
/* not store or use any values returned from the entry-point functions.  */
/* If necessary, it does pre-allocate memory for returned values.        */
/* You can use this file as a starting point for a main function that    */
/* you can deploy in your application.                                   */
/*                                                                       */
/* After you copy the file, and before you deploy it, you must make the  */
/* following changes:                                                    */
/* * For variable-size function arguments, change the example sizes to   */
/* the sizes that your application requires.                             */
/* * Change the example values of function arguments to the values that  */
/* your application requires.                                            */
/* * If the entry-point functions return values, store these values or   */
/* otherwise use them as required by your application.                   */
/*                                                                       */
/*************************************************************************/
/* Include Files */
#include <stdio.h>
#include "rt_nonfinite.h"
#include "basicNeural20.h"
#include "main.h"
#include "basicNeural20_terminate.h"
#include "basicNeural20_initialize.h"

/* Function Declarations */
static void argInit_3x1_real_T(double result[3]);
static double argInit_real_T(void);
static void main_basicNeural20(void);

/* Function Definitions */

/*
 * Arguments    : double result[3]
 * Return Type  : void
 */
static void argInit_3x1_real_T(double result[3])
{
  int b_j0;

  /* Loop over the array to initialize each element. */
  for (b_j0 = 0; b_j0 < 3; b_j0++) {
    /* Set the value of the array element.
       Change this value to the value that the application requires. */
    result[b_j0] = argInit_real_T();
  }
}

/*
 * Arguments    : void
 * Return Type  : double
 */
static double argInit_real_T(void)
{
  return 0.0;
}

/*
 * Arguments    : void
 * Return Type  : void
 */
static void main_basicNeural20(void)
{
  double dv0[3];
  double b_y1[3];

  /* Initialize function 'basicNeural20' input arguments. */
  /* Initialize function input argument 'x1'. */
  /* Call the entry-point 'basicNeural20'. */
  argInit_3x1_real_T(dv0);
  basicNeural20(dv0, b_y1);
}

static void neural_wrapper(double x_in[3], double *y_out) {
  basicNeural20(x_in, y_out);
}

/*
 * Arguments    : int argc
 *                const char * const argv[]
 * Return Type  : int
 */
int main(int argc, const char * const argv[])
{
  (void)argc;
  (void)argv;

  /* Initialize the application.
     You do not need to do this more than one time. */
  basicNeural20_initialize();

  /* Invoke the entry-point functions.
     You can call entry-point functions multiple times. */
  main_basicNeural20();
  for (int i = 1; i < argc; i++) {
    printf("%s\n", argv[i]);
  }
  if (argc == 4) {
    double y[3];
    double x[3];
    double x1, x2, x3;
    argInit_3x1_real_T(y);
    sscanf(argv[1], "%lf", &x1);
    sscanf(argv[2], "%lf", &x2);
    sscanf(argv[3], "%lf", &x3);
    x[0] = x1;
    x[1] = x2;
    x[2] = x3;
    neural_wrapper(x, y);
    for (int j = 0; j < 3; j++) {
      printf("%lf\n", y[j]);
    }
  }
  /* Terminate the application.
     You do not need to do this more than one time. */
  basicNeural20_terminate();
  return 0;
}

/*
 * File trailer for main.c
 *
 * [EOF]
 */
