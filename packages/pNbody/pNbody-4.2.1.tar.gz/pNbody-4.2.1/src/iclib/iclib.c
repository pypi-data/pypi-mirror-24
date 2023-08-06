#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>

#define  TWOPI		   6.2831853071795862


float f_fct(float r, PyArrayObject * fct, float Rmax)
  {
    
    float f,y1,y2,ix;
    int x1,x2;
    int n;
    
    /* interpolate */
    n = fct->dimensions[0];
    ix = (r/Rmax*n);    
    

    if (ix <= 0)
      f = *(float*)(fct->data + 0*(fct->strides[0]));
    else
      {
    	if (ix >= (n-1))
    	  {
    	    f = *(float*)(fct->data + (n-1)*(fct->strides[0]));
    	  }		      
    	else
    	  {
    	    
    	    x1 = (int)ix;
    	    x2 = x1+1;
    				    
    	    y1 = *(float*)(fct->data + (x1)*(fct->strides[0]));
    	    y2 = *(float*)(fct->data + (x2)*(fct->strides[0]));
    	    
    	    f = (ix - x1)/(x2-x1)*(y2-y1) + y1;
    	    
    	  }
      }

    return f;
    
  }
  

float ValFromVect(float x, PyArrayObject * xs, PyArrayObject * ys)
  {
    
    /*
    
    for a given x, return the interpolated corresponding y (from ys)
    x is assumed to be linear
    
    */
    
    float f,y1,y2;
    int x1,x2,nx;
    
    float xmin,xmax;
    float ix;
    
    /* interpolate */
    nx = xs->dimensions[0];    
    xmin = *(float*)(xs->data); 
    xmax = *(float*)(xs->data + (xs->dimensions[0]-1)*(xs->strides[0]));   
    
            
    ix = (x-xmin)/(xmax-xmin) * (nx-1);
       

    x1 = (int)ix;
    x2 = x1+1;

        
    
    if ((ix < 0) || (x1<0))
      {
        f = *(float*)(ys->data + 0*(ys->strides[0]));
	return f;
      }
      
    if ((ix > (nx-1)) || (x2>(nx-1))) 
      {
        f = *(float*)(ys->data + (ys->dimensions[0]-1)*(ys->strides[0]));   
	return f;
      }    
    
    
    /* here, we can interpolate */
    
    y1 = *(float*)(ys->data + (x1)*(ys->strides[0]));
    y2 = *(float*)(ys->data + (x2)*(ys->strides[0]));
   
    f = (ix - x1)/(x2-x1)*(y2-y1) + y1;
    
    printf("%g %g %d %g  - %g %g %d\n",x,ix,x1,y1,xmin,xmax,nx);
        
    
    return f;
    
  }




float ValFromVect2(float x, PyArrayObject * xs, PyArrayObject * ys)
  {
    
    /*
    
    !!! here, xs is not linear !!!
    
    */
    
    float f,y1,y2;
    float v1,v2;
    int x1,x2,nx,i;
    
    float xmin,xmax;
    float ix;
    
    /* interpolate */
    nx = xs->dimensions[0];    
    xmin = *(float*)(xs->data); 
    xmax = *(float*)(xs->data + (xs->dimensions[0]-1)*(xs->strides[0]));   
    
   
    if (x < xmin)
      {
        f = *(float*)(ys->data + 0*(ys->strides[0]));
	return f;
      }
      
    if (x > xmax) 
      {
        f = *(float*)(ys->data + (ys->dimensions[0]-1)*(ys->strides[0]));   
	return f;
      }    
    
       
    /* here, we need to loop in order to find x1,x2*/
    
    for (i=0;i<(xs->dimensions[0]-1);i++)
      {
        
        x1 = i;
        x2 = i+1;
	
	v1 = *(float*)(xs->data + (x1)*(xs->strides[0]));
	v2 = *(float*)(xs->data + (x2)*(xs->strides[0]));
      
        
	if ((v1<=x) && (x<v2))
          {
      	
            y1 = *(float*)(ys->data + (x1)*(ys->strides[0]));
            y2 = *(float*)(ys->data + (x2)*(ys->strides[0]));
    
	    f = (float)(x - v1)/(float)(v2-v1)*(y2-y1) + y1;
	    	    
	  }  
      
      
      }
    
            
    
    return f;
    
  }


