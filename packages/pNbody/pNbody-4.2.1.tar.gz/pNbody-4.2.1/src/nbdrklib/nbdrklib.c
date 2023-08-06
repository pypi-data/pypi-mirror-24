#include <Python.h>
#include <numpy/arrayobject.h>
#include <math.h>



int NDIM=3;



double forces(double T, double *Y, double *YP, double *GM, int n)
  {
    
    int I,I0,I1,I2,I3,I4,I5,I6;
    int   J0,J1,J2,J3,J4,J5,J6;
    double DX,DY,DZ,DD;
    double FX,FY,FZ;
       
    for (I=3;I<6*n;I=I+6)  
      {
      	YP[I]   = 0.;
      	YP[I+1] = 0.;
      	YP[I+2] = 0.;
      }
  
  
     for (I0=0;I0<n;I0++)     
       {
	 I1 = 6*(I0+1)-6;
         I2 = I1+1;
         I3 = I2+1;
         I4 = I3+1;
         I5 = I4+1;
         I6 = I5+1;
         YP[I1] = Y[I4];
         YP[I2] = Y[I5];
         YP[I3] = Y[I6];
	 	         
	 FX = 0.;
         FY = 0.;
         FZ = 0.;
        
	 for (J0=I0+1;J0<n;J0++)  
	   {
	     J1 = 6*(J0+1)-6;
	     J2 = J1+1;
             J3 = J2+1;
             J4 = J3+1;
             J5 = J4+1;
             J6 = J5+1;
	                
             DX = Y[I1]-Y[J1];
	     DY = Y[I2]-Y[J2];
	     DZ = Y[I3]-Y[J3];
           
             DD = 1.0/pow(sqrt( DX*DX + DY*DY + DZ*DZ ),3);
        
	     DX = DX*DD;
             DY = DY*DD;
	     DZ = DZ*DD;
             FX = FX - GM[J0]*DX;
             FY = FY - GM[J0]*DY;
             FZ = FZ - GM[J0]*DZ;
             YP[J4] = YP[J4] + GM[I0]*DX;
             YP[J5] = YP[J5] + GM[I0]*DY;
             YP[J6] = YP[J6] + GM[I0]*DZ;           
           }
        
	 YP[I4] = YP[I4] + FX;
         YP[I5] = YP[I5] + FY;
         YP[I6] = YP[I6] + FZ;
        
       }
       
  }



