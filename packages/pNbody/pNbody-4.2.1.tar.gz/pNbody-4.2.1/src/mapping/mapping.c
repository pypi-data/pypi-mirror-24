#include <Python.h>
#include <math.h>
#include <numpy/arrayobject.h>
#define kxmax1d 1024

#define kxmax2d 1024
#define kymax2d 1024   
   
#define kxmax3d 64
#define kymax3d 64   
#define kzmax3d 64      
   
#define PI 3.14159265358979




/*! returns the maximum of two integers
 */
int imax(int x, int y)
{
  if(x > y)
    return x;
  else
    return y;
}

/*! returns the minimum of two integers
 */
int imin(int x, int y)
{
  if(x < y)
    return x;
  else
    return y;
}

/*! returns the maximum of two double
 */
double dmax(double x, double y)
{
  if(x > y)
    return x;
  else
    return y;
}

/*! returns the minimum of two double
 */
double dmin(double x, double y)
{
  if(x < y)
    return x;
  else
    return y;
}





/*********************************/
/* mkmap1d */
/*********************************/

static PyObject *
      mapping_mkmap1d(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i; 
	  int	ix;
	  int   kx;
	  npy_intp   ld[1];
	  
	  float dseo[kxmax1d];
	  float x,gm,am;
	  
          if (!PyArg_ParseTuple(args,"OOO(i)",&pos,&gmm,&amp,&kx))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  if (kx > kxmax1d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
          mat = (PyArrayObject *) PyArray_SimpleNew(1,ld,NPY_FLOAT);
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 1 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be one dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    dseo[ix]=0.;
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	    
	    ix = (int)(x);
	    
	    if (ix >= 0 && x < kx)
              dseo[ix] = dseo[ix] + gm*am;
	  }
	  	  
		
	  /* create the subimage */	  
	  for (i=0;i<kx;i++) {
            *(float*)(mat->data + i*(mat->strides[0])) = (float) dseo[i] ;
	  }
	  
	  
	  return PyArray_Return(mat);
      }               





/*********************************/
/* mkmap1dn */
/*********************************/

static PyObject *
      mapping_mkmap1dn(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i; 
	  int	ix;
	  int   kx;
	  npy_intp   ld[1];
	  
	  float *dseo;
	  float x,gm,am;
          size_t bytes;
	  
          if (!PyArg_ParseTuple(args,"OOO(i)",&pos,&gmm,&amp,&kx))
              return NULL;
	   
	   	  
	  if(!(dseo = malloc(bytes = kx*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }	  
	   
	  	  	  
	  
          /* create the output */
	  ld[0] = kx;
          mat = (PyArrayObject *) PyArray_SimpleNew(1,ld,NPY_FLOAT);
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 1 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be one dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    dseo[ix]=0.;
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	    
	    ix = (int)(x);
	    
	    if (ix >= 0 && x < kx)
              dseo[ix] = dseo[ix] + gm*am;
	  }
	  	  
		
	  /* create the subimage */	  
	  for (i=0;i<kx;i++) {
            *(float*)(mat->data + i*(mat->strides[0])) = (float) dseo[i] ;
	  }
	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
      }               




/*********************************/
/* mkcic1dn */
/*********************************/

static PyObject *
      mapping_mkcic1dn(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i; 
	  int	ix;
	  int   kx;
	  npy_intp   ld[1];
	  
	  double *dseo;
	  float x,gm,am;
	  double xs,xi;
          size_t bytes;
	  
          if (!PyArg_ParseTuple(args,"OOO(i)",&pos,&gmm,&amp,&kx))
              return NULL;
	   
	   	  
	  if(!(dseo = malloc(bytes = kx*sizeof(double))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }	  
	   
	  	  	  
	  
          /* create the output */
	  ld[0] = kx;
          mat = (PyArrayObject *) PyArray_SimpleNew(1,ld,NPY_FLOAT);
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 1 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be one dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    dseo[ix]=0.;
	  }
	  
          double ss=0;


	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	    
	    
	    //xi = x - 0.5;
	    xi = x;
	    
	    ix = floor(xi);
	    xs = xi-ix;
	    
	    if (ix<0)			/* too small */
	      {
	         dseo[0]   = dseo[0]   + gm*am; 
		 ss+=gm*am;
		 printf("!!!!! ix<0\n");  	
	      }
	    else
	      {
	        //if (xi>=kx-0.5)		/* too big */
		if (ix>=kx)		/* too big */
		  {
		    dseo[kx-1]   = dseo[kx-1]   + gm*am;
		    ss+=gm*am;	
                    printf("!!!!! ix>=kx\n");    
		  }
		else			/* normal behavior */
		  {
		    //dseo[ix]   = dseo[ix]   + gm*am*(1-xs);
		    //dseo[ix+1] = dseo[ix+1] + gm*am*(  xs);
		    //dseo[ix]   = dseo[ix]   + gm*am;
		    
		    dseo[ix]   = dseo[ix]   + gm*am*(1-xs);
		    dseo[ix+1]   = dseo[ix+1]   + gm*am*(  xs);
		    
		    ss+=gm*am*(1-  xs);
		    ss+=gm*am*(  xs);
		    
		    if (xs > 1)
		      printf("!!!!! xs>1\n");
		    
		    if (ix<0)
		      printf("!!!!!-\n");
		    
		    if (ix>=kx)
		      printf("!!!!!+\n");		  }  
	      }  
	    
	      
	  }
	  
		
	  /* create the subimage */	  
	  for (i=0;i<kx;i++) {
            *(float*)(mat->data + i*(mat->strides[0])) = (float) dseo[i] ;
	    printf(">> %g\n",dseo[i]);
	  }
	  
	  printf(">>>>>%g\n",ss);
	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
      }  



/*********************************/
/* mkmap2d */
/*********************************/

static PyObject *
      mapping_mkmap2d(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j; 
	  int	ix,iy;
	  int   kx,ky;
	  npy_intp   ld[2];
	  
	  float dseo[kxmax2d][kymax2d];
	  float x,y,z,gm,am;
	  
          if (!PyArg_ParseTuple(args,"OOO(ii)",&pos,&gmm,&amp,&kx,&ky))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  if (kx > kxmax2d || ky > kymax2d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) { 
	      dseo[ix][iy]=0.;
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1])*(ky);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	    
	    ix = (int)(x);
            iy = (int)(y);
	    
	    if (ix >= 0 && ix < kx)
	      if (iy >= 0 && iy < ky)
	        dseo[ix][iy] = dseo[ix][iy] + gm*am;
	    	     
	  }
	  	  
		
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[i][j] ;
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }               



/*********************************/
/* mkmap2dn */
/*********************************/

static PyObject *
      mapping_mkmap2dn(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j; 
	  int	ix,iy;
	  int   kx,ky;
	  npy_intp   ld[2];
	  
	  float *dseo;
	  float x,y,z,gm,am;
	  size_t bytes;
	  
          if (!PyArg_ParseTuple(args,"OOO(ii)",&pos,&gmm,&amp,&kx,&ky))
              return NULL;
	   
	   
	  
          if(!(dseo = malloc(bytes = kx*ky*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }	  
	  	  

          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) { 
	      dseo[iy+ix*ky]=0.;
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1])*(ky);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	    
	    ix = (int)(x);
            iy = (int)(y);

	    if (ix >= 0 && ix < kx)
	      if (iy >= 0 && iy < ky)
	        {
		  dseo[iy+ix*ky]=dseo[iy+ix*ky] + gm*am;		  
	    	}     
	  }
          	  		
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[j+i*ky] ;
	    }
	  }
	  	  	  
	  free(dseo);

	  return PyArray_Return(mat);
      }               



/*********************************/
/* mkmap3d */
/*********************************/

static PyObject *
      mapping_mkmap3d(self, args)
          PyObject *self;
          PyObject *args;
      {
	  	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j,k; 
	  int	ix,iy,iz;
	  int   kx,ky,kz;
	  npy_intp   ld[3];
	  
	  float dseo[kxmax3d][kymax3d][kzmax3d];
	  float x,y,z,gm,am;
	  
          if (!PyArg_ParseTuple(args,"OOO(iii)",&pos,&gmm,&amp,&kx,&ky,&kz))
              return NULL;
	  
	  	    	   
	  /* check max size of matrix */
	  if (kx > kxmax3d || ky > kymax3d || kz > kzmax3d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
	  ld[2] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(3,ld,NPY_FLOAT);
	 	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) {
	      for (iz=0;iz<kz;iz++) {
	        dseo[ix][iy][iz]=0.;
	      }	
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1])*(ky);
	    z	= *(float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1])*(kz);
	    
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 


	    ix = (int)(x);
            iy = (int)(y);
	    iz = (int)(z);
	    
	    if (ix >= 0 && ix < kx)
	      if (iy >= 0 && iy < ky)
	        if (iz >= 0 && iz < kz)
	          dseo[ix][iy][iz] = dseo[ix][iy][iz] + gm*am;
	    
	  }
	  	  
		
	  /* create the subimage */
	  for (k=0;k<kz;k++) {	  
	    for (j=0;j<ky;j++) {
	      for (i=0;i<kx;i++) {
	        *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1]) + (k)*(mat->strides[2])) = (float) dseo[i][j][k] ;
	      }	
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }               



/*********************************/
/* mkmap3dn */
/*********************************/

static PyObject *
      mapping_mkmap3dn(self, args)
          PyObject *self;
          PyObject *args;
      {
	  	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j,k; 
	  int	ix,iy,iz;
	  int   kx,ky,kz;
	  npy_intp   ld[3];
	  
	  float *dseo;
	  float x,y,z,gm,am;
	  size_t bytes;
	  
          if (!PyArg_ParseTuple(args,"OOO(iii)",&pos,&gmm,&amp,&kx,&ky,&kz))
              return NULL;
	  
	  	    	   
          if(!(dseo = malloc(bytes = kx*ky*kz*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }	
	   	  	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
	  ld[2] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(3,ld,NPY_FLOAT);
	 	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) {
	      for (iz=0;iz<kz;iz++) {
	        dseo[ix*(kz*ky)+iy*(kz)+iz]=0.;
	      }	
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1])*(ky);
	    z	= *(float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1])*(kz);
	    
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 


	    ix = (int)(x);
            iy = (int)(y);
	    iz = (int)(z);
	    
	    if (ix >= 0 && ix < kx)
	      if (iy >= 0 && iy < ky)
	        if (iz >= 0 && iz < kz)
	          dseo[ix*(kz*ky)+iy*(kz)+iz] = dseo[ix*(kz*ky)+iy*(kz)+iz] + gm*am;
	    
	  }
	  	  
		
	  /* create the subimage */
	  for (k=0;k<kz;k++) {	  
	    for (j=0;j<ky;j++) {
	      for (i=0;i<kx;i++) {
	        *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1]) + (k)*(mat->strides[2])) = (float) dseo[i*(kz*ky)+j*(kz)+k] ;
	      }	
	    }
	  }
	  
	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
      }               






