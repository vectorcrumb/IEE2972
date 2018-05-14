/*
 * File: _coder_basicNeural20_api.h
 *
 * MATLAB Coder version            : 2.8
 * C/C++ source code generated on  : 12-Jul-2017 16:43:59
 */

#ifndef ___CODER_BASICNEURAL20_API_H__
#define ___CODER_BASICNEURAL20_API_H__

/* Include Files */
#include "tmwtypes.h"
#include "mex.h"
#include "emlrt.h"
#include <stddef.h>
#include <stdlib.h>
#include "_coder_basicNeural20_api.h"

/* Variable Declarations */
extern emlrtCTX emlrtRootTLSGlobal;
extern emlrtContext emlrtContextGlobal;

/* Function Declarations */
extern void basicNeural20(real_T x1[3], real_T b_y1[3]);
extern void basicNeural20_api(const mxArray *prhs[1], const mxArray *plhs[1]);
extern void basicNeural20_atexit(void);
extern void basicNeural20_initialize(void);
extern void basicNeural20_terminate(void);
extern void basicNeural20_xil_terminate(void);

#endif

/*
 * File trailer for _coder_basicNeural20_api.h
 *
 * [EOF]
 */
