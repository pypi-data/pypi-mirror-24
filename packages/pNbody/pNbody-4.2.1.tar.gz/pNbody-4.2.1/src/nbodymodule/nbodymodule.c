#include <Python.h>
#include <math.h>
#include <numpy/arrayobject.h>

#define kxmax 512
#define kymax 512
#define PI 3.14159265358979

      
/*********************************/
/* angular momentum              */
/*********************************/
      
static PyObject *
      nbody_am(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  PyArrayObject *vel;
	  PyArrayObject *mas;
	  PyArrayObject *ltot;
	  
	  int	i;
	  float *x,*y,*z;
	  float *vx,*vy,*vz;
	  float *m;
	  	  
	  float lx,ly,lz;
	  npy_intp   ld[1];
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOO", &pos , &vel, &mas))		
              return NULL;
	    
	  /* dimension of the output in each dimension */  

	  ld[0]=3;
	      
	  lx = 0.;
	  ly = 0.;
	  lz = 0.;	
	  	      
      	  /* loops over all elements */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

                x  = (float *) (pos->data + i*(pos->strides[0])			   );
		y  = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z  = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
		
                vx = (float *) (vel->data + i*(vel->strides[0])                    );
		vy = (float *) (vel->data + i*(vel->strides[0]) + 1*vel->strides[1]);
		vz = (float *) (vel->data + i*(vel->strides[0]) + 2*vel->strides[1]);	
		
		m  = (float *) (mas->data + i*(mas->strides[0])                    ); 
				
	      	lx = lx +  *m * (*y * *vz - *z * *vy);
	      	ly = ly +  *m * (*z * *vx - *x * *vz);
	      	lz = lz +  *m * (*x * *vy - *y * *vx);
      	  }
	  	  
	  /* create a NumPy object */	  
	  //ltot = (PyArrayObject *) PyArray_FromDims(1,ld,PyArray_FLOAT);
	  ltot = (PyArrayObject *) PyArray_SimpleNew(1,ld,NPY_FLOAT); 
	  	  	
	  *(float *)(ltot->data 		      )  = lx;
	  *(float *)(ltot->data +   (ltot->strides[0]))  = ly;
	  *(float *)(ltot->data + 2*(ltot->strides[0]))  = lz;
	        	  
	  return PyArray_Return(ltot);
      }

/*********************************/
/* angular momentum  in x,y,z    */
/*********************************/
      
static PyObject *
      nbody_amxyz(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  PyArrayObject *vel;
	  PyArrayObject *mas;
	  PyArrayObject *lxyz;
	  
	  int	i;
	  float *x,*y,*z;
	  float *vx,*vy,*vz;
	  float *m;
	  	  
	  float lx,ly,lz;
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOO", &pos , &vel, &mas))		
              return NULL;
	    
          /* create a NumPy object similar to the input */
	  lxyz = (PyArrayObject *) PyArray_SimpleNew(pos->nd,pos->dimensions,pos->descr->type_num);  
	  	      
      	  /* loops over all elements */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

                x  = (float *) (pos->data + i*(pos->strides[0])			   );
		y  = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z  = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
		
                vx = (float *) (vel->data + i*(vel->strides[0])                    );
		vy = (float *) (vel->data + i*(vel->strides[0]) + 1*vel->strides[1]);
		vz = (float *) (vel->data + i*(vel->strides[0]) + 2*vel->strides[1]);	
		
		m  = (float *) (mas->data + i*(mas->strides[0])                    ); 
				
	      	lx = *m * (*y * *vz - *z * *vy);
	      	ly = *m * (*z * *vx - *x * *vz);
	      	lz = *m * (*x * *vy - *y * *vx);
		
                *(float *)(lxyz->data + i*(lxyz->strides[0]) + 0*lxyz->strides[1])  = lx;
	        *(float *)(lxyz->data + i*(lxyz->strides[0]) + 1*lxyz->strides[1])  = ly;
	        *(float *)(lxyz->data + i*(lxyz->strides[0]) + 2*lxyz->strides[1])  = lz;
      	  }
	  	  

	        	  
	  return PyArray_Return(lxyz);
      }

/******************************************/
/* specific angular momentum  in x,y,z    */
/******************************************/
      