/*********************************/
/* mkmap1dw */
/*********************************/

static PyObject *
      mapping_mkmap1dw(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i; 
	  int	ix1,ix2;
	  float wx1,wx2;
	  int   kx;
	  npy_intp   ld[1];
	  
	  float dseo[kxmax1d];
	  float x,gm,am;
	  
          if (!PyArg_ParseTuple(args,"OOO(i)",&pos,&gmm,&amp,&kx))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  if (kx > kxmax1d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
          mat = (PyArrayObject *) PyArray_SimpleNew(1,ld,NPY_FLOAT);
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 1 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be one dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix1=0;ix1<kx;ix1++) {
	    dseo[ix1]=0.;
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	    
	    
	    if (x>=0 && x<=1)
	      {

	      	x = x*(kx-1);
	
	      	ix1 = (int)(x);
	      	ix2 = ix1+1;
	    
	      	wx1 = 1 - (x-ix1);
	      	wx2 = 1 - (ix2-x);
	    
	      	if (wx1 > 0)
              	  dseo[ix1] = dseo[ix1] + gm*am*wx1;
	      	if (wx2 > 0)
	      	  dseo[ix2] = dseo[ix2] + gm*am*wx2;
		
	      }	
	      
	  }
	  	  
		
	  /* create the subimage */	  
	  for (i=0;i<kx;i++) {
            *(float*)(mat->data + i*(mat->strides[0])) = (float) dseo[i] ;
	  }
	  
	  
	  return PyArray_Return(mat);
      }               






/*********************************/
/* mkmap2dw */
/*********************************/

static PyObject *
      mapping_mkmap2dw(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j; 
	  int	ix1,ix2,iy1,iy2;
	  float wx1,wx2,wy1,wy2;	  
	  int   kx,ky;
	  npy_intp   ld[2];
	  
	  float dseo[kxmax2d][kymax2d];
	  float x,y,z,gm,am;
	  
          if (!PyArg_ParseTuple(args,"OOO(ii)",&pos,&gmm,&amp,&kx,&ky))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  if (kx > kxmax2d || ky > kymax2d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix1=0;ix1<kx;ix1++) {
	    for (iy1=0;iy1<ky;iy1++) { 
	      dseo[ix1][iy1]=0.;
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	    
	    
	    



	    if ((x>=0 && x<=1)&&(y>=0 && y<=1))
	      {

	      	x = x*(kx-1);
	      	ix1 = (int)(x);
	      	ix2 = ix1+1;
	      	wx1 = 1 - (x-ix1);
	      	wx2 = 1 - (ix2-x);

		y = y*(ky-1);
	      	iy1 = (int)(y);
	      	iy2 = iy1+1;
	      	wy1 = 1 - (y-iy1);
	      	wy2 = 1 - (iy2-y);		
		
		
		if (wx1*wy1 > 0)
		  dseo[ix1][iy1] = dseo[ix1][iy1] + gm*am*wx1*wy1;
		if (wx2*wy1 > 0)		
		  dseo[ix2][iy1] = dseo[ix2][iy1] + gm*am*wx2*wy1;
		if (wx1*wy2 > 0)		
		  dseo[ix1][iy2] = dseo[ix1][iy2] + gm*am*wx1*wy2;
		if (wx2*wy2 > 0)		
		  dseo[ix2][iy2] = dseo[ix2][iy2] + gm*am*wx2*wy2;

		
	      }	
	      
	  }



	  	  
		
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[i][j] ;
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }               


/*********************************/
/* mkmap3dw */
/*********************************/

static PyObject *
      mapping_mkmap3dw(self, args)
          PyObject *self;
          PyObject *args;
      {
	  	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j,k; 
	  int	ix1,ix2,iy1,iy2,iz1,iz2;
	  float wx1,wx2,wy1,wy2,wz1,wz2;	
	  int   kx,ky,kz;
	  npy_intp   ld[3];
	  
	  float dseo[kxmax3d][kymax3d][kzmax3d];
	  float x,y,z,gm,am;
	  
          if (!PyArg_ParseTuple(args,"OOO(iii)",&pos,&gmm,&amp,&kx,&ky,&kz))
              return NULL;
	  
	  	    	   
	  /* check max size of matrix */
	  if (kx > kxmax3d || ky > kymax3d || kz > kzmax3d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
	  ld[2] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(3,ld,NPY_FLOAT);
	 	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix1=0;ix1<kx;ix1++) {
	    for (iy1=0;iy1<ky;iy1++) {
	      for (iz1=0;iz1<kz;iz1++) {
	        dseo[ix1][iy1][iz1]=0.;
	      }	
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
	    z	= *(float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
	    
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 




	    if ((x>=0 && x<=1)&&(y>=0 && y<=1)&&(z>=0 && z<=1))
	      {

	      	x = x*(kx-1);
	      	ix1 = (int)(x);
	      	ix2 = ix1+1;
	      	wx1 = 1 - (x-ix1);
	      	wx2 = 1 - (ix2-x);

		y = y*(ky-1);
	      	iy1 = (int)(y);
	      	iy2 = iy1+1;
	      	wy1 = 1 - (y-iy1);
	      	wy2 = 1 - (iy2-y);		
		
		z = z*(kz-1);
	      	iz1 = (int)(z);
	      	iz2 = iz1+1;
	      	wz1 = 1 - (z-iz1);
	      	wz2 = 1 - (iz2-z);		
		
		if (wx1*wy1*wz1 > 0)  
		  dseo[ix1][iy1][iz1] = dseo[ix1][iy1][iz1] + gm*am*wx1*wy1*wz1;
		if (wx1*wy1*wz2 > 0)		  
		  dseo[ix1][iy1][iz2] = dseo[ix1][iy1][iz2] + gm*am*wx1*wy1*wz2;
		if (wx1*wy2*wz1 > 0)		  
		  dseo[ix1][iy2][iz1] = dseo[ix1][iy2][iz1] + gm*am*wx1*wy2*wz1;
		if (wx1*wy2*wz2 > 0)		  
		  dseo[ix1][iy2][iz2] = dseo[ix1][iy2][iz2] + gm*am*wx1*wy2*wz2;
		if (wx2*wy1*wz1 > 0)		  
		  dseo[ix2][iy1][iz1] = dseo[ix2][iy1][iz1] + gm*am*wx2*wy1*wz1;
		if (wx2*wy1*wz2 > 0)		  
		  dseo[ix2][iy1][iz2] = dseo[ix2][iy1][iz2] + gm*am*wx2*wy1*wz2;
		if (wx2*wy2*wz1 > 0)		  
		  dseo[ix2][iy2][iz1] = dseo[ix2][iy2][iz1] + gm*am*wx2*wy2*wz1;
		if (wx2*wy2*wz2 > 0)		  
		  dseo[ix2][iy2][iz2] = dseo[ix2][iy2][iz2] + gm*am*wx2*wy2*wz2;

		
	      }	

          }
		
	  /* create the subimage */
	  for (k=0;k<kz;k++) {	  
	    for (j=0;j<ky;j++) {
	      for (i=0;i<kx;i++) {
	        *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1]) + (k)*(mat->strides[2])) = (float) dseo[i][j][k] ;
	      }	
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }      





/*********************************/
/* mkmap2dsph */
/*********************************/

static PyObject *
      mapping_mkmap2dsph(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  PyArrayObject *rsp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j; 
	  int	ix,iy;
	  int   kx,ky;
	  npy_intp   ld[2];
	  
	  float dseo[kxmax2d][kymax2d];
	  
	  float x,y,z,gm,am,sigma,sigma2,pisig,gaus,sum;
	  int   xin,xfi,yin,yfi,ixx,iyy;
	  int   dkx2,dky2,dkx,dky;
	  
          if (!PyArg_ParseTuple(args,"OOOO(ii)",&pos,&gmm,&amp,&rsp,&kx,&ky))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  if (kx > kxmax2d || ky > kymax2d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) { 
	      dseo[ix][iy]=0.;
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	   = *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    y	   = *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1])*(ky);
      	    gm     = *(float *) (gmm->data + i*(gmm->strides[0])); 
	    am     = *(float *) (amp->data + i*(amp->strides[0])); 
	    sigma  = *(float *) (rsp->data + i*(rsp->strides[0]));
	    



	    /* the size of the subgrid */
	    
	    dkx2 = (int)(3.*sigma);		/* 3 sigma -> 98% volume */
	    dky2 = (int)(3.*sigma);
	    
	    dkx = 2.*dkx2 + 1;
	    dky = 2.*dky2 + 1;



	    if (dkx==1 && dky == 1){		/* the size is 1 */
	    
	      ix = (int)(x);
              iy = (int)(y);

	      if (ix >= 0 && ix < kx) 
	        if (iy >= 0 && iy < ky) 	  
	          dseo[ix][iy] = dseo[ix][iy] + gm*am;
	        
	        
	  
	    
	    } else {
	    
	      ix =  (int)x;   /* center of the sub grid */	 
	      iy =  (int)y;  
	    
	      sigma2 = sigma*sigma;
	      pisig = 1./(2.*PI*sigma2);
	    
	      sum = 0;
	    
	      //printf("%f %d %d %d %d\n",sigma,dkx,dky,kx,ky);
	      
	      
	      /* bornes */
	      
	      xin = ix - dkx2;
	      yin = iy - dky2;
	      xfi = ix + dkx2 + 1;
	      yfi = iy + dky2 + 1;
	      	      
	      if (xin < 0){xin = 0;}
	      if (yin < 0){yin = 0;}
	      if (xfi > kx-1){xfi = kx-1;}
	      if (yfi > ky-1){yfi = ky-1;}
	      	     
	     
	      if (xfi > xin && yfi > yin ) {
	      	             
	        /* loop over the grid */
	      	for (ixx=xin;ixx < xfi;ixx++){
	      	  for (iyy=yin;iyy < yfi;iyy++){
	      	    
	      	    gaus = pisig*exp( 0.5*(-((float)(ix-ixx)/(sigma))*((float)(ix-ixx)/(sigma))    			       
	      				      -((float)(iy-iyy)/(sigma))*((float)(iy-iyy)/(sigma))) );
	      	    sum = sum + gaus;									    			       
	      												    			       
	      	    dseo[ixx][iyy] = dseo[ixx][iyy] + gm*am * gaus;					    			       

 	      	  }
	      	}
	      
	      
	      }
	      
	    } 


          }


	  	  
		
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[i][j] ;
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }               


