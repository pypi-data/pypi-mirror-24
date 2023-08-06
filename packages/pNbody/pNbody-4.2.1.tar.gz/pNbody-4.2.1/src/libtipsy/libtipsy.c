#include <Python.h>
#include <math.h>
#include <numpy/arrayobject.h>



#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>

#define MAXDIM 3
#define forever for(;;)

typedef float Real;

struct gas_particle {
    Real mass;
    Real pos[MAXDIM];
    Real vel[MAXDIM];
    Real rho;
    Real temp;
    Real hsmooth;
    Real metals ;
    Real phi ;
} ;
extern struct gas_particle *gas_particles;

struct dark_particle {
    Real mass;
    Real pos[MAXDIM];
    Real vel[MAXDIM];
    Real eps;
    Real phi ;
} ;
extern struct dark_particle *dark_particles;

struct star_particle {
    Real mass;
    Real pos[MAXDIM];
    Real vel[MAXDIM];
    Real metals ;
    Real tform ;
    Real eps;
    Real phi ;
} ;
extern struct star_particle *star_particles;

struct dump {
    double time ;
    int nbodies ;
    int ndim ;
    int nsph ;
    int ndark ;
    int nstar ;
} ;
extern struct dump header ;



static double currtime = 0.0;
static off_t currpos = 0L ;
static off_t lastpos = 0L ;
static off_t tempn;
static off_t temppos;
struct dump header  = { 0.0, 0, 0 , 0 , 0, 0};

static double ttime;

struct gas_particle *gas_particles = NULL;
struct dark_particle *dark_particles = NULL;
struct star_particle *star_particles = NULL;

/*
short *mark_gas = NULL;
short *mark_dark = NULL;
short *mark_star = NULL;

SMX box0_smx = NULL;
int *box0_pi = NULL;
*/

#include <rpc/types.h>
#include <rpc/xdr.h>

static XDR xdrs;

int xdr_header()
{
  int pad;
  
  if(xdr_double(&xdrs, &header.time) != TRUE)
    return 0;
  if(xdr_int(&xdrs, &header.nbodies) != TRUE)
    return 0;
  if(xdr_int(&xdrs, &header.ndim) != TRUE)
    return 0;
  if(xdr_int(&xdrs, &header.nsph) != TRUE)
    return 0;
  if(xdr_int(&xdrs, &header.ndark) != TRUE)
    return 0;
  if(xdr_int(&xdrs, &header.nstar) != TRUE)
    return 0;
  if(xdr_int(&xdrs, &pad) != TRUE)
    return 0;
  return 1;
}
int xdr_gas(gas)
struct gas_particle *gas;
{
  if(sizeof(Real) == sizeof(float))
    {
      if(xdr_float(&xdrs, &gas->mass) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->pos[0]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->pos[1]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->pos[2]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->vel[0]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->vel[1]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->vel[2]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->rho) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->temp) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->hsmooth) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->metals) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &gas->phi) != TRUE)
	return 0;
      return 1;
    }
    return 0;
}  

int xdr_dark(dark)
struct dark_particle *dark;
{
  if(sizeof(Real) == sizeof(float))
    {
      if(xdr_float(&xdrs, &dark->mass) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &dark->pos[0]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &dark->pos[1]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &dark->pos[2]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &dark->vel[0]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &dark->vel[1]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &dark->vel[2]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &dark->eps) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &dark->phi) != TRUE)
	return 0;
      return 1;
    }
    return 0;
}  

int xdr_star(star)
struct star_particle *star;
{
  if(sizeof(Real) == sizeof(float))
    {
      if(xdr_float(&xdrs, &star->mass) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->pos[0]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->pos[1]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->pos[2]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->vel[0]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->vel[1]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->vel[2]) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->metals) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->tform) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->eps) != TRUE)
	return 0;
      if(xdr_float(&xdrs, &star->phi) != TRUE)
	return 0;
      return 1;
    }
    return 0;
}  

#define STD_HEADER_SIZE 32
#define STD_GAS_SIZE 48
#define STD_DARK_SIZE 36
#define STD_STAR_SIZE 44