/*********************************/
/* generic_Mx1D                 */
/*********************************/
 
 
static PyObject *
      iclib_generic_Mx1D(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *x,*xs,*Mx;
	  PyArrayObject *rand1;
	  PyObject *verbose;
	  float xmax;
	  int n,irand;
	  
	  
	  int i;
	  npy_intp ld[1];
	  
	  float XX;
	  float MxMax;
	  float rnd;
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "ifOOOOOO", &n,&xmax,&xs,&Mx,&rand1,&verbose))		
              return NULL;
	  
	      
	  /* create output */
	  ld[0]=n;
	  x = (PyArrayObject *) PyArray_SimpleNew(1,ld,PyArray_FLOAT);               
	      
  	  	  	  	  
	  MxMax = ValFromVect(xmax,xs,Mx);
	  
	   
	  for (i = 0; i < n; i++)   
	    {    
	    	
	      /* number between 0 and 1 */	
              //rnd = (float)random()/(float)RAND_MAX;
	      rnd = *(float*)(rand1->data + i*(rand1->strides[0]));
		
	      /* find the corresponding radius (x may be nonlinear) */	
	      XX = ValFromVect2(rnd*MxMax,Mx,xs);	      			
	      

              if(verbose==Py_True)
	        if (fmod(i,10000)==0 && i!=0) 
	          printf("i=%8d/%d\n",i,n);
		
	      *(float*)(x->data + i*(x->strides[0])) = XX ;
	    }  


	  return PyArray_Return(x);
      }


/*********************************/
/* generic_Mx                 */
/*********************************/
 
 
static PyObject *
      iclib_generic_Mx(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos,*xs,*Mx;
	  PyArrayObject *rand1,*rand2,*rand3;
	  PyObject *verbose;
	  float xmax;
	  float x,y,z;
	  int n,irand;
	  
	  
	  
	  int i;
	  npy_intp ld[2];
	  
	  float XX,YY,ZZ;
	  float MxMax;
	  float rnd;
	  
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "ifOOOOOO", &n,&xmax,&xs,&Mx,&rand1,&rand2,&rand3,&verbose))		
              return NULL;
	  
	      
	  /* create output */
	  ld[0]=n;
	  ld[1]=3;
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);               
	      
  	  
	  /* init random */
	  //srandom(irand);
	  	  	  
	  MxMax = ValFromVect(xmax,xs,Mx);
	  
	  
	  /* normalize Mr */
	  //for (i = 0; i < Mx->dimensions[0]; i++)   
	  //  {
          //  *(float*)(Mx->data + i*(Mx->strides[0])) = *(float*)(Mx->data + i*(Mx->strides[0]))/MxMax ;
	  //  }
	  	  
	   
	  for (i = 0; i < n; i++)   
	    {    
	    	
	      /* number between 0 and 1 */	
              //rnd = (float)random()/(float)RAND_MAX;
	      rnd = *(float*)(rand1->data + i*(rand1->strides[0]));
		
	      /* find the corresponding radius (x may be nonlinear) */	
	      XX = ValFromVect2(rnd*MxMax,Mx,xs);		     	            			
	      YY = *(float*)(rand2->data + i*(rand2->strides[0]));
	      ZZ = *(float*)(rand3->data + i*(rand2->strides[0]));
	      

              if(verbose==Py_True)
	        if (fmod(i,10000)==0 && i!=0) 
	          printf("i=%8d/%d\n",i,n);
		
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = XX ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = YY ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = ZZ ;
	    }  


	  return PyArray_Return(pos);
      }
      

/*********************************/
/* generic_alpha                 */
/*********************************/
 