/*********************************/
/* mkmap2dnsph */
/*********************************/

static PyObject *
      mapping_mkmap2dnsph(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  PyArrayObject *rsp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j; 
	  int	ix,iy;
	  int   kx,ky;
	  npy_intp   ld[2];
	  
	  float *dseo;
	  size_t bytes;
	  
	  float x,y,z,gm,am,sigma,sigma2,pisig,gaus,sum;
	  int   xin,xfi,yin,yfi,ixx,iyy;
	  int   dkx2,dky2,dkx,dky;
	  	  
          if (!PyArg_ParseTuple(args,"OOOO(ii)",&pos,&gmm,&amp,&rsp,&kx,&ky))
              return NULL;
	   
	   
          if(!(dseo = malloc(bytes = kx*ky*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }
 	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	  
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) { 
	      dseo[ix*ky+iy]=0.;
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	   = *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    y	   = *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1])*(ky);
      	    gm     = *(float *) (gmm->data + i*(gmm->strides[0])); 
	    am     = *(float *) (amp->data + i*(amp->strides[0])); 
	    sigma  = *(float *) (rsp->data + i*(rsp->strides[0]));
	    
	    sigma2 = sigma*sigma;
	    pisig = 1./(2.*PI*sigma2);


	    /* the size of the subgrid */
	    
	    dkx2 = (int)(3.*sigma);		/* 3 sigma -> 98% volume */
	    dky2 = (int)(3.*sigma);
	    
	    dkx = 2.*dkx2 + 1;
	    dky = 2.*dky2 + 1;



	    if (dkx==1 && dky == 1){		/* the size is 1 */
	    
	      ix = (int)(x);
              iy = (int)(y);

	      if (ix >= 0 && ix < kx) 
	        if (iy >= 0 && iy < ky) 	  
	          dseo[ix*ky+iy] = dseo[ix*ky+iy] + gm*am;
	        
	        
	  
	    
	    } else {
	    
	      ix =  (int)x;   /* center of the sub grid */	 
	      iy =  (int)y;  
	    

	    
	      sum = 0;
	    
	      //printf("%f %d %d %d %d\n",sigma,dkx,dky,kx,ky);
	      
	      
	      /* bornes */
	      
	      xin = ix - dkx2;
	      yin = iy - dky2;
	      xfi = ix + dkx2 + 1;
	      yfi = iy + dky2 + 1;
	      	      
	      if (xin < 0){xin = 0;}
	      if (yin < 0){yin = 0;}
	      if (xfi > kx-1){xfi = kx-1;}
	      if (yfi > ky-1){yfi = ky-1;}
	      	     
	     
	      if (xfi > xin && yfi > yin ) {
	      	             
	        /* loop over the grid */
	      	for (ixx=xin;ixx < xfi;ixx++){
	      	  for (iyy=yin;iyy < yfi;iyy++){
	      	    
	      	    gaus = pisig*exp( 0.5*(-((float)(ix-ixx)/(sigma))*((float)(ix-ixx)/(sigma))    			       
	      				      -((float)(iy-iyy)/(sigma))*((float)(iy-iyy)/(sigma))) );
	      	    sum = sum + gaus;									    			       
	      												    			       
	      	    dseo[ixx*ky+iyy] = dseo[ixx*ky+iyy] + gm*am * gaus;					    			       

 	      	  }
	      	}
	      
	      
	      }
	      
	    } 


          }


	  	  
		
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[i*ky+j] ;
	    }
	  }
	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
      }               



/*********************************/
/* mkmap2dksph */
/*********************************/

/*

  here, we use the spline kernel to convolve the particule attribute
 
*/

 

#define K1  1.818913635335714
#define K2 10.913481812015714
#define K5  3.637827270672143


double WK2D(double r,double h)
  {

    double u;
    
    u = r/h;
  
    if (u>1)
      return 0.;
      
    if (u>0.5)
      return (1/(h*h)) * K5*pow((1-u),3); 
  
    
    return (1/(h*h)) * ( K1 + K2*(u-1)*u*u );
  
  }


static PyObject *
      mapping_mkmap2dksph(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  PyArrayObject *rsp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j,p; 
	  int	ix,iy;
	  int   kx,ky;
	  npy_intp   ld[2];
	  
	  float *dseo;
	  size_t bytes;
	  
	  double x,y,z,gm,am,h,h2,hx,hy;
	  double xi,yi,xi0,yi0,r,r2;
	  int Nix,Niy;
	  	  
          if (!PyArg_ParseTuple(args,"OOOO(ii)",&pos,&gmm,&amp,&rsp,&kx,&ky))
              return NULL;
	   
	   
          if(!(dseo = malloc(bytes = kx*ky*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }
 	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	  
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) { 
	      dseo[ix*ky+iy]=0.;
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (p = 0; p < pos->dimensions[0]; p++) {
      	    x	   = *(float *) (pos->data + p*(pos->strides[0]) + 0*pos->strides[1])*(kx);		/* scale x between [0,kx] */
      	    y	   = *(float *) (pos->data + p*(pos->strides[0]) + 1*pos->strides[1])*(ky);		/* scale x between [0,ky] */
      	    gm     = *(float *) (gmm->data + p*(gmm->strides[0])); 
	    am     = *(float *) (amp->data + p*(amp->strides[0])); 
	    h      = *(float *) (rsp->data + p*(rsp->strides[0]));
	    
	    	    
	    hx     = h*kx;
	    hy     = h*ky;
	    h      = hx;		/* break the anisothropy */
	    
	    h = dmin(h,0.25*kx);	/* limit h to a fraction of the boxsize */
	    	    
            xi0 = (x - hx);	    	/* bottom left pixel */
	    yi0 = (y - hy);	        /* bottom left pixel */
	    xi0 = dmax(xi0,0.0);
	    yi0 = dmax(yi0,0.0);

	    Nix = (int)(2*hx+1);
	    Niy = (int)(2*hy+1);
	    Nix = dmin(Nix,kx-(int)(xi0));
	    Niy = dmin(Niy,ky-(int)(yi0));

            h2 = h*h;



	    if (h < 1)
	      {
	      	ix = (int)(x);
	      	iy = (int)(y); 
	      
		if (ix >= 0 && ix < kx) 		    	
		  if (iy >= 0 && iy < ky)	    	    	
	      	    dseo[ix*ky+iy] = dseo[ix*ky+iy] + gm*am;
              }
	    else
              {
	      	for (i=0;i<Nix;i++)
	    	  for (j=0;j<Niy;j++)
		    {
	    	  
	    	      xi = xi0 + i;
	    	      yi = yi0 + j;
	    	    
	    	        
	    	      r2 = (xi-x)*(xi-x) +  (yi-y)*(yi-y);
	    	    
	    	      if (r2 < h2)
		        {
	    	    
	    	          r = sqrt(r2);

	    	          ix = (int)(xi);
	    	          iy = (int)(yi);      
	    	          
			
			  dseo[ix*ky+iy] = dseo[ix*ky+iy] + WK2D(r,h)*gm*am;
			
			
			}
                    }

              }

          }


	  	  
		
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[i*ky+j] ;
	    }
	  }
	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
      }               



/*********************************/
/* mkmap3dksph */
/*********************************/

/*

  here, we use the spline kernel to convolve the particule attribute
 
*/

 

#define K1  2.546479089470
#define K2 15.278874536822
#define K5  5.092958178941


double WK3D(double r,double h)
  {

    double u;
    
    u = r/h;
  
    if (u>1)
      return 0.;
      
    if (u>0.5)
      return (1/(h*h*h)) * K5*pow((1-u),3); 
  
    
    return (1/(h*h*h)) * ( K1 + K2*(u-1)*u*u );
  
  }


