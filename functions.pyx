import cython

cdef extern from "c_astrom2.h":
	double to_jsky(float fmag, float mag)
	int search_vega_filter(char *system, char *filtername, float *Lambda, float *dlambda, float *fmag)

def wrap_c_to_jsky(fmag, mag):
	return to_jsky(fmag, mag)

def wrap_c_search_vega_filter(SysteM, FilternamE, LambdA, DlambdA, FmaG):
	py_byte_SysteM    = bytes(SysteM, 'UTF-8')
	cdef char* system = py_byte_SysteM
	
	py_byte_FilternamE    = bytes(FilternamE, 'UTF-8')
	cdef char* filtername = py_byte_FilternamE
	
	cdef float c = LambdA
	cdef float* Lambda
	Lambda       = &c

	cdef float d = DlambdA
	cdef float* dlambda 
	dlambda      = &d

	cdef float e = FmaG
	cdef float* fmag
	fmag         = &e	
	
	search_vega_filter(system, filtername, Lambda, dlambda, fmag)
	
	return Lambda[0], dlambda[0], fmag[0]
	
	
	
#Limbo