float  generic_alpha_density(float a, float e, float r)
  {
      
    return pow((r + e),a);
    
  
  }


 
static PyObject *
      iclib_generic_alpha(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  float a,e,rmax;
	  float x,y,z;
	  int n,irand;
	  
	  
	  
	  int i;
	  npy_intp ld[2];
	  
	  float URHOD0,CTHE,STHE,PHI,CX,CY,RR,RHO,R;
	  float XX,YY,ZZ;
	  float EPS;
	  float DPI;
	  
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "ifffi", &n,&a,&e,&rmax,&irand))		
              return NULL;
	  
	      
	  /* create output */
	  ld[0]=n;
	  ld[1]=3;
	  //pos = (PyArrayObject *) PyArray_FromDims(2,ld,PyArray_FLOAT);                    
          pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);

	      
  	  
	  /* init random */
	  srandom(irand);
	  
	  EPS = 1e-30;
	  EPS = 0;
	  DPI = 8.*atan(1.);
	  	  
	  URHOD0 = 1./(generic_alpha_density(a,e,0.)+EPS);
	      
	  for (i = 0; i < n; i++)   
	    {    
	    	      
              do
	        {
		  
		  RR = pow( (float)random()/(float)RAND_MAX  ,1.0/3.0);
		  PHI = DPI*(float)random()/(float)RAND_MAX;
		  CTHE = 1.-2.*(float)random()/(float)RAND_MAX  ;
		  STHE = sqrt(1.-CTHE*CTHE);
		  
		  XX = RR*cos(PHI)*STHE;
		  YY = RR*sin(PHI)*STHE;
		  ZZ = RR*CTHE;
		  
		  R = sqrt( XX*XX + YY*YY + ZZ*ZZ );
		  
		  RHO = URHOD0*generic_alpha_density(a,e,rmax*R);
		
		}
              while(RHO < (float)random()/(float)RAND_MAX);


	      
	      if (fmod(i,10000)==0 && i!=0) 
	        printf("i=%8d/%d\n",i,n);
		
			      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = rmax*XX ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = rmax*YY ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = rmax*ZZ ;
	    }  


	  return PyArray_Return(pos);
      }
      

/*********************************/
/* generic_Mr                 */
/*********************************/
 

 
static PyObject *
      iclib_generic_Mr(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos,*rs,*Mr;
	  PyArrayObject *rand1,*rand2,*rand3;
	  PyObject *verbose;
	  float rmax;
	  float x,y,z;
	  int n,irand;
	  
	  
	  
	  int i;
	  npy_intp ld[2];
	  
	  float CTHE,STHE,PHI,RR;
	  float XX,YY,ZZ;
	  float DPI,MrMax;
	  float rnd;
	  
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "ifOOOOOO", &n,&rmax,&rs,&Mr,&rand1,&rand2,&rand3,&verbose))		
              return NULL;
	  
	      
	  /* create output */
	  ld[0]=n;
	  ld[1]=3;
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);               
	      
  	  
	  /* init random */
	  //srandom(irand);
	  
	  DPI = 8.*atan(1.);
	  	  
	  MrMax = ValFromVect(rmax,rs,Mr);
	  
	  
	  /* normalize Mr */
	  //for (i = 0; i < Mr->dimensions[0]; i++)   
	  //  {
          //  *(float*)(Mr->data + i*(Mr->strides[0])) = *(float*)(Mr->data + i*(Mr->strides[0]))/MrMax ;
	  //  }
	  	  
	   
	  for (i = 0; i < n; i++)   
	    {    
	    	
	      /* number between 0 and 1 */	
              //rnd = (float)random()/(float)RAND_MAX;
	      rnd = *(float*)(rand1->data + i*(rand1->strides[0]));
		
	      /* find the corresponding radius (x may be nonlinear) */	
	      RR = ValFromVect2(rnd*MrMax,Mr,rs);
	      		

              rnd = *(float*)(rand2->data + i*(rand2->strides[0]));
	      PHI = DPI*rnd;
	      rnd = *(float*)(rand3->data + i*(rand3->strides[0]));
	      CTHE = 1.-2.*rnd ;
	      STHE = sqrt(1.-CTHE*CTHE);
	
	      XX = RR*cos(PHI)*STHE;
	      YY = RR*sin(PHI)*STHE;
	      ZZ = RR*CTHE;
	      

              if(verbose==Py_True)
	        if (fmod(i,10000)==0 && i!=0) 
	          printf("i=%8d/%d\n",i,n);
		
			      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = XX ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = YY ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = ZZ ;
	    }  


	  return PyArray_Return(pos);
      }
      