static PyObject *
      mapping_mkmap3dksph(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  PyArrayObject *rsp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j,k,p; 
	  int	ix,iy,iz;
	  int   kx,ky,kz;
	  npy_intp   ld[3];
	  
	  float *dseo;
	  size_t bytes;
	  
	  double x,y,z,gm,am,h,h2,hx,hy,hz;
	  double xi,yi,zi,xi0,yi0,zi0,r,r2;
	  int Nix,Niy,Niz;
	  	  
          if (!PyArg_ParseTuple(args,"OOOO(iii)",&pos,&gmm,&amp,&rsp,&kx,&ky,&kz))
              return NULL;
	   
	   
          if(!(dseo = malloc(bytes = kx*ky*kz*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }
 	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
	  ld[2] = kz;
          mat = (PyArrayObject *) PyArray_SimpleNew(3,ld,NPY_FLOAT);	  
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) {
	      for (iz=0;iz<kz;iz++) { 
	        dseo[ix*(kz*ky)+iy*(kz)+iz]=0.;
	      }	
	    }
	  }
	  


	  /* full dseo : loop over all points in pos*/
          for (p = 0; p < pos->dimensions[0]; p++) {
      	    x	   = *(float *) (pos->data + p*(pos->strides[0]) + 0*pos->strides[1])*(kx);		/* scale x between [0,kx] */
      	    y	   = *(float *) (pos->data + p*(pos->strides[0]) + 1*pos->strides[1])*(ky);		/* scale x between [0,ky] */
	    z	   = *(float *) (pos->data + p*(pos->strides[0]) + 2*pos->strides[1])*(kz);		/* scale x between [0,kz] */
      	    gm     = *(float *) (gmm->data + p*(gmm->strides[0])); 
	    am     = *(float *) (amp->data + p*(amp->strides[0])); 
	    h      = *(float *) (rsp->data + p*(rsp->strides[0]));
	    
	    hx     = h*kx;
	    hy     = h*ky;
	    hz     = h*kz;
	    h      = hx;		/* break the anisothropy */
	    
	    h = dmin(h,0.25*kx);	/* limit h to a fraction of the boxsize */
	    	    
	    
            xi0 = (x - hx);	    	/* bottom left pixel */
	    yi0 = (y - hy);	        /* bottom left pixel */
	    zi0 = (z - hz);	        /* bottom left pixel */
	    xi0 = dmax(xi0,0.0);
	    yi0 = dmax(yi0,0.0);
	    zi0 = dmax(zi0,0.0);

	    Nix = (int)(2*hx+1);
	    Niy = (int)(2*hy+1);
	    Niz = (int)(2*hz+1);
	    Nix = dmin(Nix,kx-(int)(xi0));
	    Niy = dmin(Niy,ky-(int)(yi0));
	    Niz = dmin(Niz,kz-(int)(zi0));

            h2 = h*h;



	    if (h < 1)
	      {
	      	ix = (int)(x);
	      	iy = (int)(y); 
		iz = (int)(z); 
	      
		if (ix >= 0 && ix < kx) 		    	
		  if (iy >= 0 && iy < ky)
		    if (iz >= 0 && iz < kz)	    	    	
	      	      dseo[ix*(kz*ky)+iy*(kz)+iz] = dseo[ix*(kz*ky)+iy*(kz)+iz] + gm*am;
              }
	    else
              {
	      	for (i=0;i<Nix;i++)
	    	  for (j=0;j<Niy;j++)
		    for (k=0;k<Niz;k++)
		      {
	    	  
	    	        xi = xi0 + i;
	    	        yi = yi0 + j;
			zi = zi0 + k;
	    	    
	    	        
	    	        r2 = (xi-x)*(xi-x) + (yi-y)*(yi-y) + (zi-z)*(zi-z);
	    	    
	    	        if (r2 < h2)
		          {
	    	    
	    	            r = sqrt(r2);

	    	            ix = (int)(xi);
	    	            iy = (int)(yi);   
			    iz = (int)(zi);    
	    	          
			
			    dseo[ix*(kz*ky)+iy*(kz)+iz] = dseo[ix*(kz*ky)+iy*(kz)+iz] + WK3D(r,h)*gm*am;
			
			
			  }
                      }

              }

          }


	  	  
		
	  /* create the subimage */	  
	  for (k=0;k<kz;k++) {	  
	    for (j=0;j<ky;j++) {
	      for (i=0;i<kx;i++) {
	        *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1]) + (k)*(mat->strides[2])) = (float) dseo[i*(kz*ky)+j*(kz)+k] ;
	      }	
	    }
	  }




	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
      }               



/*********************************/
/* mkmap3dnsph */
/*********************************/

static PyObject *
      mapping_mkmap3dnsph(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  PyArrayObject *rsp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j,k; 
	  int	ix,iy,iz;
	  int   kx,ky,kz;
	  npy_intp   ld[3];
	  
	  float *dseo;
	  size_t bytes;
	  
	  float x,y,z,gm,am,sigma,sigma3,pisig,gaus,sum;
	  int   xin,xfi,yin,yfi,zin,zfi,ixx,iyy,izz;
	  int   dkx2,dky2,dkz2,dkx,dky,dkz;
	  	  
          if (!PyArg_ParseTuple(args,"OOOO(iii)",&pos,&gmm,&amp,&rsp,&kx,&ky,&kz))
              return NULL;
	   
	   
          if(!(dseo = malloc(bytes = kx*ky*kz*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }
 	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
	  ld[2] = kz;
          mat = (PyArrayObject *) PyArray_SimpleNew(3,ld,NPY_FLOAT);
	  
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) {
	      for (iz=0;iz<kz;iz++) {
	        dseo[ix*(kz*ky)+iy*(kz)+iz]=0.;
	      }	
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	   = *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    y	   = *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1])*(ky);
      	    z	   = *(float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1])*(kz);
	    
      	    gm     = *(float *) (gmm->data + i*(gmm->strides[0])); 
	    am     = *(float *) (amp->data + i*(amp->strides[0])); 
	    sigma  = *(float *) (rsp->data + i*(rsp->strides[0]));
	    
            sigma3 = sigma*sigma*sigma;
            pisig = 1./(pow(2.*PI,1.5)*sigma3);


	    /* the size of the subgrid */
	    
	    dkx2 = (int)(3.*sigma);		/* 3 sigma -> 98% volume */
	    dky2 = (int)(3.*sigma);
	    dkz2 = (int)(3.*sigma);
	    
	    dkx = 2.*dkx2 + 1;
	    dky = 2.*dky2 + 1;
	    dkz = 2.*dkz2 + 1;



	    if (dkx==1 && dky == 1 && dkz == 1){		/* the size is 1 */
	    
	      ix = (int)(x);
              iy = (int)(y);
              iz = (int)(z);

	      if (ix >= 0 && ix < kx) 
	        if (iy >= 0 && iy < ky) 
		  if (iz >= 0 && iz < kz) 	  
                    dseo[ix*(kz*ky)+iy*(kz)+iz] = dseo[ix*(kz*ky)+iy*(kz)+iz] + gm*am;
	        
	  
	    
	    } else {
	    
	      ix =  (int)x;   /* center of the sub grid */	 
	      iy =  (int)y;  
	      iz =  (int)z;  
	    	    
	      sum = 0;
	    
	      //printf("%f %d %d %d %d\n",sigma,dkx,dky,kx,ky);
	      
	      
	      /* bornes */
	      
	      xin = ix - dkx2;
	      yin = iy - dky2;
	      zin = iz - dkz2;
	      xfi = ix + dkx2 + 1;
	      yfi = iy + dky2 + 1;
	      zfi = iz + dkz2 + 1;
	      	      
	      if (xin < 0){xin = 0;}
	      if (yin < 0){yin = 0;}
	      if (zin < 0){zin = 0;}
	      if (xfi > kx-1){xfi = kx-1;}
	      if (yfi > ky-1){yfi = ky-1;}
	      if (zfi > kz-1){zfi = kz-1;}
	      	     
	     
	      if (xfi > xin && yfi > yin  && zfi > zin) {
	      	             
	        /* loop over the grid */
	      	for (ixx=xin;ixx < xfi;ixx++){
	      	  for (iyy=yin;iyy < yfi;iyy++){
		    for (izz=zin;izz < zfi;izz++){
	      	    
	      	      gaus = pisig*exp( 0.5*(   -((float)(ix-ixx)/(sigma))*((float)(ix-ixx)/(sigma)) - ((float)(iy-iyy)/(sigma))*((float)(iy-iyy)/(sigma)) - ((float)(iz-izz)/(sigma))*((float)(iz-izz)/(sigma))   ) );
	      	      sum = sum + gaus;									    			       
	      												    			       
	      	      dseo[ixx*(kz*ky)+iyy*(kz)+izz] = dseo[ixx*(kz*ky)+iyy*(kz)+izz] + gm*am * gaus;					    			       
                    }
 	      	  }
	      	}
	      
	      
	      }
	      
	    } 


          }


	  	  
		
	  /* create the subimage */	  
	  for (k=0;k<kz;k++) {	  
	    for (j=0;j<ky;j++) {
	      for (i=0;i<kx;i++) {
	        *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1]) + (k)*(mat->strides[2])) = (float) dseo[i*(kz*ky)+j*(kz)+k] ;
	      }	
	    }
	  }

	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
      }               


/*********************************/
/* mkmap2dncub */
/*********************************/

static PyObject *
      mapping_mkmap2dncub(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  PyArrayObject *rsp = NULL;
	  
	  PyArrayObject *mat;
	  
	  int  	n,i,j; 
	  int	ix,iy;
	  int   kx,ky;
	  npy_intp   ld[2];
	  
	  float *dseo;
	  size_t bytes;
	  
	  float x,y,z,gm,am,flux,size;
	  int   xin,xfi,yin,yfi,ixx,iyy;
	  int   dkx2,dky2,dkx,dky;
	  	  
          if (!PyArg_ParseTuple(args,"OOOO(ii)",&pos,&gmm,&amp,&rsp,&kx,&ky))
              return NULL;
	   
	   
          if(!(dseo = malloc(bytes = kx*ky*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }
 	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	  
	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	  n = pos->dimensions[0];		 

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) { 
	      dseo[ix*ky+iy]=0.;
	    }
	  }

	  /* full dseo : loop over all points in pos*/
          for (i = 0; i < pos->dimensions[0]; i++) {
      	    x	   = *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1])*(kx);
      	    y	   = *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1])*(ky);
      	    gm     = *(float *) (gmm->data + i*(gmm->strides[0])); 
	    am     = *(float *) (amp->data + i*(amp->strides[0])); 
	    size   = *(float *) (rsp->data + i*(rsp->strides[0]));
	    



	    /* the size of the subgrid */
	    
	    dkx2 = (int)(size);	     
	    dky2 = (int)(size);
	    
	    dkx = 2*dkx2 + 1;		/* ??? */
	    dky = 2*dky2 + 1;
	    
	    
	    flux = gm*am / ( dkx*dky );



	    if (dkx==1 && dky == 1){		/* the size is 1 */
	    
	      ix = (int)(x);
              iy = (int)(y);

	      if (ix >= 0 && ix < kx) 
	        if (iy >= 0 && iy < ky) 	  
	          dseo[ix*ky+iy] = dseo[ix*ky+iy] + flux;
	        
	        
	  
	    
	    } else {
	    
	      ix =  (int)x;   /* center of the sub grid */	 
	      iy =  (int)y;  
	    
	    	      
	      /* bornes */
	      
	      xin = ix - dkx2;
	      yin = iy - dky2;
	      xfi = ix + dkx2 + 1;
	      yfi = iy + dky2 + 1;
	      	      
	      if (xin < 0){xin = 0;}
	      if (yin < 0){yin = 0;}
	      if (xfi > kx-1){xfi = kx-1;}
	      if (yfi > ky-1){yfi = ky-1;}
	      	     
	     
	      if (xfi > xin && yfi > yin ) {
	      	             
	        /* loop over the grid */
	      	for (ixx=xin;ixx < xfi;ixx++){
	      	  for (iyy=yin;iyy < yfi;iyy++){
	      	    
	      												    			       
	      	    dseo[ixx*ky+iyy] = dseo[ixx*ky+iyy] + flux;					    			       

 	      	  }
	      	}
	      
	      
	      }
	      
	    } 


          }


	  	  
		
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[i*ky+j] ;
	    }
	  }
	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
      }   