static PyObject *
      nbody_samxyz(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  PyArrayObject *vel;
	  PyArrayObject *mas;
	  PyArrayObject *lxyz;
	  
	  int	i;
	  float *x,*y,*z;
	  float *vx,*vy,*vz;
	  float *m;
	  	  
	  float lx,ly,lz;
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOO", &pos , &vel, &mas))		
              return NULL;
	    
          /* create a NumPy object similar to the input */
          npy_intp   ld[2];
          ld[0]=pos->dimensions[0];
          ld[1]=pos->dimensions[1];
          //lxyz = (PyArrayObject *) PyArray_FromDims(pos->nd,ld,pos->descr->type_num);
	  lxyz = (PyArrayObject *) PyArray_SimpleNew(pos->nd,ld,pos->descr->type_num); 	   
	  	      
      	  /* loops over all elements */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

                x  = (float *) (pos->data + i*(pos->strides[0])			   );
		y  = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z  = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
		
                vx = (float *) (vel->data + i*(vel->strides[0])                    );
		vy = (float *) (vel->data + i*(vel->strides[0]) + 1*vel->strides[1]);
		vz = (float *) (vel->data + i*(vel->strides[0]) + 2*vel->strides[1]);	
		
		m  = (float *) (mas->data + i*(mas->strides[0])                    ); 
				
	      	lx = (*y * *vz - *z * *vy);
	      	ly = (*z * *vx - *x * *vz);
	      	lz = (*x * *vy - *y * *vx);
		
                *(float *)(lxyz->data + i*(lxyz->strides[0]) + 0*lxyz->strides[1])  = lx;
	        *(float *)(lxyz->data + i*(lxyz->strides[0]) + 1*lxyz->strides[1])  = ly;
	        *(float *)(lxyz->data + i*(lxyz->strides[0]) + 2*lxyz->strides[1])  = lz;
      	  }
	  	  

	        	  
	  return PyArray_Return(lxyz);
      }

      
/*********************************/       
/* potential in a specific point */
/*********************************/
      
static PyObject *
      nbody_potential(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  PyArrayObject *mas;
	  PyArrayObject *xpos;
	  float eps, eps2;
	  

	  int	i;
	  float *x,*y,*z;
	  float *m;
	  float *xx,*yy,*zz;
	  float pot,dx;
	  	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOOf", &pos, &mas, &xpos, &eps))		
              return NULL;
	      
	      
	  /* read the position */  
	  	  
          xx  = (float *) (xpos->data		           );   
	  yy  = (float *) (xpos->data  + 1*xpos->strides[0]);
	  zz  = (float *) (xpos->data  + 2*xpos->strides[0]); 
	  
	  pot = 0.;
	  eps2= eps * eps;
	  	      
      	  /* loops over all elements */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

                x  = (float *) (pos->data + i*(pos->strides[0])			   );
		y  = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z  = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
				
		m  = (float *) (mas->data + i*(mas->strides[0])                    ); 
								
		dx = (*x - *xx)*(*x - *xx) + (*y - *yy)*(*y - *yy) + (*z - *zz)*(*z - *zz);
		if (dx>0)  /* avoid self potential */		  
		  { 
		    dx = sqrt(dx+ eps2);
		    pot = pot - *m/dx;
		  }		
      	  }
	  	  
	        	  
	  return Py_BuildValue("f",pot);
      }    

/*********************************/       
/* acceleration in a specific point */
/*********************************/
      
static PyObject *
      nbody_acceleration(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  PyArrayObject *mas;
	  PyArrayObject *xpos;
	  float eps, eps2;
	  

	  int	i;
	  float *x,*y,*z;
	  float *m;
	  float *xx,*yy,*zz;
	  float ax,ay,az,dx,dy,dz,r,r2,fac;
	  	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOOf", &pos, &mas, &xpos, &eps))		
              return NULL;
	      
	      
	  /* read the position */  
	  	  
          xx  = (float *) (xpos->data		           );   
	  yy  = (float *) (xpos->data  + 1*xpos->strides[0]);
	  zz  = (float *) (xpos->data  + 2*xpos->strides[0]); 
	  
	  ax = 0.;
	  ay = 0.;
	  az = 0.;
	  eps2= eps * eps;
	  	      
      	  /* loops over all elements */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

                x  = (float *) (pos->data + i*(pos->strides[0])			   );
		y  = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z  = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
		
		
		
		m  = (float *) (mas->data + i*(mas->strides[0])                    ); 
		
		
		dx = (*x - *xx);
		dy = (*y - *yy);
		dz = (*z - *zz);
		
		r2 = dx*dx + dy*dy + dz*dz;	
		
		if (r2>0)  /* avoid self force */
		  {		
		    fac = *m/pow(r2+eps2 ,3.0/2.0);
				
		    ax += dx*fac;
		    ay += dy*fac;
		    az += dz*fac;
		    
		  }  
		  
      	  }
	  	  	  	        	  
	  return Py_BuildValue("fff",ax,ay,az);
      }    
        
/**************************/ 
/* total potential energy */
/**************************/ 
      
static PyObject *
      nbody_epot(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  PyArrayObject *mas;
	  float eps, eps2;
	  

	  int	i,j;
	  float *x1,*y1,*z1;
	  float *x2,*y2,*z2;
	  float *m1,*m2;
	  float pot,potj,dx;
	  	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOf", &pos, &mas, &eps))		
              return NULL;
	      
	  
	  pot = 0.;
	  eps2= eps * eps;
	  	      
      	  /* loops over all elements */
      	  for (i = 0; i < pos->dimensions[0]; i++) {
	  
            x1  = (float *) (pos->data + i*(pos->strides[0])			       );    
	    y1  = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
	    z1  = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);    
	
	    m1  = (float *) (mas->data + i*(mas->strides[0])			); 	     
	  
	    potj = 0.;
	  
	    for (j = 0; j < pos->dimensions[0]; j++) {
	  
	      if (i!=j){
                x2  = (float *) (pos->data + j*(pos->strides[0])  			 );		      
	        y2  = (float *) (pos->data + j*(pos->strides[0]) + 1*pos->strides[1]);
	        z2  = (float *) (pos->data + j*(pos->strides[0]) + 2*pos->strides[1]);	      
	
	        m2  = (float *) (mas->data + j*(mas->strides[0])  		  ); 
	        	      
	        	      
	        dx = sqrt((*x1 - *x2)*(*x1 - *x2) + (*y1 - *y2)*(*y1 - *y2) + (*z1 - *z2)*(*z1 - *z2) + eps2);
	        potj = potj - *m2/dx;
		
              }
	    }	
	    pot = pot + *m1*potj; 
      	  }
	        	  
	  return Py_BuildValue("f",0.5*pot);
      }            
      
