#include <Python.h>
#include <math.h>
#include <numpy/arrayobject.h>

#define TO_DOUBLE(a)        ( (PyArrayObject*) PyArray_CastToType(a, PyArray_DescrFromType(NPY_DOUBLE)  ,0) )


#define NT 10



double tt[NT]={1.0e+01, 1.0e+02, 1.0e+03, 1.0e+04, 1.3e+04, 2.1e+04,3.4e+04, 6.3e+04, 1.0e+05, 1.0e+09};
double mt[NT]={1.18701555, 1.15484424,1.09603514, 0.9981496, 0.96346395, 0.65175895,0.6142901,  0.6056833, 0.5897776,  0.58822635};
double unr[NT];



double MeanWeightT(double T)
  {
  
    /* mean molecular weight as a function of the Temperature */
    
    double logt;
    double ttt;
    double slope;
    double mu;
    
    int j;

    logt = log(T);
    ttt = exp(logt);    
  
    if (ttt<tt[0])
      j = 1;
    else  
      for (j=1;j<NT;j++)
    	if ( (ttt > tt[j-1]) && (ttt <= tt[j]) )
    	  break;

    slope = log(mt[j] / mt[j-1]) / log(tt[j] / tt[j-1]);
    mu = exp(slope * (logt - log(tt[j])) + log(mt[j]));

  
    return mu;
  
  }



double UNt(double T)
  {
    return T/MeanWeightT(T);
  }




double Tun(double UN)
  {
  
    /* return T for a given normalized energy */
    
    double logu;
    double uuu;
    double slope;
    double T;
    
    int j;

    logu = log(UN);
    uuu = exp(logu);
        
  
    if (uuu<unr[0])
      j = 1;
    else
      for (j=1;j<NT;j++)
    	if ((uuu > unr[j-1]) && (uuu <= unr[j]))
    	  break;

    slope = log(tt[j] / tt[j-1]) / log(unr[j] / unr[j-1]);
    T = exp(slope * (logu - log(unr[j])) + log(tt[j]));
    
    
    return T;
  
  }





static PyObject *
      thermodynlib_MeanWeightT(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  
	  PyObject *T;	
	  PyArrayObject *Ta,*mus;	  
	  double mu;  
	  
	  int i;
	  
	  /* parse arguments */    	      
          if (!PyArg_ParseTuple(args, "O", &T))		
              return NULL;
	      
	      
          /* a scalar */
	  if (PyArray_IsAnyScalar(T))
	    {
	      mu = MeanWeightT(PyFloat_AsDouble(T));
	      return Py_BuildValue("d",mu);
	    }		
	  
	  /* an array scalar */  
	  if (PyArray_Check(T))
	    {
	      
	      /* convert into array */        
	      Ta   = (PyArrayObject*) T;
	  		 
	      /* convert arrays to double */
	      Ta   = TO_DOUBLE(Ta);
	    
              /* create output */
	      mus  = (PyArrayObject *) PyArray_SimpleNew(Ta->nd,Ta->dimensions,NPY_DOUBLE);
	    
              for (i=0;i<Ta->dimensions[0];i++)
                *(double *)(mus->data + (i)*(mus->strides[0])) = MeanWeightT(*(double *)(Ta->data   + (i)*(Ta->strides[0])));
            
	    return PyArray_Return(mus);

	  
	     }
	  
	      
	    

	  return Py_BuildValue("i",-1);
      }



   
      
static PyObject *
      thermodynlib_Tun(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  
	  PyObject *UN;
	  PyArrayObject *UNa,*Ts;
	  double T;
	  
	  int i;
	  
	  
	  /* parse arguments */    	      
          if (!PyArg_ParseTuple(args, "O", &UN))		
              return NULL;
	      
	      
          /* a scalar */
	   if (PyArray_IsAnyScalar(UN))
	     {
	       T = Tun(PyFloat_AsDouble(UN));
	       return Py_BuildValue("d",T);
	     }  	 
	      


	  /* an array scalar */  
	  if (PyArray_Check(UN))
	    {
	      
	      /* convert into array */        
	      UNa   = (PyArrayObject*) UN;
	  		 
	      /* convert arrays to double */
	      UNa   = TO_DOUBLE(UNa);
	    
              /* create output */
	      Ts  = (PyArrayObject *) PyArray_SimpleNew(UNa->nd,UNa->dimensions,NPY_DOUBLE);
	    
              for (i=0;i<UNa->dimensions[0];i++)
                *(double *)(Ts->data + (i)*(Ts->strides[0])) = Tun(*(double *)(UNa->data   + (i)*(UNa->strides[0])));
            
	    return PyArray_Return(Ts);

	  
	     }
	  
	      
	    

	  return Py_BuildValue("i",-1);




      }
      










            
/* definition of the method table */      
      
static PyMethodDef thermodynlibMethods[] = {

          {"MeanWeightT",  thermodynlib_MeanWeightT, METH_VARARGS,
           "Compute the mean weight for a given temperature."},  
	   
          {"Tun",  thermodynlib_Tun, METH_VARARGS,
           "Compute temperature from the normalized specific energy."},  


	    
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      

      
void initthermodynlib(void)
      {    
          (void) Py_InitModule("thermodynlib", thermodynlibMethods);	
	  
	  import_array();
	  
	  /* init unr */
	  int i;
	  for (i=0;i<NT;i++)
	     unr[i] = UNt(tt[i]);
	  
      }      
      
