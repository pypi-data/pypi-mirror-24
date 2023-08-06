#include <Python.h>
#include <math.h>
#include <numpy/arrayobject.h>

/*********************************/
/* Integration kernel for da     */
/*********************************/


struct kernelparam
{
  float Omega0;
  float OmegaLambda;
  float Hubble;
};

float kernel(float a, struct kernelparam param)
{
  float h;

  h = param.Omega0 / (a * a * a) + (1 - param.Omega0 - param.OmegaLambda) / (a * a) + param.OmegaLambda;
  h = param.Hubble * sqrt(h);
  
  return 1 / (h * a);
}



/*********************************/
/* some nr functions             */
/*********************************/

#define FUNC(x,y) ((*func)(x,y))


float trapzd(float (*func)(float,struct kernelparam param), struct kernelparam param, float a, float b, int n)
{
	float x,tnm,sum,del;
	static float s;
	int it,j;

	if (n == 1) {
		return (s=0.5*(b-a)*(FUNC(a,param)+FUNC(b,param)));
	} else {
		for (it=1,j=1;j<n-1;j++) it <<= 1;
		tnm=it;
		del=(b-a)/tnm;
		x=a+0.5*del;
		for (sum=0.0,j=1;j<=it;j++,x+=del) sum += FUNC(x,param);
		s=0.5*(s+(b-a)*sum/tnm);
		return s;
	}
}

float qsimp(float (*func)(float,struct kernelparam param), struct kernelparam param, float a, float b, float eps, int jmax)
{
	float trapzd(float (*func)(float,struct kernelparam param), struct kernelparam param, float a, float b, int n);
	int j;
	float s,st,ost=0.0,os=0.0;

	for (j=1;j<=jmax;j++) {
		st=trapzd(func,param,a,b,j);
		s=(4.0*st-ost)/3.0;
		if (j > 5)
			if (fabs(s-os) < eps*fabs(os) ||
				(s == 0.0 && os == 0.0)) return s;
		os=s;
		ost=st;
	}
	printf("Too many steps in routine qsimp\n");
	return 0.0;
}




/*********************************/
/* Age_a                         */
/*********************************/
      
         
      
static PyObject *
      cosmolib_Age_a(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *as;
	  PyArrayObject *ts;
	  float Omega0,OmegaLambda,Hubble;
	  float	a;
	  float t;
	  int i;
	  struct kernelparam param;
	  /* parse arguments */    
	       
	        
          if (!PyArg_ParseTuple(args, "Offf", &as,&Omega0,&OmegaLambda,&Hubble))		
              return NULL;
	  
	      
	  /* create output */
	  //ts = (PyArrayObject *) PyArray_FromDims(as->nd,as->dimensions,as->descr->type_num);
	  ts = (PyArrayObject *) PyArray_SimpleNew(as->nd,as->dimensions,as->descr->type_num);                   
          /* param */
	  param.Omega0 = Omega0;
	  param.OmegaLambda = OmegaLambda;
	  param.Hubble = Hubble;
	  
	  
	      
	  for (i = 0; i < as->dimensions[0]; i++)   
	    {    
	    
	      a = *(double *)(as->data + i*(as->strides[0]));
	     
	      if (a<1e-6)
	        a = 1e-6;   
	      
              t = qsimp(kernel,param,(float)a,(float)1., 1e-6, 100);
	      
	      *(double *)(ts->data + i*(ts->strides[0])) = t;
	      
	      
	    }  


	  return PyArray_Return(ts);
      }
      


            
/* definition of the method table */      
      
static PyMethodDef cosmolibMethods[] = {

          {"Age_a",  cosmolib_Age_a, METH_VARARGS,
           "Return age of the univers as a function of a (expansion factor)."},  

 
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      

      
void initcosmolib(void)
      {    
          (void) Py_InitModule("cosmolib", cosmolibMethods);	
	  
	  import_array();
      }      
      