/*************************/       
/* rotx                  */
/*************************/ 
      
static PyObject *
      nbody_rotx(self, args)
          PyObject *self;
          PyObject *args;
      {
          float theta;
          PyArrayObject *pos;
	  PyArrayObject *rpos;
	  
	  float cs,ss;
          float xs;
	  float *x,*y,*z;
	  float rx,ry,rz;
	  int i;
	            
          if (!PyArg_ParseTuple(args, "fO", &theta, &pos))
              return NULL;
        
          cs = cos(theta);
          ss = sin(theta);
	  	  
	  /* create a NumPy object similar to the input */
          npy_intp   ld[2];
          ld[0]=pos->dimensions[0];
          ld[1]=pos->dimensions[1];
          //rpos = (PyArrayObject *) PyArray_FromDims(pos->nd,ld,pos->descr->type_num); 
	  rpos = (PyArrayObject *) PyArray_SimpleNew(pos->nd,ld,pos->descr->type_num); 	  
	  
      	  /* loop over elements  */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

	        x = (float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
		y = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
		
	      	xs = cs* *y - ss* *z;
				
		rx = *x;
	      	ry = xs;
		rz = ss* *y + cs* *z;
		
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 0*rpos->strides[1])  = rx;
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 1*rpos->strides[1])  = ry;
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 2*rpos->strides[1])  = rz;
				
      	  }
	  	  
	  return PyArray_Return(rpos);
      }      
 
 
/*************************/       
/* roty                  */
/*************************/   
    
static PyObject *
      nbody_roty(self, args)
          PyObject *self;
          PyObject *args;
      {
          float theta;
          PyArrayObject *pos;
	  PyArrayObject *rpos;
	  
	  float cs,ss;
          float xs;
	  float *x,*y,*z;
	  float rx,ry,rz;
	  int i;
	            
          if (!PyArg_ParseTuple(args, "fO", &theta, &pos))
              return NULL;
        
          cs = cos(theta);
          ss = sin(theta);
	  
	  
	  /* create a NumPy object similar to the input */
          npy_intp   ld[2];
          ld[0]=pos->dimensions[0];
          ld[1]=pos->dimensions[1];
          //rpos = (PyArrayObject *) PyArray_FromDims(pos->nd,ld,pos->descr->type_num);
	  rpos = (PyArrayObject *) PyArray_SimpleNew(pos->nd,ld,pos->descr->type_num);
	  
      	  /* loop over elements  */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

	        x = (float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
		y = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
		
	      	xs =  cs* *x + ss* *z;
				
		rx = xs;
	      	ry = *y;
		rz = -ss* *x + cs* *z;
		
		
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 0*rpos->strides[1])  = rx;
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 1*rpos->strides[1])  = ry;
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 2*rpos->strides[1])  = rz;		
		
      	  }
	  	  
	  return PyArray_Return(rpos);
      }        
      
      
/*************************/      
/* rotz                  */
/*************************/
      
static PyObject *
      nbody_rotz(self, args)
          PyObject *self;
          PyObject *args;
      {
          float theta;
          PyArrayObject *pos;
	  PyArrayObject *rpos;
	  
	  float cs,ss;
          float xs;
	  float *x,*y,*z;
	  float rx,ry,rz;
	  int i;
	            
          if (!PyArg_ParseTuple(args, "fO", &theta, &pos))
              return NULL;
        
          cs = cos(theta);
          ss = sin(theta);	  
	  
	  /* create a NumPy object similar to the input */
          npy_intp   ld[2];
          ld[0]=pos->dimensions[0];
          ld[1]=pos->dimensions[1];
          //rpos = (PyArrayObject *) PyArray_FromDims(pos->nd,ld,pos->descr->type_num);
	  rpos = (PyArrayObject *) PyArray_SimpleNew(pos->nd,ld,pos->descr->type_num);
	  
      	  /* loop over elements  */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

	        x = (float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
		y = (float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z = (float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);
		
	      	xs = cs* *x - ss* *y;
				
		rx = xs;
	      	ry = ss* *x + cs* *y;
		rz = *z;
			
		
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 0*rpos->strides[1])  = rx;
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 1*rpos->strides[1])  = ry;
	        *(float *)(rpos->data + i*(rpos->strides[0]) + 2*rpos->strides[1])  = rz;		
		
      	  }
	  	  
	  return PyArray_Return(rpos);
      }     
      
      