/*********************************/
/* exponential_disk              */
/*********************************/
 
float RHO1(float X)
  {
    /* first deriv of TM1 */
    return X*exp(-X);

  }
  
float TM1(float X)
  {
    return 1.0 - (1.0+X)*exp(-X);
  }
   
 
 
static PyObject *
      iclib_exponential_disk(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  float Hr,Hz,Rmax,Zmax;
	  float x,y,z;
	  int n,irand;
	  
	  
	  
	  int i;
	  npy_intp ld[2];
	  int k;
	  float XM,xx,D;
	  float R,PHI;
	  float x0;
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "iffffi", &n,&Hr,&Hz,&Rmax,&Zmax,&irand))		
              return NULL;
	  
	      
	  /* create output */
	  //pos = (PyArrayObject *) PyArray_FromDims(as->nd,as->dimensions,as->descr->type_num); 
	  ld[0]=n;
	  ld[1]=3;
	  //pos = (PyArrayObject *) PyArray_FromDims(2,ld,PyArray_FLOAT);  
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);                  
	      
  	  
	  /* init random */
	  srandom(irand);	  
	      
	  for (i = 0; i < n; i++)   
	    {    
	      
	      /* radial distribution */
	      R = Rmax+1;
	      while (R>Rmax)
	        {
	      
	          k = 0;
                  XM = (float)random()/(float)RAND_MAX;
                  //xx = 2.*Hr*XM;			/* initial point (bad choice... Pfen ?) */
		  xx = 2.*XM;				/* initial point */
		  x0 = xx;		  
		  
		  k = 0;
		  D = 1;
	          while (fabs(D)> 1E-12)
		    {
		    
                      if (k>32)
		        {
                          //printf("x0=%g xx=%g D=%g\n",x0,xx,D);
			  break;
			}
		    
		      D = (XM - TM1(xx))/RHO1(xx);
		      xx = xx + D;
		      k = k + 1;
		      
		    }
		    		    
		    
                  R = xx*Hr;	
		  
		}  
			      
	      
	      /* angular distribution */
              PHI = TWOPI*(float)random()/(float)RAND_MAX;
              x = R*cos(PHI);
              y = R*sin(PHI);
	      
	      /* verticale distribution */
	      z = Zmax+1;
	      while(z>Zmax)
	        {
		  z = -Hz*log((float)random()/(float)RAND_MAX);
		}	
		
              if ((float)random()/(float)RAND_MAX < 0.5)
                z = -z; 	            
	      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = x ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = y ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = z ;
	    }  


	  return PyArray_Return(pos);
      }
      

/*********************************/
/* miyamoto_nagai                */
/*********************************/


float  rhod1(float a, float b2, float r2, float z2)
  {
      
    float c,c2,d,d2;
    //float cte = 0.079577471636878186;
    
    c2= b2 + z2; 						        
    c = sqrt(c2);						        
    d = a + c;							        
    d2 = d*d;							        
    //return cte * b2*(a*r2 + (d+c+c)*d2) / ( c*c2*sqrt( pow((r2+d2),5) ) ); 
    return b2*(a*r2 + (d+c+c)*d2) / ( c*c2*sqrt( pow((r2+d2),5) ) );  
    
  
  }


 
