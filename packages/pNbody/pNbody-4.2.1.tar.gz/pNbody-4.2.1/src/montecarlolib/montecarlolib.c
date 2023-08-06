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



/*********************************/
/* mkmap1d */
/*********************************/

static PyObject *
      montecarlolib_mc1d(self, args)
          PyObject *self;
          PyObject *args;
      {


	  PyArrayObject *mat = NULL;
          PyArrayObject *pos;
	  	  
	  int  	n,i; 
	  int   nx;
	  int   ix;
	  int   irand;
	  
	  float x,p;
	  npy_intp   ld[1];
	  
          if (!PyArg_ParseTuple(args,"Oii",&mat,&n,&irand))
              return NULL;
	   
	  /* get the size of mat */
	  if (mat->nd != 1) 
	    {
	       PyErr_SetString(PyExc_ValueError,"argument 1 must be of dimension 1.");
	       return NULL;
	    }
	  else
	    {  
	      nx = mat->dimensions[0];
	    }
	  	  
	  
	  /* create the output */
	  ld[0]=n;
	  pos = (PyArrayObject *) PyArray_SimpleNew(1,ld,PyArray_FLOAT);
	      
	 	
	  /* init random */
	  srandom(irand);		
		
	  /* now, compute */
	  for (i=0;i<n;i++)
	    {
	    
              do
	        {	    
	    	  x = (float)random()/(float)RAND_MAX;
	    
	    	  ix = (int)(x*(nx-1)); 
	          
		  /* find the corresponding probability */
	      	  p = *(float *) (mat->data + ix*(mat->strides[0]));
	          
		   
	        }
              while(p<(float)random()/(float)RAND_MAX);	      
	      
	      *(float*)(pos->data + i*(pos->strides[0])) = x ;
	      	      
	      
	    }
	  	
		  
	  return PyArray_Return(pos);


	  
      }               






/*********************************/
/* mkmap2d */
/*********************************/

static PyObject *
      montecarlolib_mc2d(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
	  PyArrayObject *mat = NULL;
          PyArrayObject *pos;
	  	  
	  int  	n,i; 
	  int   nx,ny;
	  int   ix,iy;
	  int   irand;
	  
	  float x,y,p;
	  npy_intp   ld[2];
	  
          if (!PyArg_ParseTuple(args,"Oii",&mat,&n,&irand))
              return NULL;
	   
	  /* get the size of mat */
	  if (mat->nd != 2) 
	    {
	       PyErr_SetString(PyExc_ValueError,"argument 1 must be of dimension 2.");
	       return NULL;
	    }
	  else
	    {  
	      nx = mat->dimensions[0];
	      ny = mat->dimensions[1];
	    }
	  	  
	  
	  /* create the output */
	  ld[0]=n;
	  ld[1]=2;
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);
	      
	 	
	  /* init random */
	  srandom(irand);		
		
	  /* now, compute */
	  for (i=0;i<n;i++)
	    {
	    
              do
	        {	    
	    	  x = (float)random()/(float)RAND_MAX;
	    	  y = (float)random()/(float)RAND_MAX;
	    
	    	  ix = (int)(x*(nx-1)); 
	      	  iy = (int)(y*(ny-1));
	          
		  /* find the corresponding probability */
	      	  p = *(float *) (mat->data + ix*(mat->strides[0]) + iy*(mat->strides[1]));
	          
		  //printf("%d %d %g\n",ix,iy,p);
		   
	        }
              while(p<(float)random()/(float)RAND_MAX);	      
	      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = x ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = y ;
	      	      
	      
	    }
	  	
		  
	  return PyArray_Return(pos);
      }               


/*********************************/
/* mkmap3d */
/*********************************/

static PyObject *
      montecarlolib_mc3d(self, args)
          PyObject *self;
          PyObject *args;
      {
	  	  
	  
	  PyArrayObject *mat = NULL;
          PyArrayObject *pos;
	  	  
	  int  	n,i; 
	  int   nx,ny,nz;
	  int   ix,iy,iz;
	  int   irand;
	  
	  float x,y,z,p;
	  npy_intp   ld[2];
	  
          if (!PyArg_ParseTuple(args,"Oii",&mat,&n,&irand))
              return NULL;
	   
	  /* get the size of mat */
	  if (mat->nd != 2) 
	    {
	       PyErr_SetString(PyExc_ValueError,"argument 1 must be of dimension 2.");
	       return NULL;
	    }
	  else
	    {  
	      nx = mat->dimensions[0];
	      ny = mat->dimensions[1];
	      nz = mat->dimensions[2];
	    }
	  	  
	  
	  /* create the output */
	  ld[0]=n;
	  ld[1]=3;
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);
	      
	 	
	  /* init random */
	  srandom(irand);		
		
	  /* now, compute */
	  for (i=0;i<n;i++)
	    {
	    
              do
	        {	    
	    	  x = (float)random()/(float)RAND_MAX;
	    	  y = (float)random()/(float)RAND_MAX;
		  z = (float)random()/(float)RAND_MAX;
	    
	    	  ix = (int)(x*(nx-1)); 
	      	  iy = (int)(y*(ny-1));
		  iz = (int)(z*(nz-1));
	          
		  /* find the corresponding probability */
	      	  p = *(float *) (mat->data + ix*(mat->strides[0]) + iy*(mat->strides[1]) + iz*(mat->strides[2]));
	          
		   
	        }
              while(p<(float)random()/(float)RAND_MAX);	      
	      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = x ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = y ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = z ;
	      	      
	      
	    }
	  	
		  
	  return PyArray_Return(pos);	  

      }               






      
            
/* definition of the method table */      
      
static PyMethodDef montecarlolibMethods[] = {

          {"mc1d",  montecarlolib_mc1d, METH_VARARGS,
           "Return a 1d monte carlo distribution."},

          {"mc2d",  montecarlolib_mc2d, METH_VARARGS,
           "Return a 2d monte carlo distribution."},

          {"mc3d",  montecarlolib_mc3d, METH_VARARGS,
           "Return a 3d monte carlo distribution."},
	   
	   	   	   	   
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      
      
void initmontecarlolib(void)
      {    
          (void) Py_InitModule("montecarlolib", montecarlolibMethods);	
	  
	  import_array();
      }      
      