/*************************/      
/* spin                  */
/*************************/
      
static PyObject *
      nbody_spin(self, args)
          PyObject *self;
          PyObject *args;
      {
          PyArrayObject *pos;
	  PyArrayObject *vel;
	  PyArrayObject *omega;
	  PyArrayObject *nvel;
	  
	  float x,y,z;
	  float vx,vy,vz;
	  float ox,oy,oz;
	  int i;
	            
          if (!PyArg_ParseTuple(args, "OOO", &pos, &vel, &omega))
              return NULL;
          
	  
	  /* create a NumPy object similar to the input */
          npy_intp   ld[2];
          ld[0]=vel->dimensions[0];
          ld[1]=vel->dimensions[1];
	  //nvel = (PyArrayObject *) PyArray_FromDims(vel->nd,ld,vel->descr->type_num);
	  nvel = (PyArrayObject *) PyArray_SimpleNew(vel->nd,ld,vel->descr->type_num);
	  
	  ox = *(float *) (omega->data + 0*omega->strides[0]);	    
	  oy = *(float *) (omega->data + 1*omega->strides[0]);
	  oz = *(float *) (omega->data + 2*omega->strides[0]);	    
	  
	  
	  
      	  /* loop over elements  */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

	        x = *(float *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
		y = *(float *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
		z = *(float *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);

	        vx = *(float *) (vel->data + i*(vel->strides[0]) + 0*vel->strides[1]);
		vy = *(float *) (vel->data + i*(vel->strides[0]) + 1*vel->strides[1]);
		vz = *(float *) (vel->data + i*(vel->strides[0]) + 2*vel->strides[1]);
		
				
	        vx = vx + (oy*z - oz*y);
		vy = vy + (oz*x - ox*z);
		vz = vz + (ox*y - oy*x);			
		
	        *(float *)(nvel->data + i*(nvel->strides[0]) + 0*nvel->strides[1])  = vx;
	        *(float *)(nvel->data + i*(nvel->strides[0]) + 1*nvel->strides[1])  = vy;
	        *(float *)(nvel->data + i*(nvel->strides[0]) + 2*nvel->strides[1])  = vz;		
		
      	  }
	  	  
	  return PyArray_Return(nvel);
      }        
      
      
      
      
/*********************************/
/* pamap */
/*********************************/

static PyObject *
      nbody_pamap(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  float xmx,ymx,cd;
	  int view,scale;	/* log : scale = 0, lin : scale = 1 */
	  
	  PyArrayObject *mat;
	  
	  
	  int   kx,ky;
	  int   kxx,kyy;
	  int   kxx2,kyy2;
	  int  	n,i,j; 
	  int	ix,iy,xi,yi;
	  npy_intp   dim[2];
	  
	  float ax,ay,bx,by;  
	  float dseo[kxmax][kymax];
	  float gmnt,cdopt;
	  float x,y,z,gm;
	  float min,max;
	  float v;
	  int *pv;
	 	  
	  
	         
          if (!PyArg_ParseTuple(args, "OO(ii)fffii",&pos,&gmm,&kx,&ky,&xmx,&ymx,&cd,&view,&scale))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  
	  if (kx > kxmax || ky > kymax){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  
	  
	  /* create the output */
	  
	  dim[0]=kx;
	  dim[1]=ky;
	  //mat = (PyArrayObject *) PyArray_FromDims(2,dim,PyArray_SHORT);
	  mat = (PyArrayObject *) PyArray_SimpleNew(2,dim,NPY_SHORT);   
	 
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
	  		  
	  gmnt = 0.;	  
	  
	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 2;
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 1;
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 2;
	  }	
	    	  
	  /* full dseo : loop over all points in pos*/

          for (i = 0; i < pos->dimensions[0]; i++) {

      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));
	    
	    gmnt = gmnt+gm;
	  		       
      
	    if (x > -xmx && x < xmx) {
	      if (y > -ymx && y < ymx) {
	  		
	  	ix =	   (int)(ax*x + bx) -1;
	  	iy =	   (int)(ay*y + by) -1;
			 
	  	dseo[ix][iy] = dseo[ix][iy] + gm;
		//printf("%d %d %d\n",i,ix,iy);

	      }
	    }	 
	  }
	 
	
	  /* inverse of the mean weight per particule */
	  gmnt = (float)n/gmnt;		        /*????*/	
	
	
	  min = 1e20;
	  max = 0.;
	  
	  /* find min and max */
		  	   
          for (ix=0;ix<kxx;ix++) {
	     for (iy=0;iy<kyy;iy++) {
	       if (dseo[ix][iy] < min) {min = dseo[ix][iy];}  
	       if (dseo[ix][iy] > max) {max = dseo[ix][iy];}  
	     }
	   }
	   
	  /* optimum factor */
	  if (gmnt*max==0){
	   cdopt = 0.;
	  } 
	  else {
	    switch(scale){				/* dépendance de l'échelle */
	      case 0: cdopt = 255./log(gmnt*max+1.);
	      	      break;
	      case 1: cdopt = 255./   (gmnt*max);
                      break;
	    }
	  }
	  if (cd==0) {cd=cdopt;}
	  	
	  /* create the subimage */	  

	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	    	 
	      switch(scale){				  /* dépendance de l'échelle */
	        case 0: v = cd*log(gmnt*dseo[i][j]+1.);
		        break;
	        case 1: v = cd*   (gmnt*dseo[i][j]+1.);
		        break;
	      } 	  
		      
	      if (v > 255.) {
		*(short*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (short) 255.;
	      } else {
		*(short*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (short) v ;
	      }  	        
	         
	    }
	  }
	  
	  return Py_BuildValue("(Of)",mat,cdopt);
      } 
  
  
      