/*********************************/
/* mapzero */
/*********************************/

static PyObject *
      mapping_mapzero(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  float xmx,ymx,xc,yc,zc;
	  int view;
	  
	  PyArrayObject *mat;
	  
	  
	  int   kx,ky;
	  int   kxx,kyy;
	  int   kxx2,kyy2;
	  int  	n,i,j; 
	  int	ix,iy,xi,yi,zi;
	  npy_intp   ld[2];
	  
	  float ax,ay,bx,by;  
	  float dseo[kxmax2d][kymax2d];
	  float mm;
	  float x,y,z,gm;
	 	  	         
          if (!PyArg_ParseTuple(args,"OO(ii)(ff)(fff)i",&pos,&gmm,&kx,&ky,&xmx,&ymx,&xc,&yc,&zc,&view))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  
	  if (kx > kxmax2d || ky > kymax2d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	      
	 
	  /* set image dimension */
	 
 	  kxx=kx;						
 	  kyy=ky;						
 	  kxx2=kxx/2;						   
 	  kyy2=kyy/2;						   
 
 	  ax  =kxx2/xmx;					   
 	  ay  =kyy2/ymx; 
	  					   
 	  bx  =kxx2+1.; 					   
 	  by  =kyy2+1.; 	
	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float0");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	 
	  n = pos->dimensions[0];		 


	  /* initialisation of dseo */
	  	  
	  for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) { 
	      dseo[ix][iy]=0.;
	    }
	  }
	  		  	
				  			  
	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 2;
	    xc = xc;
	    yc = zc;
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 1;
	    xc = xc;
	    yc = yc;
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 2;
	    xc = yc;
	    yc = zc;
	  }	  	  


          mm = 0.;

	  /* full dseo : loop over all points in pos*/

          for (i = 0; i < pos->dimensions[0]; i++) {

      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]) -xc;
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]) -yc;
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	          
	    if (x > -xmx && x < xmx) {
	      if (y > -ymx && y < ymx) {
	  		
	  	ix =	   (int)(ax*x + bx) -1;
	  	iy =	   (int)(ay*y + by) -1;
			 
	  	dseo[ix][iy] = dseo[ix][iy] + gm;	/* add in cell */	
		mm = mm + gm;				/* sum the weight */

	      }
	    }	 
	  }

	  
	  /* normalisation */
	  /*
	  if(mm!=0.){
            for (ix=0;ix<kxx;ix++) {
	      for (iy=0;iy<kyy;iy++) {			        
	    	dseo[ix][iy]=dseo[ix][iy]/mm;
	      }						        
	    }	 
	  }   
	  */
	
	  	
	  /* create the subimage */	  

	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	    	      	      
	      *(float*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (float) dseo[i][j] ;
	         
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }               



/*********************************/
/* mapzerosph */
/*********************************/

static PyObject *
      mapping_mapzerosph(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *rsp = NULL;
	  float xmx,ymx,xc,yc,zc,frsp;
	  int view;
	  
	  PyArrayObject *mat;
	  
	  
	  int   kx,ky;
	  int   kxx,kyy;
	  int   kxx2,kyy2;
	  int   dkx2,dky2,dkx,dky;
	  int   ikx,iky;
	  int  	n,i,j; 
	  int	ix,iy,xi,yi,ixx,iyy;
	  int   xin,xfi,yin,yfi;
	  npy_intp   ld[2];
	  
	  float ax,ay,bx,by;  
	  float dseo[kxmax2d][kymax2d];
	  float mm;
	  float x,y,z,gm,sigma,sigma2,pisig,gaus,ds,sum;
	  int *pv;
	 	  
	  
	         
          if (!PyArg_ParseTuple(args, "OOO(ii)(ff)(fff)fi",&pos,&gmm,&rsp,&kx,&ky,&xmx,&ymx,&xc,&yc,&zc,&frsp,&view))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  
	  if (kx > kxmax2d || ky > kymax2d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	      
	 
	  /* set image dimension */
	 
 	  kxx=kx;						
 	  kyy=ky;						
 	  kxx2=kxx/2;						   
 	  kyy2=kyy/2;	
	   
 	  ax  =kxx2/xmx;					   
 	  ay  =kyy2/ymx; 
	  					   
 	  bx  =kxx2+1.; 					   
 	  by  =kyy2+1.; 	
	  	 
	  /* check the size of pos */
	 
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float0");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	 
	  n = pos->dimensions[0];		 


	  /* initialisation of dseo */
	  	  
	  for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) { 
	      dseo[ix][iy]=0.;
	    }
	  }
	  		  
	  
	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 2;
	    xc = xc;
	    yc = zc;
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 1;
	    xc = xc;
	    yc = yc;
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 2;
	    xc = yc;
	    yc = zc;
	  }	  	  

          mm = 0;
          
	  /* full dseo : loop over all points in pos*/

          for (i = 0; i < pos->dimensions[0]; i++) {

      	    x	   = *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]) -xc;
      	    y	   = *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]) -yc;
      	    gm     = *(float *) (gmm->data + i*(gmm->strides[0]));
	    sigma  = *(float *) (rsp->data + i*(rsp->strides[0]));
	    
	    sigma = frsp*sigma;
	    mm = mm+gm;	    
	    
	    /* define the subgrid */
	  
	    /* the size of the subgrid */
	    
	    dkx2 = (int)(ax* 2.*sigma);		/* 3 sigma -> 98% volume */
	    dky2 = (int)(ay* 2.*sigma);
	    
	    dkx = 2.*dkx2 + 1;
	    dky = 2.*dky2 + 1;
	    
	    if (dkx==1 && dky == 1){		/* the size is 1 */
	    
	      if (x > -xmx && x < xmx) {
	        if (y > -ymx && y < ymx) {
	        	  
	          ix =       (int)(ax*x + bx) -1;
	          iy =       (int)(ay*y + by) -1;
	        	   
	          dseo[ix][iy] = dseo[ix][iy] + gm;

	        }
	      } 	  

	    
	    } else {
	    
	      ix =  (int)(ax*x + bx) -1;   /* center of the grid */	 
	      iy =  (int)(ay*y + by) -1;  
	    
	      sigma2 = sigma*sigma;
	      pisig = 1./(2.*PI*sigma2);
	    
	      ds = (1./ax)*(1./ay);  
	      sum = 0;
	    
	      //printf("%f %d %d %d %d\n",sigma,dkx,dky,kxx,kyy);
	      
	      
	      /* bornes */
	      
	      xin = ix - dkx2;
	      yin = iy - dky2;
	      xfi = ix + dkx2 + 1;
	      yfi = iy + dky2 + 1;
	      	      
	      if (xin < 0){xin = 0;}
	      if (yin < 0){yin = 0;}
	      if (xfi > kxx-1){xfi = kxx-1;}
	      if (yfi > kyy-1){yfi = kyy-1;}
	      	     
	     
	      if (xfi > xin && yfi > yin ) {
	      	             
	        /* loop over the grid */
	      	for (ixx=xin;ixx < xfi;ixx++){
	      	  for (iyy=yin;iyy < yfi;iyy++){
	      	    
	      	    gaus = ds*pisig*exp( 0.5*(-((float)(ix-ixx)/(ax*sigma))*((float)(ix-ixx)/(ax*sigma))    			       
	      				      -((float)(iy-iyy)/(ay*sigma))*((float)(iy-iyy)/(ay*sigma))) );
	      	    sum = sum + gaus;									    			       
	      												    			       
	      	    dseo[ixx][iyy] = dseo[ixx][iyy] + gm * gaus;					    			       

 	      	  }
	      	}
	      }
	      
	    }  
	    
	  }
	  
	  
	  /* normalisation */
	  /*
	  if(mm!=0.){
            for (ix=0;ix<kxx;ix++) {
	      for (iy=0;iy<kyy;iy++) {			        
	    	dseo[ix][iy]=dseo[ix][iy]/mm;
	      }						        
	    }	 
	  } 
	  */  
	
	  /* create the subimage */	  

	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	    	      	      
	      *(float*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (float) dseo[i][j] ;
	         
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }      
      
/*********************************/
/* mapone */
/*********************************/