void rk78(int *IR, double *T, double *DT, double *X, int N, double *TOL, double (* DER)(double t, double *y, double *yp, double *gm, int n), double *GM)

  {
  
    /*
    	Variable step-size automatic one-step integrator for a system of
    	6*N first order ordinary differential equations with initial values
    	The Runge-Kutta-Fehlberg formula 7(8) is used
    	REF   E. FEHLBERG, NASA TECHNICAL REPORT TR R-287, 1968
    	Description of parameters list
    		(All floating variables in DOUBLE PRECISION)
    	IR	O    NUMBER OF REJECTIONS OF THE LAST STEP
    		     (IN CASE  DT WAS TOO LARGE)
    	T	I-O  INDEPENDENT VARIABLE
    	DT	I-O  STEP SIZE
    		     A RECOMMENDED VALUE FOR THE NEXT STEP IS OUTPUT
    	X(N6)	I-O  DEPENDENT VARIABLES
    	FM(N6)       AUXILIARY ARRAYS	WITH M = 0 TO 6
    	F7(N6)       ABSOLUTE ESTIMATED TRUNCATION ERROR ON EACH COMPONENT
    	N6	I    ORDER OF THE DIFFERENTIAL EQUATIONS SYSTEM
    	TOL	I    RELATIVE TOLERATED ERROR ON EACH COMPONENT
    	DER	I    NAME OF THE SUBROUTINE COMPUTING THE DERIVATIVES. THIS
    		     SUBROUTINE HAS TO HAVE THE STANDARD CALLING SEQUENCE
    	CALL DER(T,X,F0)  
    */

    int I;
    int N6 = N;
    double F0[N6],F1[N6],F2[N6],F3[N6],F4[N6],F5[N6],F6[N6],F7[N6];
    
    
  
    double CH1 = 34e0/105e0,   CH2 = 9e0/35e0,    CH3 = 9e0/280e0,
           CH4 = 41e0/840e0,   AL2 = 2e0/27e0,    AL3 = 1e0/9e0,
           AL4 = 1e0/6e0,      AL5 = 5e0/12e0,    AL6 = 5e-1;
    double AL7 = 5e0/6e0,      AL9 = 2e0/3e0,     ALA = 1e0/3e0,
           B21 = 2e0/27e0,     B31 = 1e0/36e0,    B41 = 1e0/24e0,
           B51 = 5e0/12e0,     B61 = 5e-2,        B71 = -25e0/108e0;
    double B81 = 31e0/3e2,     B101= -91e0/108e0, B111= 2383e0/41e2,
           B121= 3e0/205e0,    B131= -1777e0/41e2,B32 = 1e0/12e0,
           B43 = .125e0,       B53 = -25e0/16e0,  B64 = 25e-2;
    double B74 = 125e0/108e0,  B94 = -53e0/6e0,   B104= 23e0/108e0,
           B114= -341e0/164e0, B65 = 2e-1,        b75 = -65e0/27e0,
           B85 = 61e0/225e0,   B95 = 704e0/45e0,  B105= -976e0/135e0;
    double B115= 4496e0/1025e0,B76 = 125e0/54e0,  B86 = -2e0/9e0,
           B96 = -107e0/9e0,   B106= 311e0/54e0,  B116= -301e0/82e0,
           B126= -6e0/41e0,    B136= -289e0/82e0, B87 = 13e0/9e2;
    double B97 = 67e0/9e1,     B107= -19e0/6e1,   B117= 2133e0/41e2,
           B127= -3e0/205e0,   B137= 2193e0/41e2, B108= 17e0/6e0,
           B118= 45e0/82e0,    B128= -3e0/41e0,   B138= 51e0/82e0;
    double B119= 45e0/164e0,   B139= 33e0/164e0,  B1110= 18e0/41e0,
           B1310= 12e0/41e0;
    
      double X1,X4,X5,X6,X7,X8,X9;

      *IR = 0;
      DER(*T, X, F1, GM, N6/6);
      
      /* begin loop 20 */
      while(1)
        {
      
      	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*B21*F1[I]; 
      
      	  DER(*T + AL2* *DT, F0, F2, GM, N6/6);

      	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*(B31*F1[I] + B32*F2[I]); 
	    
      	  DER(*T + AL3* *DT, F0, F3, GM, N6/6);
      
      	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*(B41*F1[I] + B43*F3[I]);
      
      	  DER(*T + AL4* *DT, F0, F4, GM, N6/6);
      	 
	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*(B51*F1[I] + B53*(F3[I] - F4[I]));
      
      	  DER(*T + AL5* *DT, F0, F5, GM, N6/6);
	  
      	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*(B61*F1[I] + B64*F4[I] + B65*F5[I]);
      
      	  DER(*T + AL6* *DT, F0, F6, GM, N6/6);
      	  
	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*(B71*F1[I] + B74*F4[I] + b75*F5[I] + B76*F6[I]);
         
      	  DER(*T + AL7* *DT, F0, F7, GM, N6/6);
      
      	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*(B81*F1[I] + B85*F5[I] + B86*F6[I] + B87*F7[I]);
      
      	  DER(*T + AL4* *DT, F0, F2, GM, N6/6);
      
      	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*(2e0*F1[I] + B94*F4[I] + B95*F5[I] + B96*F6[I] + B97*F7[I] + 3e0*F2[I]);
      
      	  DER(*T + AL9* *DT, F0, F3, GM, N6/6);
      
      	  for (I=0;I<N6;I++)
      	    {
      	      X1 = F1[I];
      	      X4 = F4[I];
      	      X5 = F5[I];
      	      X6 = F6[I];
      	      X7 = F7[I];
      	      X8 = F2[I];
      	      X9 = F3[I];
      	      F2[I] = CH1*X6 + CH2*(X7 + X8) + CH3*X9;
      	      F0[I] = X[I] + *DT*(B101*X1 + B104*X4 + B105*X5 + B106*X6 + B107*X7 + B108*X8 - B32*X9);
      	      F4[I] = B111*X1 + B114*X4 + B115*X5 + B116*X6 + B117*X7 + B118*X8 + B119*X9;
      	      F5[I] = B121*X1 + B126*X6 + B127*X7 + B128*(X8 - X9);
      	      F6[I] = B131*X1 + B114*X4 + B115*X5 + B136*X6 + B137*X7 + B138*X8 + B139*X9;
      	    }
      
      	  DER(*T + ALA* *DT, F0, F3, GM, N6/6);
      
      	  for (I=0;I<N6;I++)
      	    {
      	      F7[I] = X[I] + *DT*(F4[I] + B1110*F3[I]);
      	      F0[I] = X[I] + *DT*(F5[I] - B126*F3[I]);
      	    }
	    
      	  DER(*T + *DT, F7, F4, GM, N6/6);
      	  DER(*T,       F0, F5, GM, N6/6);
      
      	  for (I=0;I<N6;I++)
      	    F0[I] = X[I] + *DT*(F6[I] + B1310*F3[I] + F5[I]);
      
      	  DER(*T + *DT, F0, F6, GM, N6/6);
      
      	  X7 = 1e-30;
      
      	  for (I=0;I<N6;I++)
      	    {
      	      F0[I] = X[I];
      	      X[I] = X[I] + *DT*(CH3*F3[I] + CH4*(F5[I] + F6[I]) + F2[I]);
      	      F7[I] = *DT*(F1[I] + F4[I] - F5[I] - F6[I])*CH4;
      	      X7 = X7 + pow((F7[I]/TOL[I]),2);
      	    }
	  
	    
      	  X9 = *DT;
      	  *DT = *DT*pow((25e-4/X7),625e-4);
	        
      	  if (X7 > 1e0) 
      	    {
      	     
	      for (I=0;I<N6;I++)
	  	X[I] = F0[I];
      	      *IR = *IR + 1;
      	      
	      /*GOTO 20*/
      	    
	    
	    }
      	  else
      	    {	    
      	      *T = *T + X9;
	      return ;
	    }  
      
        }	    
	
  }