static PyObject * libtipsy_read(PyObject *self, PyObject *args)
{
  
  FILE *infile;
  char title;
  size_t tsize; 
  int old_nstar;
  int i;
  int nread;
  char *filename;
  
  
  if (!PyArg_ParseTuple(args, "s", &filename))
    return NULL;  
  
  
  /* create a dictionary to store header */
  PyObject *header_dict;
  PyObject *header_key;
  PyObject *header_value;
  header_dict = PyDict_New();

    
    
    
  
  /* openfile */
  infile = fopen(filename,"r");
        
  xdrstdio_create(&xdrs, infile, XDR_DECODE); 

  forever {
      if(xdr_header() != 1) {
          printf("<sorry time too large %s, using %f>\n",title,
        		   (float)currtime) ;
          break ;
      }
      if(header.ndim < 2 || header.ndim > 3) {
              printf("<sorry, file has crazy dimension, %s>\n",title) ;
              fseek(infile,0L,0);
              currtime=0.0;
              currpos=0;
              header.nstar = 0;
              return FALSE;
      }
      currtime = header.time ;
      currpos = ftell(infile) - STD_HEADER_SIZE;
      if ( (float)header.time >= (float)ttime ) 
          break ;
      tempn = header.nsph;
      tempn *= STD_GAS_SIZE;
      temppos = tempn;
      tempn = header.ndark;
      tempn *= STD_DARK_SIZE;
      temppos += tempn;
      tempn = header.nstar;
      tempn *= STD_STAR_SIZE;
      temppos += tempn;
      fseek(infile,temppos,1);
  }   
  fseek(infile,currpos,0) ;
  lastpos = currpos ;
  xdr_header();
  

  if(header.ndim < 2 || header.ndim > 3) {
          printf("<sorry, file has crazy dimension, %s>\n",title) ;
          header.nstar = 0;
          fseek(infile,0L,0);
          return FALSE;
  }
  
  
  /* allocate gas particles */
  
  if(gas_particles != NULL) free(gas_particles);
  if(header.nsph != 0) {	      
    tsize = header.nsph;
    tsize *= sizeof(*gas_particles);
      gas_particles = (struct gas_particle *)malloc(tsize);
      if(gas_particles == NULL) {
          printf("<sorry, no memory for gas particles, %s>\n",title) ;
          return FALSE;
      }
  }
  else
    gas_particles = NULL;
    
    
    
  /* allocate dark particles */
    
  if(dark_particles != NULL) free(dark_particles);
  if(header.ndark != 0) {
    tsize = header.ndark;
    tsize *= sizeof(*dark_particles);
      dark_particles = (struct dark_particle *)malloc(tsize);
      if(dark_particles == NULL) {
          printf("<sorry, no memory for dark particles, %s>\n",title) ;
          return FALSE;
      }
  }
  else
    dark_particles = NULL;


  /* allocate star particles */

  if(star_particles != NULL) free(star_particles);
  if(header.nstar != 0) {
    tsize = header.nstar;
    tsize *= sizeof(*star_particles);
      star_particles = (struct star_particle *)malloc(tsize);
      if(star_particles == NULL) {
          printf("<sorry, no memory for star particles, %s>\n",title) ;
          return FALSE;
      }
  }
  else
    star_particles = NULL;




  //printf("time     = %f\n",header.time);
  //printf("nbodies  = %d\n",header.nbodies);
  //printf("ndim     = %d\n",header.ndim);
  

  //printf("nsph     = %d\n",header.nsph);
  //printf("ndark    = %d\n",header.ndark);
  //printf("nstar    = %d\n",header.nstar);

  //printf("%d\n",sizeof(struct dump));
  //printf("%d\n",sizeof(struct gas_particle));
  //printf("%d\n",sizeof(struct dark_particle));
  //printf("%d\n",sizeof(struct star_particle));
  




  for(i = 0; i < header.nsph; ++i) {
      if(!xdr_gas(&gas_particles[i]))
          break;
  }
  if(i != header.nsph)
      printf("<sorry, short read of gas: %d vs %d, %s>\n", i,
             header.nsph, title);

  for(i = 0; i < header.ndark; ++i) {
      if(!xdr_dark(&dark_particles[i]))
          break;
  }
  if(i != header.ndark)
      printf("<sorry, short read of dark: %d vs %d, %s>\n", i,
             header.ndark, title);

  for(i = 0; i < header.nstar; ++i) {
      if(!xdr_star(&star_particles[i]))
          break;
  }
  if(i != header.nstar)
      printf("<sorry, short read of star: %d vs %d, %s>\n", i,
             header.nstar, title);
  
  /*
  currpos = lastpos ;
  fseek(infile,currpos,0) ;
  currtime = header.time ;
  if ((float)ttime != (float)currtime){
      printf("<used time %f, hope you don't mind %s>\n",
             (float)currtime,title);
  }
  */
  
  xdr_destroy(&xdrs);

  
  /* create ouput */
  PyArrayObject  *pos,*vel,*mass,*eps,*phi;
  
  npy_intp   ld[2],ldm[1];
  ld[0] = header.ndark;
  ld[1] = header.ndim;
  ld[0] = header.ndark;
  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
  vel = (PyArrayObject *) PyArray_SimpleNew(2,ld,NPY_FLOAT);
  mass = (PyArrayObject *) PyArray_SimpleNew(1,ld,NPY_FLOAT);
  eps = (PyArrayObject *) PyArray_SimpleNew(1,ld,NPY_FLOAT);
  phi = (PyArrayObject *) PyArray_SimpleNew(1,ld,NPY_FLOAT);
    
    
  
  for (i=0;i<header.ndark;i++)
    {
      *(float*)(pos->data + i*(pos->strides[0]) + (0)*(pos->strides[1]) ) = (float)dark_particles[i].pos[0];
      *(float*)(pos->data + i*(pos->strides[0]) + (1)*(pos->strides[1]) ) = (float)dark_particles[i].pos[1];	  
      *(float*)(pos->data + i*(pos->strides[0]) + (2)*(pos->strides[1]) ) = (float)dark_particles[i].pos[2];	    
      
      *(float*)(vel->data + i*(vel->strides[0]) + (0)*(vel->strides[1]) ) = (float)dark_particles[i].vel[0];
      *(float*)(vel->data + i*(vel->strides[0]) + (1)*(vel->strides[1]) ) = (float)dark_particles[i].vel[1];	  
      *(float*)(vel->data + i*(vel->strides[0]) + (2)*(vel->strides[1]) ) = (float)dark_particles[i].vel[2];	    

      *(float*)(mass->data + i*(mass->strides[0])                        ) = (float)dark_particles[i].mass;	    
      *(float*)(eps->data  + i*(eps->strides[0])                         ) = (float)dark_particles[i].eps;	    
      *(float*)(phi->data  + i*(phi->strides[0])                         ) = (float)dark_particles[i].phi;	    
      
    }  
    


  /* fill in header */  
  
  header_key   = PyString_FromString("time");
  header_value = PyFloat_FromDouble(header.time);
  PyDict_SetItem(header_dict,header_key,header_value);  

  header_key   = PyString_FromString("nbodies");
  header_value = PyInt_FromLong((long)header.nbodies);
  PyDict_SetItem(header_dict,header_key,header_value);  
    
  header_key   = PyString_FromString("ndim");
  header_value = PyInt_FromLong((long)header.ndim);
  PyDict_SetItem(header_dict,header_key,header_value);  
    
  header_key   = PyString_FromString("nsph");
  header_value = PyInt_FromLong((long)header.nsph);
  PyDict_SetItem(header_dict,header_key,header_value);  
    
  header_key   = PyString_FromString("ndark");
  header_value = PyInt_FromLong((long)header.ndark);
  PyDict_SetItem(header_dict,header_key,header_value);  
  
  header_key   = PyString_FromString("nstar");
  header_value = PyInt_FromLong((long)header.nstar);
  PyDict_SetItem(header_dict,header_key,header_value);  
    
    
    
    
  return Py_BuildValue("OOOOOO",header_dict,pos,vel,mass,eps,phi);     
}















static PyMethodDef libtipsyMethods[] = {

          {"read",   libtipsy_read, METH_VARARGS,
           "read a binary tipsy file"},


          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      









PyMODINIT_FUNC initlibtipsy(void)
      {    
          (void) Py_InitModule("libtipsy", libtipsyMethods);	


	  /* needed for numpy */
	  import_array();
      }     