static PyObject *
      mapping_mapone(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  float xmx,ymx,xc,yc,zc;
	  int view;
	  
	  PyArrayObject *mat;
	  
	  
	  int   kx,ky;
	  int   kxx,kyy;
	  int   kxx2,kyy2;
	  int  	n,i,j; 
	  int	ix,iy,xi,yi,zi;
	  npy_intp   ld[2];
	  
	  float ax,ay,bx,by;  
	  float dseo[kxmax2d][kymax2d];
	  float mm[kxmax2d][kymax2d];
	  float x,y,z,gm,am;
	 	  	         
          if (!PyArg_ParseTuple(args,"OOO(ii)(ff)(fff)i",&pos,&gmm,&amp,&kx,&ky,&xmx,&ymx,&xc,&yc,&zc,&view))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  
	  if (kx > kxmax2d || ky > kymax2d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);

	      
	 
	  /* set image dimension */
	 
 	  kxx=kx;						
 	  kyy=ky;						
 	  kxx2=kxx/2;						   
 	  kyy2=kyy/2;						   
 
 	  ax  =kxx2/xmx;					   
 	  ay  =kyy2/ymx; 
	  					   
 	  bx  =kxx2+1.; 					   
 	  by  =kyy2+1.; 	
	  	 
	  /* check the size of pos */
	 
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float0");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	 
	  n = pos->dimensions[0];		 


	  /* initialisation of dseo */
	  	  
	  for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) { 
	      dseo[ix][iy]=0.;
	      mm[ix][iy]=0.;
	    }
	  }
	  		  	  
	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 2;
	    xc = xc;
	    yc = zc; 
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 1;
	    xc = xc;
	    yc = yc; 	  
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 2;
	    xc = yc;
	    yc = zc; 
	  }	  	  


	  /* full dseo : loop over all points in pos*/

          for (i = 0; i < pos->dimensions[0]; i++) {

      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]) -xc;
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]) -yc;
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	          
	    if (x > -xmx && x < xmx) {
	      if (y > -ymx && y < ymx) {
	  		
	  	ix =	   (int)(ax*x + bx) -1;
	  	iy =	   (int)(ay*y + by) -1;
			 
	  	dseo[ix][iy] = dseo[ix][iy] + gm*am;
		mm[ix][iy] = mm[ix][iy] + gm;

	      }
	    }	 
	  }
	  
	  /* normalisation */
          for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) {			        
	      if(mm[ix][iy]!=0){			        
	    	dseo[ix][iy]=dseo[ix][iy]/(float)mm[ix][iy];
	      } 					        
	    }						        
	  }	  
	
	  	
	  /* create the subimage */	  

	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	    	      	      
	      *(float*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (float) dseo[i][j] ;
	         
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }               

/*********************************/
/* mapn */
/*********************************/

static PyObject *
      mapping_mapn(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  float xmx,ymx,xc,yc,zc;
	  int view;
	  
	  PyArrayObject *mat;
	  
	  
	  int   kx,ky;
	  int   kxx,kyy;
	  int   kxx2,kyy2;
	  int  	n,i,j; 
	  int	ix,iy,xi,yi,zi;
	  npy_intp   ld[2];
	  
	  float ax,ay,bx,by;  
	  float dseo[kxmax2d][kymax2d];
	  int nn[kxmax2d][kymax2d];
	  float x,y,z,gm,am;
	  
	  
	 	  	         
          if (!PyArg_ParseTuple(args,"OOO(ii)(ff)(fff)i",&pos,&gmm,&amp,&kx,&ky,&xmx,&ymx,&xc,&yc,&zc,&view))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  
	  if (kx > kxmax2d || ky > kymax2d){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	      
	 
	  /* set image dimension */
	 
 	  kxx=kx;						
 	  kyy=ky;						
 	  kxx2=kxx/2;						   
 	  kyy2=kyy/2;						   
 
 	  ax  =kxx2/xmx;					   
 	  ay  =kyy2/ymx; 
	  					   
 	  bx  =kxx2+1.; 					   
 	  by  =kyy2+1.; 	
	  	 
	  /* check the size of pos */
	 
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float0");
	    return NULL;
	  }
	  	  
	  /* number of particules */ 
	 
	  n = pos->dimensions[0];		 


	  /* initialisation of dseo */
	  	  
	  for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) { 
	      dseo[ix][iy]=0.;
	      nn[ix][iy]=0;
	    }
	  }
	  		  	  
	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 2;
	    xc = xc;
	    yc = zc; 
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 1;
	    xc = xc;
	    yc = yc; 
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 2;
	    xc = yc;
	    yc = zc; 
	  }	  	  


	  /* full dseo : loop over all points in pos*/

          for (i = 0; i < pos->dimensions[0]; i++) {

      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]) -xc;
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]) -yc;
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	          
	    if (x > -xmx && x < xmx) {
	      if (y > -ymx && y < ymx) {
	  		
	  	ix =	   (int)(ax*x + bx) -1;
	  	iy =	   (int)(ay*y + by) -1;
			 
	  	dseo[ix][iy] = dseo[ix][iy] + gm*am;
		nn[ix][iy] = nn[ix][iy] + 1;
	      }
	    }	 
	  }
	  	  

//	  /* check the statistic */
//          for (ix=0;ix<kxx;ix++) {
//	    for (iy=0;iy<kyy;iy++) {			        
//	      if(nn[ix][iy]<=2){			        
//	    	dseo[ix][iy]=0.;
//	      } 					        
//	    }						        
//	  }

		
	  /* create the subimage */	  

	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	    	      	      
	      *(float*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (float) dseo[i][j] ;
	         
	    }
	  }
	  
	  
	  return PyArray_Return(mat);
      }               



/*********************************/
/* mkmap3dnsph */
/*********************************/


#define KERNEL_COEFF_1  2.546479089470	 
#define KERNEL_COEFF_2 15.278874536822  					 
#define KERNEL_COEFF_5  5.092958178941			  



static PyObject *
      mapping_mkmap3dslicesph(self, args)
          PyObject *self;
          PyObject *args;
      {
	  	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  PyArrayObject *rsp = NULL;	
	  
	  
	    
	  PyArrayObject *mat;
	  
          int   kx,ky,kz;
	  float xmin,xmax,ymin,ymax,zmin,zmax;

	  
	  
	  int  	n,i,j,k; 
	  int	ix,iy,iz;
	  npy_intp   ld[2];
	  int   izz;
	  
	  float *dseo;
	  float x,y,z,gm,am,r;
	  float xx,yy,zz;
	  float fx,fy,fz;
	  
	  size_t bytes;
	  
          if (!PyArg_ParseTuple(args,"OOOO(iii)(ff)(ff)(ff)i",&pos,&gmm,&amp,&rsp,&kx,&ky,&kz,&xmin,&xmax,&ymin,&ymax,&zmin,&zmax,&izz))
              return NULL;
	  
	  	    	   
          if(!(dseo = malloc(bytes = kx*ky*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }	
	   

	  /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	 	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) {
	        dseo[ix*ky+iy] = 0.;
	    }
	  }
	  

	  n = pos->dimensions[0];		 


          /* some constants */
          fx = (kx-1)/(xmax-xmin);
	  fy = (ky-1)/(ymax-ymin);
	  fz = (kz-1)/(zmax-zmin); 

           
          /* set xmin,ymin,zmin for each particles */
	 	 
	 
	  /* first slice */
	  int ixx,iyy;
	  int iz1,iz2;
	  float wk;
	  float h,u;
	  float hinv3;
	  iz1 = 0;
	  iz2 = 1;

	  int ixmin, ixmax;
	  int iymin, iymax;
	  int izmin, izmax;

	  
          /* loop over all particles */
          for (i = 0; i < n; i++) 
	    {
	    
              z = *(float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
              h = *(float *) (rsp->data + i*(rsp->strides[0]));
	      
	      izmin = (int)  (((z - h)-zmin)*fz);
	      izmax = (int)  (((z + h)-zmin)*fz);
	      
              izmin = imax(izmin,0);
              izmax = imin(izmax,kz-1);
	      	      

	      if ( (izz>=izmin) && (izz<=izmax) )
	        {
	    		  
     	      	  x = *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
      	      	  y = *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
    
	      	  gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	    
              	  am  = *(float *) (amp->data + i*(amp->strides[0])); 
	      
	      
	      	  ixmin = (int)  (((x - h)-xmin)*fx);
	      	  ixmax = (int)  (((x + h)-xmin)*fx);
	      
              	  ixmin = imax(ixmin,0);
              	  ixmax = imin(ixmax,kx-1);
	      	      
	      	  iymin = (int)  (((y - h)-ymin)*fy);
	      	  iymax = (int)  (((y + h)-ymin)*fy);
	      
              	  iymin = imax(iymin,0);
              	  iymax = imin(iymax,ky-1);
	      
	      
		  hinv3 = 1.0/(h*h*h)  *  (xmax-xmin)/kx * (ymax-ymin)/ky * (zmax-zmin)/kz ;
		  
		  if ((ixmin==ixmax) && (iymin==iymax) && (izmin==izmax))
		    {
		      dseo[ixmin*ky+iymin] = dseo[ixmin*ky+iymin] + gm*am;
		      continue;
		    }
		    		  		  
	      	   
	      	  /* loop over the grid */
	      	  for (ixx=ixmin;ixx <= ixmax;ixx++)
	      	    {
	      	    for (iyy=iymin;iyy <= iymax;iyy++)
		      {
		      	      	      								
			xx = (ixx/fx)+xmin;		/* physical coordinate */
			yy = (iyy/fy)+ymin;
			zz = (izz/fz)+zmin; 	
										
			r = sqrt( (x-xx)*(x-xx) + (y-yy)*(y-yy) + (z-zz)*(z-zz) );	       

			u = r/h;
						
			
			if (u<1)
			  {
			    if(u < 0.5) 							   					  
			      wk = hinv3 * (KERNEL_COEFF_1 + KERNEL_COEFF_2 * (u - 1) * u * u);
			    else
                              wk = hinv3 * KERNEL_COEFF_5 * (1.0 - u) * (1.0 - u) * (1.0 - u);
	      		
	                   			    
			    dseo[ixx*ky+iyy] = dseo[ixx*ky+iyy] + gm*am * wk;  
			  }
		      
		  		      
 	      	      }
	      	    }
	      
	        }
	    	  
            }	  
	  
	  
	  
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[j+i*ky] ;
	    }
	  }	 

	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
	  
	  
	  
      }               

struct points
  {
    int   index;
    float h;
    float z;
    float izmin;
    float izmax;
    int next;
    int prev;
  };