/*********************************/
/* pdpmap */
/*********************************/

static PyObject *
      nbody_pdmap(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *amp = NULL;
	  float xmx,ymx,cd,omin,omax;
	  int view;
	  
	  PyArrayObject *mat;
	  
	  
	  int   kx,ky;
	  int   kxx,kyy;
	  int   kxx2,kyy2;
	  int  	n,i,j; 
	  int	ix,iy,xi,yi,zi;
	  npy_intp   dim[2];
	  
	  float ax,ay,bx,by;  
	  float dseo[kxmax][kymax];
	  float nn[kxmax][kymax];
	  float cdopt;
	  float x,y,z,gm,am;
	  float min,max,mean,sigm;
	  float v;
	  int *pv;
	 	  	         
          if (!PyArg_ParseTuple(args,"OOO(ii)fffffi",&pos,&gmm,&amp,&kx,&ky,&xmx,&ymx,&cd,&omin,&omax,&view))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  
	  if (kx > kxmax || ky > kymax){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
	  /* create the output */
	  
	  dim[0]=kx;
	  dim[1]=ky;
	  //mat = (PyArrayObject *) PyArray_FromDims(2,dim,PyArray_SHORT);
	  mat = (PyArrayObject *) PyArray_SimpleNew(2,dim,NPY_SHORT);    
	 
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
	      nn[ix][iy]=0.;
	    }
	  }
	  		  	  
	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 2;
	    zi = 1; 
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 1;
	    zi = 2;
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 2;
	    zi = 3;
	  }	  	  


	  /* full dseo : loop over all points in pos*/

          for (i = 0; i < pos->dimensions[0]; i++) {

      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]);
	    z	= *(float *) (pos->data + i*(pos->strides[0]) + zi*pos->strides[1]);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));	
	    am  = *(float *) (amp->data + i*(amp->strides[0])); 
	          
	    if (x > -xmx && x < xmx) {
	      if (y > -ymx && y < ymx) {
	  		
	  	ix =	   (int)(ax*x + bx) -1;
	  	iy =	   (int)(ay*y + by) -1;
			 
	  	dseo[ix][iy] = dseo[ix][iy] + gm*am;
		nn[ix][iy] = nn[ix][iy] + gm;

	      }
	    }	 
	  }
	
	  min =  1e20;
	  max = -1e20;
	  mean = 0.;
	  sigm = 0.;
	  
	  /* find min and max, mean and sigma */
		  	   
          for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) {			        
	      if(nn[ix][iy]!=0){			        
	    	dseo[ix][iy]=dseo[ix][iy]/(float)nn[ix][iy];
	    	if (dseo[ix][iy] < min) {min = dseo[ix][iy];}   
	    	if (dseo[ix][iy] > max) {max = dseo[ix][iy];}   
	    	mean = mean + dseo[ix][iy];		        
	    	sigm = sigm + dseo[ix][iy]*dseo[ix][iy];        
	      } 					        
	    }						        
	  }						     
	  	  						     
	  mean = mean / (float)(kxx*kyy);	            		     
	  sigm = sqrt(sigm / (float)(kxx*kyy) - mean*mean);  

         
	  /* optimal ranges */
	  if (cd == 0.) {
	    cd = 1.;
	  }

	  min = mean - cd*sigm; 					   
	  max = mean + cd*sigm;   
	  
	  /* use given ranges if values are different */
	  if (omin != omax) {
	    min = omin;
	    max = omax;
	    mean = (omin+omax)/2.;
	  }
	  
	  cd = 255./ (max-min);
	  //printf("%f %f %f %f\n",min,max,mean,sigm);

          /* shift dseo whith the min */
	  for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) {
	      if(nn[ix][iy]==0){
	        dseo[ix][iy] = min;  /* on met au minimum si vide */
	      }	
	      
	      dseo[ix][iy] = dseo[ix][iy] - min;
	    }
	  }
		   		  
	  	
	  /* create the subimage */	  

	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	    	      
	      v = cd*dseo[i][j];
	      
	      if (v > 254.) {
		*(short*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (short) 254. +1.;
	      } else {
		*(short*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (short) v + 1.;
	      }  	        
	         
	    }
	  }
	  
	  
	  return Py_BuildValue("(Of)",mat,cdopt);
      }               


/*********************************/
/* sphmap */
/*********************************/