void Output(FILE *fd, double t, double *x, int n)
  {
    
    int i;
    
    fprintf(fd,"%g ",t);
    
    for (i=0;i<n;i++)
      /* x,y,z,vx,vy,vz */
      fprintf(fd,"%g %g %g %g %g %g ",x[0+6*i],x[1+6*i],x[2+6*i],x[3+6*i],x[4+6*i],x[5+6*i]);  
    
    fprintf(fd,"\n");        
  }



/*********************************/
/* Compute */
/*********************************/

static PyObject *
      nbdrklib_Compute(self, args)
          PyObject *self;
          PyObject *args;
      {
        
        PyArrayObject *pos,*vel,*mass;
	int n;
	int i,j;  
	int ir; 																	        
  	double t,dt,tmin,tmax;
  	//double x[6*NDIM],xx[6*NDIM],xp[6*NDIM],tol[6*NDIM],gm[NDIM];
	double *x,*xx,*xp,*tol,*gm;
  	double epsx,epsv;
  	double tout,dtout;
	char *filename="qq.dat";
	FILE *fd;
	size_t bytes;
	
	
	//if (! PyArg_ParseTuple(args, "OOOdddddds",&pos,&vel,&mass,&tmin,&tmax,&dt,&dtout,&epsx,&epsv,&filename))
        if (! PyArg_ParseTuple(args, "OOOdddddds",&pos,&vel,&mass,&tmin,&tmax,&dt,&dtout,&epsx,&epsv,&filename))
          return PyString_FromString("error");
	
	
	
	/* check number of bodies = number of dim of pos,vel,mass */
	
	if (pos->nd != 2)
	  {
	    PyErr_SetString(PyExc_ValueError,"dimension of pos must be 2.");
	    return NULL;
	  }
	
	if (vel->nd != 2)
	  {
	    PyErr_SetString(PyExc_ValueError,"dimension of vel must be 2.");
	    return NULL;
	  }	
	
	if (mass->nd != 1)
	  {
	    PyErr_SetString(PyExc_ValueError,"dimension of mass must be 1.");
	    return NULL;
	  }	
	  
	if ((pos->dimensions[0]!=vel->dimensions[0])||(vel->dimensions[0]!=mass->dimensions[0]))  
	  {
	    PyErr_SetString(PyExc_ValueError,"size of pos,vel and mass must be identical");
	    return NULL;
	  }	
        
	
        n = pos->dimensions[0];
	
	/* allocate memory */
	if(!(x  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `x' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }	
	  
	if(!(xx  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `xx' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }		  

	if(!(xp  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `xp' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }	

	if(!(tol  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `tol' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }

	if(!(gm  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `gm' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }	  		
	
	
	/* read data */  
	  	
	
        for (i = 0; i < n; i++) 
	  {
	    x[0+6*i] = *(double *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
	    x[1+6*i] = *(double *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
	    x[2+6*i] = *(double *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);	
	    
	    x[3+6*i] = *(double *) (vel->data + i*(vel->strides[0]) + 0*vel->strides[1]);
	    x[4+6*i] = *(double *) (vel->data + i*(vel->strides[0]) + 1*vel->strides[1]);
	    x[5+6*i] = *(double *) (vel->data + i*(vel->strides[0]) + 2*vel->strides[1]);
	    
	    gm[i]    = *(double *)  (mass->data + i*(mass->strides[0])                 );		    
	        		    
	  } 
	  
        
	/* some init */
  	for (i=0;i<6*n;i=i+6)  
  	  {
  	    for(j=i;j<i+3;j++)
  	      {
  		tol[j  ] = epsx;
  		tol[j+3] = epsv;
  	      }
  	  }    
  
  	for (i=0;i<6*n;i++)
  	  xx[i] = x[i]; 

  	/* first loop to determine dt */
	t=tmin;
  	rk78(&ir, &t, &dt, xx, 6*n, tol, &forces, gm);	  
	

  	/* main loop */
  	t=tmin;
	tout = dtout;

	/* open output */
	fd = fopen(filename,"w");   
	Output(fd,t,x,n);
		
  	while (t<tmax)
  	  {
  
  	    if ((t+dt>tout)&&(t!=tmin) )
  	      {
		dt = tout-t;
  	      }
  
	    rk78(&ir, &t, &dt, x, 6*n, tol, &forces, gm);
	     	    
  	    
	    if ((t >= tout))
  	      {
		Output(fd,t,x,n);
		tout = tout + dtout;
  	      }   
	  }
       		
 	fclose(fd);
	  
	return Py_BuildValue("i",1);
      }               


/*********************************/
/* IntegrateOverDt */
/*********************************/

static PyObject *
      nbdrklib_IntegrateOverDt(self, args)
          PyObject *self;
          PyObject *args;
      {
        
        PyArrayObject *pos,*vel,*mass;
	int n;
	int i,j;  
	int ir; 																	        
  	double t,dt,tstart,tend;
  	//double x[6*NDIM],xx[6*NDIM],xp[6*NDIM],tol[6*NDIM],gm[NDIM];
	double *x,*xx,*xp,*tol,*gm;
  	double epsx,epsv;
	size_t bytes;
	
	
        if (! PyArg_ParseTuple(args, "OOOddddd",&pos,&vel,&mass,&tstart,&tend,&dt,&epsx,&epsv))
	  {
	    PyErr_SetString(PyExc_ValueError,"Error in arguments");
	    return NULL;
	  }  		
	
	/* check number of bodies = number of dim of pos,vel,mass */
	
	if (pos->nd != 2)
	  {
	    PyErr_SetString(PyExc_ValueError,"dimension of pos must be 2.");
	    return NULL;
	  }
	
	if (vel->nd != 2)
	  {
	    PyErr_SetString(PyExc_ValueError,"dimension of vel must be 2.");
	    return NULL;
	  }	
	
	if (mass->nd != 1)
	  {
	    PyErr_SetString(PyExc_ValueError,"dimension of mass must be 1.");
	    return NULL;
	  }	
	  
	if ((pos->dimensions[0]!=vel->dimensions[0])||(vel->dimensions[0]!=mass->dimensions[0]))  
	  {
	    PyErr_SetString(PyExc_ValueError,"size of pos,vel and mass must be identical");
	    return NULL;
	  }	
        
	
        n = pos->dimensions[0];
	
	/* allocate memory */
	if(!(x  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `x' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }	
	  
	if(!(xx  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `xx' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }		  

	if(!(xp  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `xp' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }	

	if(!(tol  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `tol' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }

	if(!(gm  = malloc(bytes = 6*n * sizeof(double))))
    	  {
    	    printf("failed to allocate memory for `gm' (%g MB).\n", bytes / (1024.0 * 1024.0));
    	    exit(-1);
    	  }	  		
		
	/* read data */  
	  	
	
        for (i = 0; i < n; i++) 
	  {
	    x[0+6*i] = *(double *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]);
	    x[1+6*i] = *(double *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]);
	    x[2+6*i] = *(double *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]);	
	    
	    x[3+6*i] = *(double *) (vel->data + i*(vel->strides[0]) + 0*vel->strides[1]);
	    x[4+6*i] = *(double *) (vel->data + i*(vel->strides[0]) + 1*vel->strides[1]);
	    x[5+6*i] = *(double *) (vel->data + i*(vel->strides[0]) + 2*vel->strides[1]);
	    
	    gm[i]    = *(double *)  (mass->data + i*(mass->strides[0])                 );		    
	        		    
	  } 
	  
	/* some init */
  	for (i=0;i<6*n;i=i+6)  
  	  {
  	    for(j=i;j<i+3;j++)
  	      {
  		tol[j  ] = epsx;
  		tol[j+3] = epsv;
  	      }
  	  }    
  
  	for (i=0;i<6*n;i++)
  	  xx[i] = x[i]; 

  	/* first loop to determine dt */
	t=tstart;
  	rk78(&ir, &t, &dt, xx, 6*n, tol, &forces, gm);	  
	

  	/* main loop */
  	t=tstart; 
	
	
		
  	while (t<tend)
  	  {
  
  	    if ((t+dt>tend)&&(t!=tstart) )
  	      {
		dt = tend-t;
  	      }
  
	    rk78(&ir, &t, &dt, x, 6*n, tol, &forces, gm);
	     	    
	  }
       	
	/* return pos,vel,time */
	
        for (i = 0; i < n; i++) 
	  {
	    *(double *) (pos->data + i*(pos->strides[0]) + 0*pos->strides[1]) = x[0+6*i] ;
	    *(double *) (pos->data + i*(pos->strides[0]) + 1*pos->strides[1]) = x[1+6*i] ;
	    *(double *) (pos->data + i*(pos->strides[0]) + 2*pos->strides[1]) = x[2+6*i] ;
	    
	    *(double *) (vel->data + i*(vel->strides[0]) + 0*vel->strides[1]) = x[3+6*i] ;
	    *(double *) (vel->data + i*(vel->strides[0]) + 1*vel->strides[1]) = x[4+6*i] ;
	    *(double *) (vel->data + i*(vel->strides[0]) + 2*vel->strides[1]) = x[5+6*i] ;
	  } 
			  
	return Py_BuildValue("OOdd",pos,vel,t,dt);
      }               



   
            
/* definition of the method table */      
      
static PyMethodDef nbdrklibMethods[] = {

          {"Compute",  nbdrklib_Compute, METH_VARARGS,
           "Compute all."},

          {"IntegrateOverDt",  nbdrklib_IntegrateOverDt, METH_VARARGS,
           "Integrate the system over dt."},
	   	   	   	   
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      
      
void initnbdrklib(void)
      {    
          (void) Py_InitModule("nbdrklib", nbdrklibMethods);	
	  
	  import_array();
      }      
      