static PyObject *
      iclib_miyamoto_nagai(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  float a,b,Rmax,Zmax;
	  float x,y,z;
	  int n,irand;
	  
	  
	  
	  int i;
	  npy_intp ld[2];
	  
	  float URHOD0,CTHE,STHE,PHI,CX,CY,RR,R2,Z2,RHO;
	  float XX,YY,ZZ;
	  float EPS;
	  float Rmax2,Zmax2,b2;
	  float DPI;
	  
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "iffffi", &n,&a,&b,&Rmax,&Zmax,&irand))		
              return NULL;
	  
	      
	  /* create output */
	  //pos = (PyArrayObject *) PyArray_FromDims(as->nd,as->dimensions,as->descr->type_num); 
	  ld[0]=n;
	  ld[1]=3;
	  //pos = (PyArrayObject *) PyArray_FromDims(2,ld,PyArray_FLOAT);     
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);               
	      
  	  
	  /* init random */
	  srandom(irand);
	  
	  b2 = b*b;
	  Rmax2 = Rmax*Rmax;
	  Zmax2 = Zmax*Zmax;
	  EPS = 1e-30;
	  EPS = 0;
	  DPI = 8.*atan(1.);
	  
	  URHOD0 = 1./(rhod1(a,b2,0.,0.)+EPS);
	      
	  for (i = 0; i < n; i++)   
	    {    
	    	      
              do
	        {
		  
		  
		  RR = pow( (float)random()/(float)RAND_MAX  ,1.0/3.0);
		  PHI = DPI*(float)random()/(float)RAND_MAX;
		  CTHE = 1.-2.*(float)random()/(float)RAND_MAX  ;
		  STHE = sqrt(1.-CTHE*CTHE);
		  
		  XX = RR*cos(PHI)*STHE;
		  YY = RR*sin(PHI)*STHE;
		  ZZ = RR*CTHE;
		  
		  R2 = XX*XX + YY*YY;
		  Z2 = ZZ*ZZ;
		  RHO = URHOD0*rhod1(a,b2,Rmax2*R2,Zmax2*Z2);
		
		}
              while(RHO < (float)random()/(float)RAND_MAX);


	      
	      if (fmod(i,10000)==0 && i!=0) 
	        printf("i=%8d/%d\n",i,n);
		
			      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = Rmax*XX ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = Rmax*YY ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = Zmax*ZZ ;
	    }  


	  return PyArray_Return(pos);
      }
      




static PyObject *
      iclib_miyamoto_nagai_f(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos, *fct;
	  float a,b,Rmax,Zmax;
	  float x,y,z;
	  int n,irand;
	  
	  
	  
	  int i;
	  npy_intp ld[2];
	  
	  float URHOD0,URHOD1,CTHE,STHE,PHI,CX,CY,RR,R2,Z2,RHO,R;
	  float XX,YY,ZZ;
	  float EPS;
	  float Rmax2,Zmax2,b2;
	  float DPI;
	  float fRmax;
	  
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "iffffiOf", &n,&a,&b,&Rmax,&Zmax,&irand,&fct,&fRmax))		
              return NULL;
	  
	      
	  /* create output */
	  ld[0]=n;
	  ld[1]=3;
	  //pos = (PyArrayObject *) PyArray_FromDims(2,ld,PyArray_FLOAT);          
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);          
	      
  	  
	  /* init random */
	  srandom(irand);
	  
	  b2 = b*b;
	  Rmax2 = Rmax*Rmax;
	  Zmax2 = Zmax*Zmax;
	  EPS = 1e-30;
	  EPS = 0;
	  DPI = 8.*atan(1.);
	  
	  /* find the max density along the disk */
	  URHOD0 = -1;
	  
	  for (i=0;i<n;i++)
	    {
	      R = Rmax*((float)i/(float)n);
	      R2 = R*R;
	      	      
	      URHOD1 = rhod1(a,b2,R2,0)/f_fct(R,fct,fRmax);
	      	      	      
	      if (URHOD1>URHOD0)
	        {
	          URHOD0 = URHOD1;
		}     
	    }
	    
	  URHOD0 = 1/URHOD0;
	  
	      
	  for (i = 0; i < n; i++)   
	    {    
	    	    	      
              do
	        {
		  
		  RR = pow( (float)random()/(float)RAND_MAX  ,1.0/3.0);
		  PHI = DPI*(float)random()/(float)RAND_MAX;
		  CTHE = 1.-2.*(float)random()/(float)RAND_MAX  ;
		  STHE = sqrt(1.-CTHE*CTHE);
		  
		  XX = RR*cos(PHI)*STHE;
		  YY = RR*sin(PHI)*STHE;
		  ZZ = RR*CTHE;
		  
		  R2 = XX*XX + YY*YY;
		  Z2 = ZZ*ZZ;
		  RHO = URHOD0* rhod1(a,b2,Rmax2*R2,Zmax2*Z2)/f_fct(sqrt(Rmax2*R2),fct,fRmax);
		
		}
              while(RHO < (float)random()/(float)RAND_MAX);


	      
	      if (fmod(i,10000)==0 && i!=0) 
	        printf("i=%8d/%d\n",i,n);
		
			      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = Rmax*XX ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = Rmax*YY ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = Zmax*ZZ ;
	    }  


	  return PyArray_Return(pos);
      }