static PyObject *
      nbody_sphmap(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  PyArrayObject *rsp = NULL;
	  float xmx,ymx,cd,frsp;
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
	  npy_intp   dim[2];
	  
	  float ax,ay,bx,by;  
	  float dseo[kxmax][kymax];
	  float gmnt,cdopt;
	  float x,y,z,gm,sigma,sigma2,pisig,gaus,ds,sum;
	  float min,max;
	  float v;
	  int *pv;
	 	  
	  
	         
          if (!PyArg_ParseTuple(args, "OOO(ii)ffffi",&pos,&gmm,&rsp,&kx,&ky,&xmx,&ymx,&cd,&frsp,&view))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  
	  if (kx > kxmax || ky > kymax){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  
	  
	  /* create the output */
	  
	  dim[0]=kx;
	  dim[1]=ky;
	  //mat = (PyArrayObject *) PyArray_FromDims(2,dim,PyArray_SHORT);
	  mat = (PyArrayObject *) PyArray_SimpleNew(2,dim,NPY_SHORT);    
	 
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
	  		  
	  gmnt = 0.;	  
	  
	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 2;
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 1;
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 2;
	  }	  	  

          
	  /* full dseo : loop over all points in pos*/

          for (i = 0; i < pos->dimensions[0]; i++) {

      	    x	   = *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]);
      	    y	   = *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]);
      	    gm     = *(float *) (gmm->data + i*(gmm->strides[0]));
	    sigma  = *(float *) (rsp->data + i*(rsp->strides[0]));
	    
	    sigma = frsp*sigma;
	    gmnt = gmnt+gm;	    
	    
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
	      
	      //printf("%d %d %d %d\n",xin,xfi,yin,yfi);
	     
	     
	      if (xfi > xin && yfi > yin ) {
	      	             
	        /* loop over the grid */
	      	for (ixx=xin;ixx < xfi;ixx++){
	      	  for (iyy=yin;iyy < yfi;iyy++){
	      	    
	      	    gaus = ds*pisig*exp( 0.5*(-((float)(ix-ixx)/(ax*sigma))*((float)(ix-ixx)/(ax*sigma))    			       
	      				      -((float)(iy-iyy)/(ay*sigma))*((float)(iy-iyy)/(ay*sigma))) );
	      	    sum = sum + gaus;									    			       
	      												    			       
	      	    //printf("%d %d \n",ixx,iyy);	     
	      	    dseo[ixx][iyy] = dseo[ixx][iyy] + gm * gaus;					    			       

 	      	  }
	      	}
	      }
	      
	    }  
	    
      	  //printf("%f\n",sum);
	  }
	  
	  
	
	  /* inverse of the mean weight per particule */
	  gmnt = (float)n/gmnt;		        /*????*/	
	
	
	  min = 1e20;
	  max = 0.;
	  
	  /* find min and max */
		  	   
          for (ix=0;ix<kxx;ix++) {
	     for (iy=0;iy<kyy;iy++) {
	       if (dseo[ix][iy] < min) {min = dseo[ix][iy];}  
	       if (dseo[ix][iy] > max) {max = dseo[ix][iy];}  
	     }
	   }
	   
	  /* optimum factor */
	  if (gmnt*max==0){
	   cdopt = 0.;
	  } 
	  else {
	    cdopt = 254./log(gmnt*max+1.);
	  }
	  if (cd==0) {cd=cdopt;}
	  	
	  /* create the subimage */	  

	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	    	      
	      v = cd*log(gmnt*dseo[i][j]+1.);
	      
	      if (v > 254.) {
		*(short*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (short) 254. +1.;
	      } else {
		*(short*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (short) v + 1.;
	      }  	        
	         
	    }
	  }
	  
	  
	  return Py_BuildValue("(Of)",mat,cdopt);
      }
            
/*********************************/
/* ampmap */
/*********************************/