static PyObject *
      mapping_mkmap3dsortedsph(self, args)
          PyObject *self;
          PyObject *args;
      {
	  	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  PyArrayObject *rsp = NULL;	
	  
	  
	    
	  PyArrayObject *mat;
	  
          int   kx,ky,kz;
	  float xmin,xmax,ymin,ymax,zmin,zmax;

	  
	  
	  int  	n,i,j,k; 
	  int	ix,iy,iz;
	  npy_intp   ld[2];
	  int   izz;
	  
	  float *dseo;
	  float x,y,z,gm,am,r;
	  float xx,yy,zz;
	  float fx,fy,fz;
	  
	  struct points *P;
          int   nP;

	  
	  size_t bytes;
	  
          if (!PyArg_ParseTuple(args,"OOOO(iii)(ff)(ff)(ff)",&pos,&gmm,&amp,&rsp,&kx,&ky,&kz,&xmin,&xmax,&ymin,&ymax,&zmin,&zmax))
              return NULL;
	  
	  	    	   
          if(!(dseo = malloc(bytes = kx*ky*sizeof(float))))
           {
    	     printf("failed to allocate memory for `dseo' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }	
	   
	  n = pos->dimensions[0];	   	   
	  
	  /* allocate memory for P */
          if(!(P = malloc(bytes = n*sizeof(struct points))))
           {
    	     printf("failed to allocate memory for `P' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	     return NULL;
           }		  
	  

          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	 	      
	 	  	 
	  /* check the size of pos */
	  if (pos->nd != 2 || pos->descr->type_num != PyArray_FLOAT) {
	    PyErr_SetString(PyExc_ValueError,"argument 1 must be two dimentionnal and of type Float32");
	    return NULL;
	  }
	  	  

	  /* initialisation of dseo */	  
	  for (ix=0;ix<kx;ix++) {
	    for (iy=0;iy<ky;iy++) {
	        dseo[ix*ky+iy] = 0.;
	    }
	  }
	  		 


          /* some constants */
          fx = (kx-1)/(xmax-xmin);
	  fy = (ky-1)/(ymax-ymin);
	  fz = (kz-1)/(zmax-zmin); 

           
          /* set xmin,ymin,zmin for each particles */
	 	 
	 
	  /* first slice */
	  int ixx,iyy;
	  int iz1,iz2;
	  float wk;
	  float h,u;
	  float hinv3;
	  iz1 = 0;
	  iz2 = 1;

	  int ixmin, ixmax;
	  int iymin, iymax;
	  int izmin, izmax;
	  
	  int istart;
	  int nAdded;
	  

	  
	  nP = 0;
	  nAdded = 0;
	  istart = 0;

         
	  for (iz=0;izz<kz;izz++)
            {

            
	      i=nAdded;						      /* index of first particle not added */
	      	      
	      do
	        {
	        
	          if (i==n)					      /* no particles left to add */
	            break;
	          
	          
	          z	= *(float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
	          h	= *(float *) (rsp->data + i*(rsp->strides[0]));
	          izmin = imax((int)  (((z - h)-zmin)*fz),0);
	          izmax = imin((int)  (((z + h)-zmin)*fz),kz-1);
	          
	          
	          if (izmin>izz)				      /* the next particle is not in the slice, do nothing */
	            break;
	          
	        						      /* the particle enter the slice, add it */
	            
	          P[i].index = i;
	          P[i].z     = z;
	          P[i].h     = h;
	          P[i].izmin = izmin;
	          P[i].izmax = izmax;
	
	          /********************************/
	          /* set its position in the list */
	          /********************************/
	
	          /* default, first one */
                  
	          if (nP==0)
	            {
                      P[i].next=-1;
                    }
	          else
	            {
	              P[i].next = istart;
                      P[istart].prev=i;       
	            } 

	          P[i].prev=-1;
	          istart = i;	    
	          
	          	          
	          nAdded++;			    
	          nP++;
	          i++;  	/* move to next particle */
	            
	
	        
	        }
	      while(1);
	

	  
	      /***************************************/
              /* loop over all particles in the list */
	      /***************************************/

	      i = istart;
	      
              //printf("(%d) nP=%d\n",izz,nP);

	      
	      if (nP>0)
	      	do
	      	  {
	      	  
	      		    
		    z	  = P[i].z;
	      	    izmin = P[i].izmin;
              	    izmax = P[i].izmax;
              	    h	  = P[i].h;	  
		    
				    
		    /* do the particle */
		    
		    
		    if(izmax<izz)		/* the part leaves the slice */
		      {
		      
		        
		      
		        
			if (nP==1)
                          {
			    /* do nothing */
			  }
			else
			  {
			
			    			
			    /* remove it from the list */			
			    if (P[i].prev==-1)  				  /* first one */
			      {
			    	istart = P[i].next;
			    	P[istart].prev = -1;
			      }
			    else
			      {  
			    	if (P[i].next==-1)				  /* last one */
			    	  {
			    	    P[P[i].prev].next = -1;
			    	  }
			    	else						  /* one in the middle */
			    	  {
				    P[ P[i].prev ].next = P[i].next;
				    P[ P[i].next ].prev = P[i].prev;
				     	
			    	  }				  
			      }
			
			  }
			  
			nP--;  
			    
			
		      }
		    else	  
		      {        
		    		      
	
    		    	x = *(float *) (pos->data + P[i].index*(pos->strides[0]) + 0*pos->strides[1]);
     	      	    	y = *(float *) (pos->data + P[i].index*(pos->strides[0]) + 1*pos->strides[1]);
      	      
    		    	gm  = *(float *) (gmm->data + P[i].index*(gmm->strides[0]));	  
	      	    	am  = *(float *) (amp->data + P[i].index*(amp->strides[0])); 
              	    
	      	    
	      	    	ixmin = (int)  (((x - h)-xmin)*fx);
	      	    	ixmax = (int)  (((x + h)-xmin)*fx);
	      	    
	      	    	ixmin = imax(ixmin,0);
              	    	ixmax = imin(ixmax,kx-1);
              	    	    
	      	    	iymin = (int)  (((y - h)-ymin)*fy);
	      	    	iymax = (int)  (((y + h)-ymin)*fy);
	      	    
	      	    	iymin = imax(iymin,0);
              	    	iymax = imin(iymax,ky-1);
              	    
	      	    
	      	    	hinv3 = 1.0/(h*h*h)  *  (xmax-xmin)/kx * (ymax-ymin)/ky * (zmax-zmin)/kz ;
	      	    			
	      	    	 
	      	    	/* loop over the grid */
	      	    	for (ixx=ixmin;ixx <= ixmax;ixx++)
	      	    	  {
	      	    	  for (iyy=iymin;iyy <= iymax;iyy++)
	      	    	    {
	      	    								      
	      	    	      xx = (ixx/fx)+xmin;	      /* physical coordinate */
	      	    	      yy = (iyy/fy)+ymin;
	      	    	      zz = (izz/fz)+zmin;     
	      	    								      
	      	    	      r = sqrt( (x-xx)*(x-xx) + (y-yy)*(y-yy) + (z-zz)*(z-zz) );	     
	      
		    	      u = r/h;
	      	    	      
	      	    	      
	      	    	      if (u<1)
	      	    		{
	      	    		  if(u < 0.5)											 
	      	    		    wk = hinv3 * (KERNEL_COEFF_1 + KERNEL_COEFF_2 * (u - 1) * u * u);
	      	    		  else
	      	    		    wk = hinv3 * KERNEL_COEFF_5 * (1.0 - u) * (1.0 - u) * (1.0 - u);
              	    	      
	      	    					  
	      	    		  dseo[ixx*ky+iyy] = dseo[ixx*ky+iyy] + gm*am * wk;  
	      	    		  
	      	    		}
	      	    	    
	      	    			    
	      	    	    }
 	      	    	  }
	      	    
	      	      }

		      
		    i =  P[i].next;	  
			
	      	  }
              	while (i!=-1);    
	      
	  
	    }
	  
	  
	  
	  /* create the subimage */	  
	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	      *(float*)(mat->data + i*(mat->strides[0]) + (j)*(mat->strides[1])) = (float) dseo[j+i*ky] ;
	    }
	  }	 

	  
	  free(dseo);
	  
	  return PyArray_Return(mat);
	  
	  
	  
      }               




/*********************************/
/* create_line */
/*********************************/
/* http://graphics.lcs.mit.edu/~mcmillan/comp136/Lecture6/Lines.html */


static PyObject *
      mapping_create_line(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
	  PyArrayObject *mat = NULL;
	  int x0,y0,x1,y1,color,width;
	  int dy = y1 - y0;								   
	  int dx = x1 - x0;								   
	  int stepx, stepy;	  
	  	 	  	         
          if (!PyArg_ParseTuple(args,"Oiiiii",&mat,&x0,&y0,&x1,&y1,&color))
              return NULL;
	  
	  /* create the output */
	  	    
	  dy = y1 - y0; 							       
	  dx = x1 - x0; 							       
	  
	  width = 1;	
	         
          if (dy < 0) { dy = -dy;  stepy = -width; } else { stepy = width; }  
          if (dx < 0) { dx = -dx;  stepx = -1; } else { stepx = 1; }			   
	  dy <<= 1;									   
      	  dx <<= 1;									   
       
          y0 *= width;  							     
          y1 *= width;  							     
          *(float*)(mat->data + x0*(mat->strides[0]) + y0*mat->strides[1]) = (float) color ;
      	  if (dx > dy) {								   
      	      int fraction = dy - (dx >> 1);						   
              while (x0 != x1) {							   
          	  if (fraction >= 0) {  						   
          	      y0 += stepy;							   
          	      fraction -= dx;							   
          	  }									   
          	  x0 += stepx;  							   
          	  fraction += dy;							   
		  *(float*)(mat->data + x0*(mat->strides[0]) + y0*mat->strides[1]) = (float) color ;
              } 									   
	  } else {									   
              int fraction = dx - (dy >> 1);						   
              while (y0 != y1) {							   
          	  if (fraction >= 0) {  						   
          	      x0 += stepx;							   
          	      fraction -= dy;							   
          	  }									   
          	  y0 += stepy;  							   
          	  fraction += dx;							   
		  *(float*)(mat->data + x0*(mat->strides[0]) + y0*mat->strides[1]) = (float) color ;
              } 									   
	  }										   
	  
	  
	  return Py_BuildValue("i",1);
      }   

/*********************************/
/* create_line */
/*********************************/


static PyObject *
      mapping_create_line2(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *mat;
	  npy_intp   ld[2];   
	  int kx,ky,x1,y1,x2,y2,color;

	  int i;               // loop counter							        
	  int ystep, xstep;    // the step on y and x axis
	  int error;           // the error accumulated during the increment
	  int errorprev;       // *vision the previous value of the error variable
	  int x,y;     	       // the line points
	  int ddy, ddx;        // compulsory variables: the double values of dy and dx
	  int dx ;
	  int dy;	  
	  	 	  	         
          if (!PyArg_ParseTuple(args,"iiiiiii",&kx,&ky,&x1,&y1,&x2,&y2,&color))
              return NULL;
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	  
          y = y1;
	  x = x1;  
	  dx = x2 - x1;
	  dy = y2 - y1;
	  
	  *(short*)(mat->data + x1*(mat->strides[0]) + y1*mat->strides[1]) = color ;
	  // NB the last point can't be here, because of its previous point (which has to be verified)
	  if (dy < 0){
	    ystep = -1;
	    dy = -dy;
	  }else
	    ystep = 1;
	  if (dx < 0){
	    xstep = -1;
	    dx = -dx;
	  }else
	    xstep = 1;
	  ddy = 2 * dy;  // work with double values for full precision
	  ddx = 2 * dx;
	  if (ddx >= ddy){  // first octant (0 <= slope <= 1)
	    // compulsory initialization (even for errorprev, needed when dx==dy)
	    errorprev = error = dx;  // start in the middle of the square
	    for (i=0 ; i < dx ; i++){  // do not use the first point (already done)
	      x += xstep;
	      error += ddy;
	      if (error > ddx){  // increment y if AFTER the middle ( > )
	        y += ystep;
	        error -= ddx;
	        // three cases (octant == right->right-top for directions below):
	        if (error + errorprev < ddx)  // bottom square also
		  *(float*)(mat->data + (x)*(mat->strides[0]) + (y-ystep)*mat->strides[1]) = (float)color ;
	        else if (error + errorprev > ddx)  // left square also
		  *(float*)(mat->data + (x-xstep)*(mat->strides[0]) + (y)*mat->strides[1]) = (float)color ;
	        else{  // corner: bottom and left squares also
		  *(short*)(mat->data + (x)*(mat->strides[0]) + (y-ystep)*mat->strides[1]) = (float)color ;
		  *(short*)(mat->data + (x-xstep)*(mat->strides[0]) + (y)*mat->strides[1]) = (float)color ;
	        }
	      }
	      *(float*)(mat->data + (x)*(mat->strides[0]) + (y)*mat->strides[1]) = (float)color ;
	      errorprev = error;
	    }
	  }else{  // the same as above
	    errorprev = error = dy;
	    for (i=0 ; i < dy ; i++){
	      y += ystep;
	      error += ddx;
	      if (error > ddy){
	        x += xstep;
	        error -= ddy;
	        if (error + errorprev < ddy)
		  *(float*)(mat->data + (x-xstep)*(mat->strides[0]) + (y)*mat->strides[1]) = (float)color ;
	        else if (error + errorprev > ddy)
		  *(float*)(mat->data + (x)*(mat->strides[0]) + (y-ystep)*mat->strides[1]) = (float)color ;
	        else{
		  *(float*)(mat->data + (x-xstep)*(mat->strides[0]) + (y)*mat->strides[1]) = (float)color ;
		  *(float*)(mat->data + (x)*(mat->strides[0]) + (y-ystep)*mat->strides[1]) = (float)color ;
	        }
	      }
	      *(float*)(mat->data + (x)*(mat->strides[0]) + (y)*mat->strides[1]) = (float)color ;
	      errorprev = error;
	    }
	  }

	  
	  return PyArray_Return(mat);
      }   


/*********************************/
/* create_line */
/*********************************/

static PyObject *
      mapping_create_line3(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
	  int kx,ky,x0,y0,x1,y1,color;
	  
	  PyArrayObject *mat;
	  float a,b;
	  int x,y,dx;
	  int n,lx,ly,s0,s1,inv;
	  npy_intp   ld[2];
	  	 	  	         
          if (!PyArg_ParseTuple(args,"iiiiiii",&kx,&ky,&x0,&y0,&x1,&y1,&color))
              return NULL;
	  
          /* create the output */
	  ld[0] = kx;
	  ld[1] = ky;
          mat = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
	  
	  if (x0 == x1 && y0 == y1) {
	    *(float*)(mat->data + (x0)*(mat->strides[0]) + (y0)*mat->strides[1]) = (float) color ;  
	    return Py_BuildValue("i",0);
	  }
	  
	  
          lx = abs(x1-x0);
	  ly = abs(y1-y0);	  
	  
          inv = 0;
	  
	  if (lx < ly) {
	    /* swap x,y */
	    s0 = x0;
	    s1 = x1;
	    x0 = y0;
	    x1 = y1;
	    y0 = s0;
	    y1 = s1;
	    inv = 1;
	  }
	  
	  a = (float)(y0-y1)/(float)(x0-x1);
	  b = (float)(x0*y1 - y0*x1)/(float)(x0-x1);
	  
	 
	  /* dx */
	  if (x1>x0) {dx = 1;} else {dx=-1;}
	  
	  /* main loop */   
	  x = x0;
	  while (x!=x1) {
	    y = (int) (a*(float)x + b);
	    if (inv){
	      *(float*)(mat->data + (y)*(mat->strides[0]) + (x)*mat->strides[1]) = (float)color ;
	      //printf("- %d %d\n",y,x);
	      } else {
	      *(float*)(mat->data + (x)*(mat->strides[0]) + (y)*mat->strides[1]) = (float)color ;
	      //printf("%d %d\n",x,y);   
	    }
	    x = x + dx;
	  }

	  /* last point */
	  if (inv){
	    *(float*)(mat->data + (y1)*(mat->strides[0]) + (x1)*mat->strides[1]) = (float)color ;
	    //printf("- %d %d\n",y1,x1);
	    } else {
	    *(float*)(mat->data + (x1)*(mat->strides[0]) + (y1)*mat->strides[1]) = (float)color ;
	    //printf("%d %d\n",x1,y1);	    
	    
	  }
	  
	  *(float*)(mat->data + (96)*(mat->strides[0]) + (73)*mat->strides[1]) = (float)color ;
	  *(float*)(mat->data + (94)*(mat->strides[0]) + (76)*mat->strides[1]) = (float)color ;
	  *(float*)(mat->data + (92)*(mat->strides[0]) + (79)*mat->strides[1]) = (float)color ;
	  	  
	  return PyArray_Return(mat);
      }   
      
            
/* definition of the method table */      
      
static PyMethodDef mappingMethods[] = {


          {"mkmap1d",   mapping_mkmap1dn, METH_VARARGS,
           "Return a 1d mapping."},

          {"mkmap1dn",  mapping_mkmap1dn, METH_VARARGS,
           "Return a 1d mapping (no limit on the matrix size)."},

          {"mkcic1dn",  mapping_mkcic1dn, METH_VARARGS,
           "Return a 1d cic mapping (no limit on the matrix size)."},


          {"mkmap2d",   mapping_mkmap2dn, METH_VARARGS,
           "Return a 2d mapping."},

          {"mkmap2dn",  mapping_mkmap2dn, METH_VARARGS,
           "Return a 2d mapping (no limit on the matrix size)."},


          {"mkmap3d",   mapping_mkmap3dn, METH_VARARGS,
           "Return a 3d mapping."},

          {"mkmap3dn",  mapping_mkmap3dn, METH_VARARGS,
           "Return a 3d mapping (no limit on the matrix size)."},
	   
	   
	   
          {"mkmap3dslicesph",  mapping_mkmap3dslicesph, METH_VARARGS,
           "Return a 3d slice (sph)."},

          {"mkmap3dsortedsph",  mapping_mkmap3dsortedsph, METH_VARARGS,
           "Return a 3d mapping (sph)."},

          {"mkmap1dw",  mapping_mkmap1dw, METH_VARARGS,
           "Return a 1d mapping (a particle is distributed over 2 nodes)."},

          {"mkmap2dw",  mapping_mkmap2dw, METH_VARARGS,
           "Return a 2d mapping (a particle is distributed over 4 nodes)."},

          {"mkmap3dw",  mapping_mkmap3dw, METH_VARARGS,
           "Return a 3d mapping (a particle is distributed over 8 nodes)."},


          {"mkmap2dsph",  mapping_mkmap2dnsph, METH_VARARGS,
           "Return a 2d smoothed maping."},
	   
          {"mkmap2dksph",  mapping_mkmap2dksph, METH_VARARGS,
           "Return a 2d smoothed maping (use the spline kernel)."},
	   
          {"mkmap3dksph",  mapping_mkmap3dksph, METH_VARARGS,
           "Return a 3d smoothed maping (use the spline kernel)."},
	   

          {"mkmap3dsph",  mapping_mkmap3dnsph, METH_VARARGS,
           "Return a 3d smoothed maping."},

	   
          {"mkmap2dnsph", mapping_mkmap2dnsph, METH_VARARGS,
           "Return a 2d smoothed maping (no limit on the matrix size)."},	   
	   
          {"mkmap2dncub", mapping_mkmap2dncub, METH_VARARGS,
           "Return a 2d smoothed maping (each part. is projected into a cube instead of a sphere)."},	   


	   
          //{"mapzero",  mapping_mapzero, METH_VARARGS,
          // "Return the zero momentum. (obsolete)"},
	   
          //{"mapzerosph",  mapping_mapzerosph, METH_VARARGS,
          // "Return the zero momentum (softned) (obsolete)."},	   
	   	   	   
          //{"mapone",  mapping_mapone, METH_VARARGS,
          // "Return the first momentum (obsolete)."},

          //{"mapn",  mapping_mapn, METH_VARARGS,
          // "Return the first momentum (not normalized) (obsolete)."},



          {"create_line",  mapping_create_line, METH_VARARGS,
           "Add a line in the given matrice using the Bresenham algorithm."},

          {"create_line2",  mapping_create_line2, METH_VARARGS,
           "Add a line in the given matrice using the Bresenham algorithm."},
	   
          {"create_line3",  mapping_create_line3, METH_VARARGS,
           "Add a line in the given matrice using a personal algorithm."},	   
	   	   	   	   
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      
      
void initmapping(void)
      {    
          (void) Py_InitModule("mapping", mappingMethods);	
	  
	  import_array();
      }      
      