/*********************************/
/* Burkert                */
/*********************************/


float  burkert_density(float rs,float r)
  {  
    return  1 / ( ( 1 + r/rs  ) * ( 1 + pow((r/rs),2)  ) );
  }


 
static PyObject *
      iclib_burkert(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  float rs,Rmax;
	  float x,y,z;
	  int n,irand;
	  
	  
	  
	  int i;
	  npy_intp ld[2];
	  
	  float URHOD0,CTHE,STHE,PHI,CX,CY,RR,R2,RHO;
	  float XX,YY,ZZ;
	  float EPS;
	  float Rmax2;
	  float DPI;
	  
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "iffi", &n,&rs,&Rmax,&irand))		
              return NULL;
	  
	      
	  /* create output */
	  ld[0]=n;
	  ld[1]=3;
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);               
	      
  	  
	  /* init random */
	  srandom(irand);
	  
	  Rmax2 = Rmax*Rmax;
	  EPS = 1e-30;
	  EPS = 0;
	  DPI = 8.*atan(1.);
	  
	  URHOD0 = 1/burkert_density(rs,0);
	  
	  
	      
	  for (i = 0; i < n; i++)   
	    {    
	    	      
              do
	        {
		  
		  RR = pow( (float)random()/(float)RAND_MAX  ,1.0/3.0);
		  PHI = DPI*(float)random()/(float)RAND_MAX;
		  CTHE = 1.-2.*(float)random()/(float)RAND_MAX  ;
		  STHE = sqrt(1.-CTHE*CTHE);
		  
		  XX = RR*cos(PHI)*STHE;
		  YY = RR*sin(PHI)*STHE;
		  ZZ = RR*CTHE;
		  
		  R2 = XX*XX + YY*YY + ZZ*ZZ;
		  		  
		  
		  RHO = URHOD0*burkert_density(rs,sqrt(Rmax2*R2));
		
		}
              while(RHO < (float)random()/(float)RAND_MAX);


	      
	      if (fmod(i,10000)==0 && i!=0) 
	        printf("i=%8d/%d\n",i,n);
		
			      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = Rmax*XX ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = Rmax*YY ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = Rmax*ZZ ;
	    }  


	  return PyArray_Return(pos);
      }
      




/*********************************/
/* NFWg				 */
/*********************************/


float  nfwg_density(float rs,float gamma, float e, float r)
  {  
    return  1/  (  pow(((r+e)/rs),gamma) * pow( 1+pow(r/rs,2) ,0.5*(3-gamma))  );
    //return  1/  (     (((r+e)/rs) ) * pow(1+r/rs,2)   );
  }


 
