#include <Python.h>
#include <math.h>
#include <numpy/arrayobject.h>


 
static PyObject *
      asciilib_read(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *out = NULL;
	  
	  PyObject *f;
	  PyObject *Py_Line;
	  PyObject *Py_List;
	  PyObject *Py_Float;
	  char *line;
	  
	  int n,m,i,j;

	  //int   *dim;
	  npy_intp dim[2];
	  int   nd;
	  
		  	  
	  /* parse arguments */    
          if (!PyArg_ParseTuple(args, "O(ii)", &f,&n,&m))		
              return Py_BuildValue("i",-1);
	  
	  /* check */    
	  if(!PyFile_CheckExact(f))
	    {
              PyErr_SetString(PyExc_AttributeError, "first argument is not a file.");   
              return NULL;
	    }
	  
	  
	  /* create the output */ 
	  //nd = 2;
	  //if(!(dim = malloc(sizeof(int)*nd)))
	  //  {
          //    PyErr_SetString(PyExc_AttributeError, "Problem when allocating dim");   
          //    return NULL;
	  //  }	 
	  dim[0] = n;
	  dim[1] = m;
	  //out = (PyArrayObject *) PyArray_FromDims(nd,dim,PyArray_FLOAT);
	  //out = (PyArrayObject *) PyArray_FromDims(2,dim,PyArray_FLOAT);
	  out = (PyArrayObject *) PyArray_SimpleNew(2,dim,NPY_FLOAT);
         
	  
	  
	  for (i=0;i<n;i++)
	    {
	      Py_Line = PyFile_GetLine(f,0);	
	      //Py_XINCREF(Py_Line);
	            
	      Py_List = PyUnicode_Split(Py_Line,NULL,m);
	      //Py_XINCREF(Py_List);
	      
	      if (PyList_GET_SIZE(Py_List)!=m)
	        PyErr_SetString(PyExc_AttributeError, "something's wring here."); 
	      
	      for (j=0;j<m;j++)
	        {
	          //printf("*%s* %d %d %d %d\n",PyString_AsString(PyList_GetItem(Py_List,j)),i,j,n,m);	
		  Py_Float = PyFloat_FromString(PyList_GetItem(Py_List,j),NULL);
		  //Py_XINCREF(Py_Float);
		  *(float*)(out->data + i*(out->strides[0]) + (j)*(out->strides[1])) = (float) PyFloat_AsDouble(Py_Float);
		  //Py_XDECREF(Py_Float);
		  Py_CLEAR(Py_Float);
	        }
	      
	      
	      //Py_XDECREF(Py_Line);
	      //Py_XDECREF(Py_List);
	      Py_CLEAR(Py_Line);
	      Py_CLEAR(Py_List);
	      
	      
	    }
	  
	  //free(dim);
	  
	  
	  
	  
	  
	  return PyArray_Return(out);
      }
      







            
/* definition of the method table */      
      
static PyMethodDef asciilibMethods[] = {

          {"read",  asciilib_read, METH_VARARGS,
           "Read ascii file"},
	    
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      

      
void initasciilib(void)
      {    
          (void) Py_InitModule("asciilib", asciilibMethods);	
	  
	  import_array();
      }      
      