static PyObject *
      nbody_ampmap(self, args)
          PyObject *self;
          PyObject *args;
      {
	  
          PyArrayObject *pos = NULL;
	  PyArrayObject *gmm = NULL;
	  float xmx,ymx,cd,omin,omax;
	  int view;
	  
	  PyArrayObject *mat;
	  
	  
	  int   kx,ky;
	  int   kxx,kyy;
	  int   kxx2,kyy2;
	  int  	n,i,j; 
	  int	ix,iy,xi,yi,zi;
	  npy_intp   dim[2];
	  
	  float ax,ay,bx,by;  
	  float dseo[kxmax][kymax];
	  float nn[kxmax][kymax];
	  float cdopt;
	  float x,y,z,gm;
	  float min,max,mean,sigm;
	  float v;
	  int *pv;
	 	  	         
          if (!PyArg_ParseTuple(args,"OO(ii)fffffi",&pos,&gmm,&kx,&ky,&xmx,&ymx,&cd,&omin,&omax,&view))
              return NULL;
	   
	   
	  /* check max size of matrix */
	  
	  if (kx > kxmax || ky > kymax){
	    PyErr_SetString(PyExc_ValueError,"dimension of argument 3 is too large.");
	    return NULL;	  
	  }
	  	  
	  
	  /* create the output */
	  
	  dim[0]=kx;
	  dim[1]=ky;
	  //mat = (PyArrayObject *) PyArray_FromDims(2,dim,PyArray_SHORT);
	  mat = (PyArrayObject *) PyArray_SimpleNew(2,dim,NPY_SHORT);    
	 
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
	      nn[ix][iy]=0.;
	    }
	  }
	  		  	  
	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 2;
	    zi = 1; 
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 1;
	    zi = 2;
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 2;
	    zi = 3;
	  }	  	  


	  /* full dseo : loop over all points in pos*/

          for (i = 0; i < pos->dimensions[0]; i++) {

      	    x	= *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]);
      	    y	= *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]);
	    z	= *(float *) (pos->data + i*(pos->strides[0]) + zi*pos->strides[1]);
      	    gm  = *(float *) (gmm->data + i*(gmm->strides[0]));
      
	    if (x > -xmx && x < xmx) {
	      if (y > -ymx && y < ymx) {
	  		
	  	ix =	   (int)(ax*x + bx) -1;
	  	iy =	   (int)(ay*y + by) -1;
			 
	  	dseo[ix][iy] = dseo[ix][iy] + gm*z;
		nn[ix][iy] = nn[ix][iy] + gm;

	      }
	    }	 
	  }
	
	
	  min =  1e20;
	  max = -1e20;
	  mean = 0.;
	  sigm = 0.;
	  
	  /* find min and max, mean and sigma */
		  	   
          for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) {			        
	      if(nn[ix][iy]!=0){			        
	    	dseo[ix][iy]=dseo[ix][iy]/(float)nn[ix][iy];    
	    	if (dseo[ix][iy] < min) {min = dseo[ix][iy];}   
	    	if (dseo[ix][iy] > max) {max = dseo[ix][iy];}   
	    	mean = mean + dseo[ix][iy];		        
	    	sigm = sigm + dseo[ix][iy]*dseo[ix][iy];        
	      } 					        
	    }						        
	  }						     
	  	  						     
	  mean = mean / (float)(kxx*kyy);	            		     
	  sigm = sqrt(sigm / (float)(kxx*kyy) - mean*mean);  

         
	  /* optimal ranges */
	  if (cd == 0.) {
	    cd = 1.;
	  }

	  min = mean - cd*sigm; 					   
	  max = mean + cd*sigm;   
	  
	  if (omin != omax) {
	    min = omin;
	    max = omax;
	    mean = (omin+omax)/2.;
	  }
	  
	  cd = 255./ (max-min);
	  //printf("%f %f %f %f\n",min,max,mean,sigm);

          /* shift dseo whith the min */
	  for (ix=0;ix<kxx;ix++) {
	    for (iy=0;iy<kyy;iy++) {
	      if(nn[ix][iy]==0){
	        dseo[ix][iy] = min;  /* on met au minimum si vide */
	      }	
	      dseo[ix][iy] = dseo[ix][iy] - min;
	    }
	  }
		   		  
	  	
	  /* create the subimage */	  

	  for (j=0;j<ky;j++) {
	    for (i=0;i<kx;i++) {
	    	      
	      v = cd*dseo[i][j];
	      
	      if (v > 254.) {
		*(short*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (short) 254. +1.;
	      } else {
		*(short*)(mat->data + i*(mat->strides[0]) + (ky-j-1)*(mat->strides[1])) = (short) v + 1.;
	      }  	        
	         
	    }
	  }
	  
	  
	  return Py_BuildValue("(Of)",mat,cdopt);
      }               

/*********************************/
/* perspective */
/*********************************/  
    
static PyObject *
      nbody_perspective(self, args)
          PyObject *self;
          PyObject *args;
      {
          float r_obs,foc;
	  PyArrayObject *pos;
	  PyArrayObject *npos;
	  int view;
	  
          PyArrayObject *array = NULL;
	  
          int i;
	  float r;
	  float x,y,z;
	  int xi,yi,zi;
	  	            
          if (!PyArg_ParseTuple(args, "Offi", &pos, &r_obs,&foc, &view))
              return NULL;
	      
	  /* create a NumPy object similar to the input */
          npy_intp   ld[2];
          ld[0]=pos->dimensions[0];
          ld[1]=pos->dimensions[1];	  
	  //npos = (PyArrayObject *) PyArray_FromDims(pos->nd,ld,pos->descr->type_num);	      
	  npos = (PyArrayObject *) PyArray_SimpleNew(pos->nd,ld,pos->descr->type_num);    

	  /* choose the view */
	  
	  if (view==1){		/*xz*/
	    xi = 0;
	    yi = 1;
	    zi = 2;
	  }
	  
	  if (view==2){		/*xy*/
	    xi = 0;
	    yi = 2;
	    zi = 1;
	  }
	  
	  if (view==3){		/*yz*/
	    xi = 1;
	    yi = 0;
	    zi = 2;
	  }	

      	  /* loop over elements */
      	  for (i = 0; i < pos->dimensions[0]; i++) {

	        x = *(float *) (pos->data + i*(pos->strides[0]) + xi*pos->strides[1]);
		y = *(float *) (pos->data + i*(pos->strides[0]) + yi*pos->strides[1]);
		z = *(float *) (pos->data + i*(pos->strides[0]) + zi*pos->strides[1]);
		
		r = fabs(y+r_obs);
		
//		if (r > foc){
//		  y =  1.;  
//		} else {
//		  y = -1.;
//		}

	        *(float *)(npos->data + i*(npos->strides[0]) + xi*npos->strides[1])  = foc* x/r;
	        *(float *)(npos->data + i*(npos->strides[0]) + yi*npos->strides[1])  = y;
	        *(float *)(npos->data + i*(npos->strides[0]) + zi*npos->strides[1])  = foc* z/r;
				
      	  }
	  
	  return PyArray_Return(npos);
      }