static PyObject *
      iclib_nfwg(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  float rs,gamma,e,Rmax;
	  float x,y,z;
	  int n,irand;
	  
	  
	  
	  int i;
	  npy_intp ld[2];
	  
	  float URHOD0,CTHE,STHE,PHI,CX,CY,RR,R2,RHO;
	  float XX,YY,ZZ;
	  float EPS;
	  float Rmax2;
	  float DPI;
	  
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "iffffi", &n,&rs,&gamma,&e,&Rmax,&irand))		
              return NULL;
	  	      
	  /* create output */
	  ld[0]=n;
	  ld[1]=3;
	  pos = (PyArrayObject *) PyArray_SimpleNew(2,ld,PyArray_FLOAT);               
	      
  	  
	  /* init random */
	  srandom(irand);
	  
	  Rmax2 = Rmax*Rmax;
	  EPS = 1e-30;
	  EPS = 0;
	  DPI = 8.*atan(1.);
	  
	  URHOD0 = 1/nfwg_density(rs,gamma,e,0);	  
	  
	      
	  for (i = 0; i < n; i++)   
	    {    
	    	      
              do
	        {
		  
		  RR = pow( (float)random()/(float)RAND_MAX  ,1.0/3.0);
		  PHI = DPI*(float)random()/(float)RAND_MAX;
		  CTHE = 1.-2.*(float)random()/(float)RAND_MAX  ;
		  STHE = sqrt(1.-CTHE*CTHE);
		  
		  XX = RR*cos(PHI)*STHE;
		  YY = RR*sin(PHI)*STHE;
		  ZZ = RR*CTHE;
		  
		  R2 = XX*XX + YY*YY + ZZ*ZZ;
		  		  
		  
		  RHO = URHOD0*nfwg_density(rs,gamma,e,sqrt(Rmax2*R2));
		
		}
              while(RHO < (float)random()/(float)RAND_MAX);


	      
	      if (fmod(i,10000)==0 && i!=0) 
	        printf("i=%8d/%d\n",i,n);
		
			      
	      *(float*)(pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = Rmax*XX ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = Rmax*YY ;
	      *(float*)(pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = Rmax*ZZ ;
	    }  


	  return PyArray_Return(pos);
      }
      






            
/* definition of the method table */      
      
static PyMethodDef iclibMethods[] = {

          {"generic_Mx1D",  iclib_generic_Mx1D, METH_VARARGS,
           "Return position following the density given by M(x)=Mx. Return only x."},

          {"generic_Mx",  iclib_generic_Mx, METH_VARARGS,
           "Return position following the density given by M(x)=Mx. We assume an homogeneous distribution in y and z."},


          {"generic_alpha",  iclib_generic_alpha, METH_VARARGS,
           "Return position following the density (r+eps)^a."},

          {"generic_Mr",  iclib_generic_Mr, METH_VARARGS,
           "Return position following the density given by M(r)=Mr."},


          {"exponential_disk",  iclib_exponential_disk, METH_VARARGS,
           "Return position of an exponential disk."},  

          {"miyamoto_nagai",  iclib_miyamoto_nagai, METH_VARARGS,
           "Return position of a miyamoto_nagai model."},  

          {"miyamoto_nagai_f",  iclib_miyamoto_nagai_f, METH_VARARGS,
           "Return position of a miyamoto_nagai model divided by f(R)."},  

          {"miyamoto_nagai_f",  iclib_miyamoto_nagai_f, METH_VARARGS,
           "Return position of a miyamoto_nagai model divided by f(R)."},  

          {"burkert",  iclib_burkert, METH_VARARGS,
           "Return position of a burkert model."},  

          {"nfwg",  iclib_nfwg, METH_VARARGS,
           "Return position of a nfwg model."},  
	   	    
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      

      
void initiclib(void)
      {    
          (void) Py_InitModule("iclib", iclibMethods);	
	  
	  import_array();
      }      
      