/*********************************/
/* convol */
/*********************************/  
    
static PyObject *
      nbody_convol(self, args)
          PyObject *self;
          PyObject *args;
      {
          PyArrayObject *a = NULL;
	  PyArrayObject *b = NULL;
	  PyArrayObject *c = NULL;
	  
          int nxd,nyd;
	  
	  
          int i,j,k,l;
	  float norm;
	  double *val,*aa,*bb;

          if (!PyArg_ParseTuple(args, "OO",&a,&b))
              return NULL;
	      
	  nxd = (b->dimensions[0]-1)/2;
          nyd = (b->dimensions[1]-1)/2;
	  
	  /* create a NumPy object similar to the input */
          npy_intp   ld[2];
          ld[0]=a->dimensions[0];
          ld[1]=a->dimensions[1];	  
	  //c = (PyArrayObject *) PyArray_FromDims(a->nd,ld,a->descr->type_num);
	  c = (PyArrayObject *) PyArray_SimpleNew(a->nd,ld,a->descr->type_num);
	  
	  for (i=0;i<c->dimensions[0];i++) {
	    for (j=0;j<c->dimensions[1];j++) {		/* loops over the image */
	    
	      val  = (double *) (c->data + (i)*(c->strides[0]) + (j)*c->strides[1]);
	    
	      norm = 0;
	    
	      for (k=-nxd;k<nxd+1;k++) {
	        for (l=-nyd;l<nyd+1;l++) {		/* loops over the kernel */
		
		  if (i+k >= 0 && i+k < c->dimensions[0]) {
		    if (j+l >= 0 && j+l < c->dimensions[1]) {		/* check if we are in the window */
		    
		      aa   = (double *) (a->data + (i+k)  *(a->strides[0]) + (j+l)  *a->strides[1]);
		      bb   = (double *) (b->data + (k+nxd)*(b->strides[0]) + (l+nyd)*b->strides[1]);
		      
		      *val = *val + *aa * *bb;

		      //norm = norm + *bb;
		    }
		  }  
		
		}
	      }
	      
	      //if (norm !=0.) {*val = *val/norm;}
	      	    
	    }
	  }
	
	  
	  return PyArray_Return(c);
      }      



      
            
/* definition of the method table */      
      
static PyMethodDef nbodyMethods[] = {
	   
          {"am",  nbody_am, METH_VARARGS,
           "Calculate the angular momentum of the model."}, 

          {"amxyz",  nbody_amxyz, METH_VARARGS,
           "Calculate the angular momentum in x,y,z for all particles."}, 

          {"samxyz",  nbody_samxyz, METH_VARARGS,
           "Calculate the specific angular momentum in x,y,z for all particles."}, 
	   	   	   
          {"potential",  nbody_potential, METH_VARARGS,
           "Calculate the potential at a given position, with a given softening."}, 

          {"acceleration",  nbody_acceleration, METH_VARARGS,
           "Calculate the acceleration at a given position, with a given softening."}, 

          {"epot",  nbody_epot, METH_VARARGS,
           "Calculate the total potential energy."}, 
	   	   
          {"rotx",  nbody_rotx, METH_VARARGS,
           "Rotation around the x axis."},	
	   
          {"roty",  nbody_roty, METH_VARARGS,
           "Rotation around the y axis."},
	   
          {"rotz",  nbody_rotz, METH_VARARGS,
           "Rotation around the z axis."},	   	       

          {"spin",  nbody_spin, METH_VARARGS,
           "Spin the model around an axis."},
	   
          {"pamap",  nbody_pamap, METH_VARARGS,
           "Return a map of the given points."},
	   
          {"pdmap",  nbody_pdmap, METH_VARARGS,
           "Return a ponderated map of the given points."},	   

          {"sphmap",  nbody_sphmap, METH_VARARGS,
           "Return a sphmap of the given points."},
	   	   
          {"ampmap",  nbody_ampmap, METH_VARARGS,
           "Return a map of amplitude of the given points."},	   
	   
          {"perspective",  nbody_perspective, METH_VARARGS,
           "Return a 3d projection of the given points."},	 	   

          {"convol",  nbody_convol, METH_VARARGS,
           "Return a 2d convolution of a with kernel b."},
	   	   	   	   
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      

      
void initnbodymodule(void)
      {    
          (void) Py_InitModule("nbodymodule", nbodyMethods);	
	  
	  import_array();
      }      
      
