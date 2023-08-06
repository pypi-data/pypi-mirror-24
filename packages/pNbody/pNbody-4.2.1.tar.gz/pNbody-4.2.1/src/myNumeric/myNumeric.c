#include <Python.h>
#include <math.h>
#include <numpy/arrayobject.h>


/*********************************/
/* some nr functions             */
/*********************************/

#define FREE_ARG char*
#define NR_END 1
#define TINY 1.0e-25
#define FREERETURN {free_vector(d,0,n-1);free_vector(c,0,n-1);return;}

void nrerror(char error_text[])
/* Numerical Recipes standard error handler */
{
	fprintf(stderr,"Numerical Recipes run-time error...\n");
	fprintf(stderr,"%s\n",error_text);
	fprintf(stderr,"...now exiting to system...\n");
	exit(1);
}

float *vector(long nl, long nh)
/* allocate a float vector with subscript range v[nl..nh] */
{
	float *v;

	v=(float *)malloc((size_t) ((nh-nl+1+NR_END)*sizeof(float)));
	if (!v) nrerror("allocation failure in vector()");
	return v-nl+NR_END;
}

void free_vector(float *v, long nl, long nh)
/* free a float vector allocated with vector() */
{
	free((FREE_ARG) (v+nl-NR_END));
}

void polint(float xa[], float ya[], int n, float x, float *y, float *dy)
{
	int i,m,ns=1;
	float den,dif,dift,ho,hp,w;
	float *c,*d;

	dif=fabs(x-xa[0]);
	c=vector(0,n-1);
	d=vector(0,n-1);
	for (i=0;i<n;i++) {
		if ( (dift=fabs(x-xa[i])) < dif) {
			ns=i;
			dif=dift;
		}
		c[i]=ya[i];
		d[i]=ya[i];
	}
	*y=ya[ns--];
	for (m=1;m<n;m++) {
		for (i=0;i<=n-m;i++) {
			ho=xa[i]-x;
			hp=xa[i+m]-x;
			w=c[i+1]-d[i];
			if ( (den=ho-hp) == 0.0) nrerror("Error in routine polint");
			den=w/den;
			d[i]=hp*den;
			c[i]=ho*den;
		}
		*y += (*dy=(2*ns < (n-m) ? c[ns+1] : d[ns--]));
	}
	free_vector(d,0,n-1);
	free_vector(c,0,n-1);
	
}

void ratint(float xa[], float ya[], int n, float x, float *y, float *dy)
{
	int m,i,ns=1;
	float w,t,hh,h,dd,*c,*d;

	c=vector(0,n-1);
	d=vector(0,n-1);
	hh=fabs(x-xa[0]);
	for (i=0;i<n;i++) {
		h=fabs(x-xa[i]);
		if (h == 0.0) {
			*y=ya[i];
			*dy=0.0;
			FREERETURN
		} else if (h < hh) {
			ns=i;
			hh=h;
		}
		c[i]=ya[i];
		d[i]=ya[i]+TINY;
	}
	*y=ya[ns--];
	for (m=1;m<n;m++) {
		for (i=0;i<=n-m;i++) {
			w=c[i+1]-d[i];
			h=xa[i+m]-x;
			t=(xa[i]-x)*d[i]/h;
			dd=t-c[i+1];
			if (dd == 0.0) nrerror("Error in routine ratint");
			dd=w/dd;
			d[i]=c[i+1]*dd;
			c[i]=t*dd;
		}
		*y += (*dy=(2*ns < (n-m) ? c[ns+1] : d[ns--]));
	}
	FREERETURN
}


void spline(float x[], float y[], int n, float yp1, float ypn, float y2[])
{
	int i,k;
	float p,qn,sig,un,*u;
	u=vector(1,n-1);
	if (yp1 > 0.99e30)
		y2[0]=u[0]=0.0;
	else {
		y2[0] = -0.5;
		u[0]=(3.0/(x[1]-x[0]))*((y[1]-y[0])/(x[1]-x[0])-yp1);
	}
	for (i=1;i<=n;i++) {
		sig=(x[i]-x[i-1])/(x[i+1]-x[i-1]);
		p=sig*y2[i-1]+2.0;
		y2[i]=(sig-1.0)/p;
		u[i]=(y[i+1]-y[i])/(x[i+1]-x[i]) - (y[i]-y[i-1])/(x[i]-x[i-1]);
		u[i]=(6.0*u[i]/(x[i+1]-x[i-1])-sig*u[i-1])/p;
	}
	if (ypn > 0.99e30)
		qn=un=0.0;
	else {
		qn=0.5;
		un=(3.0/(x[n-1]-x[n-2]))*(ypn-(y[n-1]-y[n-2])/(x[n-1]-x[n-2]));
	}
	y2[n-1]=(un-qn*u[n-2])/(qn*y2[n-2]+1.0);
	for (k=n-2;k>=0;k--)
		y2[k]=y2[k]*y2[k+1]+u[k];
	free_vector(u,1,n-1);
	
}
void splint(float xa[], float ya[], float y2a[], int n, float x, float *y)
{
	void nrerror(char error_text[]);
	int klo,khi,k;
	float h,b,a;

	klo=0;
	khi=n-1;
	while (khi-klo > 1) {
		k=(khi+klo) >> 1;
		if (xa[k] > x) khi=k;
		else klo=k;
	}
	h=xa[khi]-xa[klo];
	if (h == 0.0) nrerror("Bad xa input to routine splint");
	a=(xa[khi]-x)/h;
	b=(x-xa[klo])/h;
	*y=a*ya[klo]+b*ya[khi]+((a*a*a-a)*y2a[klo]+(b*b*b-b)*y2a[khi])*(h*h)/6.0;
}




/*********************************/
/* tests                         */
/*********************************/
      
static PyObject *
      myNumeric_test(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *x;
	  int	d,i,type;
	  npy_intp *ds;
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "O", &x))		
              return NULL;
	      
	  /* look at the dimension */
	  
	  d = x->nd;
	  printf("dimension = %d\n",d);   
	  
	  
          /* look at the dimension */	
	  ds = x->dimensions;
	  
	  for (i=0;i<d;i++){
	    printf("subd %d\n",(int)ds[i]);
	  }   
	  
	  
	  /* look at the type */
	  
	  type = x->descr->type_num;
	  printf("type = %d\n",type); 
	  printf("\n");
	  //printf("type SBYTE = %d\n",PyArray_SBYTE);			/* same than Int32 in numpy */
	  printf("type SHORT = %d\n",PyArray_SHORT);
	  printf("type INT = %d\n",PyArray_INT);
	  printf("type LONG = %d\n",PyArray_LONG);
	  printf("type FLOAT = %d\n",PyArray_FLOAT);
	  printf("type DOUBLE = %d\n",PyArray_DOUBLE);

	  return Py_BuildValue("i",1);
      }
      






/*********************************/
/* lininterp1d                   */
/*********************************/
      
static PyObject *
      myNumeric_lininterp1d(self, args)
          PyObject *self;
          PyObject *args;
      {


	  PyArrayObject *x  = NULL;
	  PyArrayObject *y  = NULL;
	  PyArrayObject *xs = NULL;
	  PyArrayObject *ys = NULL;
	  float xx,yy;
	  int	i,j;
	  float x1,x2,y1,y2;
	  float a,b;
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOO", &x,&xs,&ys))		
              return NULL;
	      
	      
          y = (PyArrayObject *) PyArray_SimpleNew(x->nd,x->dimensions,PyArray_FLOAT);
	          


      	  for (i = 0; i < x->dimensions[0]; i++) {
	  
	    xx = *(float *) (x->data + i*(x->strides[0]));


            
	    if ( xx <  *(float *) (xs->data + 0*(xs->strides[0])))
	      {
	        j = 0;
	      }
	    else
	      {
	      
	        for (j = 0; j < xs->dimensions[0]-1; j++) {
		                 
		  if ((xx >= *(float *) (xs->data + j*(xs->strides[0]))  ) && (xx < *(float *) (xs->data + (j+1)*(xs->strides[0]))))
		      break;
			    
		  }
	      }  
	    
      
    	    if (j == (xs->dimensions[0]-1))
    	       j = xs->dimensions[0]-2;

   
    
    	    x1 = *(float *) (xs->data + (j  )*(xs->strides[0]));
    	    y1 = *(float *) (ys->data + (j  )*(ys->strides[0]));
    	    x2 = *(float *) (xs->data + (j+1)*(xs->strides[0]));
    	    y2 = *(float *) (ys->data + (j+1)*(ys->strides[0]));
								
    	    a = (y1-y2)/(x1-x2);
    	    b = y1-a*x1;   
   
            yy = a*xx + b;
   
   
            *(float *) (y->data + i*(y->strides[0])) = yy;

      	  }
	  

          return PyArray_Return(y);

      }


/*********************************/
/* quadinterp1d                   */
/*********************************/
      
static PyObject *
      myNumeric_quadinterp1d(self, args)
          PyObject *self;
          PyObject *args;
      {


	  PyArrayObject *x  = NULL;
	  PyArrayObject *y  = NULL;
	  PyArrayObject *xs = NULL;
	  PyArrayObject *ys = NULL;
	  float xx,yy;
	  int	i,j,dj;
	  float x1,x2,x3,y1,y2,y3;
	  float x12,x23,xs12,xs23,y12,y23; 
	  float a,b,c;
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOO", &x,&xs,&ys))		
              return NULL;
	      
	      
          y = (PyArrayObject *) PyArray_SimpleNew(x->nd,x->dimensions,PyArray_FLOAT);
        


      	  for (i = 0; i < x->dimensions[0]; i++) {
	  
	    xx = *(float *) (x->data + i*(x->strides[0]));


            
	    if ( xx <  *(float *) (xs->data + 0*(xs->strides[0])))
	      {
	        j = 0;
	      }
	    else
	      {
	      
	        for (j = 0; j < xs->dimensions[0]-1; j++) {
		                 
		  if ((xx >= *(float *) (xs->data + j*(xs->strides[0]))  ) && (xx < *(float *) (xs->data + (j+1)*(xs->strides[0]))))
		      break;
			    
		  }
	      }  
	    
	    
	    if (fmod(j,2)==0)
    	      dj = 0;
    	    else 
    	      dj = -1;	 
    
   
   
    	    if ((j+2+dj) == xs->dimensions[0])
    	       dj = dj-1;

   
    
    	    x1 = *(float *) (xs->data + (j+dj  )*(xs->strides[0]));
    	    y1 = *(float *) (ys->data + (j+dj  )*(ys->strides[0]));
    	    x2 = *(float *) (xs->data + (j+1+dj)*(xs->strides[0]));
    	    y2 = *(float *) (ys->data + (j+1+dj)*(ys->strides[0]));
    	    x3 = *(float *) (xs->data + (j+2+dj)*(xs->strides[0]));
  	    y3 = *(float *) (ys->data + (j+2+dj)*(ys->strides[0]));
								
    
    	    x12 = x1-x2;
	    x23 = x2-x3;
    
    	    xs12 = x1*x1 - x2*x2;
	    xs23 = x2*x2 - x3*x3;
    
    	    y12 = y1-y2;
	    y23 = y2-y3;

    
    	    a = (y12*x23-y23*x12)/(xs12*x23-xs23*x12);
    	    b = (y12 - a*xs12)/x12; 
   	    c =  y1 - a*x1*x1- b*x1;
   
   
            yy = a*xx*xx + b*xx + c;
   
   
            *(float *) (y->data + i*(y->strides[0])) = yy;

		 
      	  }
	  

          return PyArray_Return(y);

      }


/*********************************/
/* quadinterp1d                   */
/*********************************/
      
static PyObject *
      myNumeric_quaddinterp1d(self, args)
          PyObject *self;
          PyObject *args;
      {


	  PyArrayObject *x  = NULL;
	  PyArrayObject *y  = NULL;
	  PyArrayObject *xs = NULL;
	  PyArrayObject *ys = NULL;
	  	  
	  float xx,yy;
	  int	i,j;
	  float x1,x2,y1,y2;
	  float a,b,c;
	  float *as,*bs,*cs;
	  float p0,p;
	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOOf", &x,&xs,&ys,&p0))		
              return NULL;
	      
	      
          y = (PyArrayObject *) PyArray_SimpleNew(x->nd,x->dimensions,PyArray_FLOAT);



	  /* allocate memory */	  
          if(!(as = malloc(xs->dimensions[0] * sizeof(float))))
	    {PyErr_SetString(PyExc_ValueError,"Failed to allocate memory for as.");}	  

          if(!(bs = malloc(xs->dimensions[0] * sizeof(float))))
	    {PyErr_SetString(PyExc_ValueError,"Failed to allocate memory for bs.");}	  

          if(!(cs = malloc(xs->dimensions[0] * sizeof(float))))
	    {PyErr_SetString(PyExc_ValueError,"Failed to allocate memory for cs.");}	  

        
	
	  /* first, compute as,bc,cs */	 	
	
	  p = p0;

      	  for (i = 0; i < xs->dimensions[0]-1; i++) {
	  
   	    x1 = *(float *)(xs->data + (i)  *(xs->strides[0]));
   	    y1 = *(float *)(ys->data + (i)  *(ys->strides[0]));
   	    x2 = *(float *)(xs->data + (i+1)*(xs->strides[0]));
   	    y2 = *(float *)(ys->data + (i+1)*(ys->strides[0]));
   	    
	    if ((x1-x2) == 0)
	      printf("warning !!! x1=x2=%g\n\n",x1);
   	    
   	    as[i] = -( (y1-y2) - p*(x1-x2) ) / pow((x1-x2),2);
   	    bs[i] = p - 2*as[i]*x1;
   	    cs[i] = y1 - as[i]*x1*x1 - bs[i]*x1;
	    
	       	    
   	    /* slope next point */
   	    p = 2*as[i]*x2 + bs[i];
	    
	    	  	  
	  
	  }
	  
	
	  /* now, loop over all points */	 	
	

      	  for (i = 0; i < x->dimensions[0]; i++) {
	  
	    xx = *(float *) (x->data + i*(x->strides[0]));

            
	    if ( xx <  *(float *) (xs->data + 0*(xs->strides[0])))
	      {
	        j = 0;
	      }
	    else
	      {
	      
	        for (j = 0; j < xs->dimensions[0]-1; j++) {
		                 
		  if ((xx >= *(float *) (xs->data + j*(xs->strides[0]))  ) && (xx < *(float *) (xs->data + (j+1)*(xs->strides[0]))))
		      break;
			    
		  }
	      }  
	    
	           
   
    	    if ((j) == xs->dimensions[0]-1)
    	       j = j-1;


            yy =  as[j]*xx*xx + bs[j]*xx + cs[j];
   
            *(float *) (y->data + i*(y->strides[0])) = yy;

		 
      	  }
	  

          return PyArray_Return(y);

      }


/*********************************/
/* vprod             */
/*********************************/
      
static PyObject *
      myNumeric_vprod(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *pos;
	  PyArrayObject *vel;
	  PyArrayObject *ltot;
	  
	  int	i;
	  float *x,*y,*z;
	  float *vx,*vy,*vz;
	  	  
	  float lx,ly,lz;
	  npy_intp   ld[1];
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OO", &pos , &vel))		
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
						
	      	lx = lx +   (*y * *vz - *z * *vy);
	      	ly = ly +   (*z * *vx - *x * *vz);
	      	lz = lz +   (*x * *vy - *y * *vx);
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
/* getmask                       */
/*********************************/

static PyObject *
      myNumeric_getmask(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *x;
	  PyArrayObject *y;
	  PyArrayObject *z;
	  
	  int	i,j,k;
	  long	xx,yy;
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OO", &x, &y))		
              return NULL;
	  
	  	  
	  /* check the type */	  
	     
	  if (x->descr->type_num != PyArray_LONG){
	    PyErr_SetString(PyExc_ValueError,"type of first argument must be integer.");
	    return NULL;
	  }

	  if (y->descr->type_num != PyArray_LONG){
	    PyErr_SetString(PyExc_ValueError,"type of second argument must be integer.");
	    return NULL;
	  }
	  
	  /* check the dimension */
	  
	  if (x->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of first argument must be 1."); 
	    return NULL;
	  }

	  if (y->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of second argument must be 1."); 
	    return NULL;
	  }	  	

	  /* create a NumPy object similar to the input x*/
	  //z = (PyArrayObject *) PyArray_FromDims(x->nd,x->dimensions,x->descr->type_num);
          z = (PyArrayObject *) PyArray_SimpleNew(x->nd,x->dimensions,x->descr->type_num);
	  
	  /* loop over elements of x */	
	  j = 0;
	  for (i = 0; i < x->dimensions[0]; i++) { 


            xx = *(long *)(x->data + i*(x->strides[0]));	/* read x */
	    yy = *(long *)(y->data + j*(y->strides[0]));	/* read y */
	    
	    
	    while (xx>yy) {					/* here, we assume that x and y are sorted ... no ? */					    
	      j++;
	      
	      if (j>y->dimensions[0]){				/* if reached the end of y */
	        for (k = i; k < x->dimensions[0]; k++) { 
	          *(long *)(z->data + k*(z->strides[0])) = 0;	
	          } 
	        return PyArray_Return(z); 
	      }
	        
	      yy = *(long *)(y->data + j*(y->strides[0]));    /* read y */
            }								    
	    
	    
	    if (yy==xx){
	      *(long *)(z->data + i*(z->strides[0])) = 1;  
	      j++;	
	      if (j>y->dimensions[0]){				/* if reached the end of y */
	        for (k = i; k < x->dimensions[0]; k++) { 
	          *(long *)(z->data + k*(z->strides[0])) = 0;	
	          } 
	        return PyArray_Return(z); 
	      }	      
	      				   
	    } else {					   
	      *(long *)(z->data + i*(z->strides[0])) = 0;  
	    }						   
	      
	  	  
	  }
	  /* end of loop over elements of x */	
	  		
		      	  
	  return PyArray_Return(z);
      }

/*********************************/
/* histogram2d                   */
/*********************************/

static PyObject *
      myNumeric_histogram2d(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *f1;
	  PyArrayObject *f2;
	  PyArrayObject *binx;
	  PyArrayObject *biny;
	  PyArrayObject *h;
	  
	  int	i,j,ix,iy;
	  npy_intp   dim[2];
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOOO",&f1,&f2,&binx,&biny))		
              return NULL;
	  
	  	  
	  /* check the types */	  
	     
	  if (f1->descr->type_num != PyArray_DOUBLE){
	    PyErr_SetString(PyExc_ValueError,"type of first argument must be float.");
	    return NULL;
	  }

	  if (f2->descr->type_num != PyArray_DOUBLE){
	    PyErr_SetString(PyExc_ValueError,"type of second argument must be float.");
	    return NULL;
	  }
	  
	  if (binx->descr->type_num != PyArray_DOUBLE){
	    PyErr_SetString(PyExc_ValueError,"type of third argument must be float.");
	    return NULL;
	  }	  
	  
	  
	  if (biny->descr->type_num != PyArray_DOUBLE){
	    PyErr_SetString(PyExc_ValueError,"type of fourth argument must be float.");
	    return NULL;
	  }	 	  
	  
	  
	  /* check the dimensions */
	  
	  if (f1->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of first argument must be 1."); 
	    return NULL;
	  }

	  if (f2->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of second argument must be 1."); 
	    return NULL;
	  }	
	  
	  if (binx->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of third argument must be 1."); 
	    return NULL;
	  }

	  if (biny->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of fourth argument must be 1."); 
	    return NULL;
	  }		  
	  
	  
	  /* -- */
	  
	  if (f1->dimensions[0] != f2->dimensions[0]){
	    PyErr_SetString(PyExc_ValueError,"first and second argument must have the same size."); 
	    return NULL;
	  }
	  
	  	  	  
	  /* create the output */
	  
	  dim[0]=binx->dimensions[0];
	  dim[1]=biny->dimensions[0];
	  //h = (PyArrayObject *) PyArray_FromDims(2,dim,PyArray_DOUBLE); 
	  h = (PyArrayObject *) PyArray_SimpleNew(2,dim,NPY_DOUBLE); 
	  
	  /* fill the output */
	  
	  /* loop over all elements of f1 and f2 */
	  for (i = 0; i < f1->dimensions[0]; i++) {
	  
	    ix = -1;
	    iy = -1;
	  
	    /* find ix*/
	    for (j = 0; j < binx->dimensions[0]-1; j++){
	      if ( *(double *)(f1->data + i*(f1->strides[0])) >= *(double *)(binx->data + j*(binx->strides[0])) &&  
	           *(double *)(f1->data + i*(f1->strides[0])) < *(double *)(binx->data + (j+1)*(binx->strides[0]))  ){
	        ix = j;
		break;
	      }
	    }
	    	    
	    /* find iy*/
	    for (j = 0; j < biny->dimensions[0]-1; j++){
	      if ( *(double *)(f2->data + i*(f2->strides[0])) >= *(double *)(biny->data + j*(biny->strides[0])) &&  
	           *(double *)(f2->data + i*(f2->strides[0])) < *(double *)(biny->data + (j+1)*(biny->strides[0]))  ){
	        iy = j;
		break;
	      }
	    }
	    
	    if (ix != -1 && iy != -1){
	      *(double *)(h->data + ix*(h->strides[0]) + iy*(h->strides[1])) = *(double *)(h->data + ix*(h->strides[0]) + iy*(h->strides[1])) + 1. ; 
	    }	    
	  
	  
	  }
        
      	  
	  return PyArray_Return(h);
      }


/*********************************/
/* hnd                           */
/*********************************/

static PyObject *
      myNumeric_hnd(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyObject *lst;
	  PyObject *tpl;
	  PyArrayObject *mat;
	  PyArrayObject *h;
	  
	  int i,d,ii;
	  int n;
	  float val;
	  
	  int offset,inbox;
	  
	  int dim;
	  float min,max;
	  
	  //int *ndim;
	  npy_intp *ndim;
	  float *nmin, *nmax;
	  
	  
	  
	  
	  /* parse arguments */    
          if (!PyArg_ParseTuple(args, "OO",&lst,&mat))		
              return NULL;

	  /***************/	
	  /* check input */
	  /***************/
	      	
	  /* check if lst is a list */		  
	  if (!PyList_Check(lst)){
	    PyErr_SetString(PyExc_ValueError,"Type of first argument must be list."); 
	    return NULL;
	  }
	  
	  /* check size */	
	  dim = PyList_Size(lst);

	  if (dim != mat->dimensions[1]){
	    PyErr_SetString(PyExc_ValueError,"First argument must have the same size than the second argument."); 
	    return NULL;
	  }	
	  
	  /* check type */
	  if(mat->descr->type_num != PyArray_FLOAT){
	    PyErr_SetString(PyExc_ValueError,"Type of second argument must be float."); 
	    return NULL;	  
	  }
	  	  
	  /* allocate memory */	  
          if(!(ndim = malloc(dim * sizeof(npy_intp))))
	    {PyErr_SetString(PyExc_ValueError,"Failed to allocate memory for ndim.");}	  
          if(!(nmin = malloc(dim * sizeof(float))))
	    {PyErr_SetString(PyExc_ValueError,"Failed to allocate memory for nmin.");}	
          if(!(nmax = malloc(dim * sizeof(float))))
	    {PyErr_SetString(PyExc_ValueError,"Failed to allocate memory for nmax.");}		
    	    
   	 
	  /* gather arguments in the list */
	  for (d = 0; d < dim; d++){
	  	  
	    tpl = PyList_GetItem(lst,d);
	    
	    /* check that tpl is a tuple */
	    if (!PyTuple_Check(tpl)){
	      PyErr_SetString(PyExc_ValueError,"Elements of first argument must be tuples."); 
	      return NULL;
	    }
	    /* check the content of the tuple */
            if (!PyArg_ParseTuple(tpl, "ffi",&min,&max,&n)){
	      PyErr_SetString(PyExc_ValueError,"Elements of tuples are wrong."); 
	      return NULL;
	    }  	    
	    ndim[d]=n;
	    nmin[d]=min;
	    nmax[d]=max;
	  }
	  

	  
	  
	  /* create the output */	  	  
	  //h = (PyArrayObject *) PyArray_FromDims(dim,ndim,PyArray_FLOAT); 	  
	  h = (PyArrayObject *) PyArray_SimpleNew(dim,ndim,NPY_FLOAT); 	
	  
	  /*************/	
	  /* compute h */
	  /*************/
	  
	  /* loop over all elements of mat */
	  for (i = 0; i < mat->dimensions[0]; i++) {
	  
	    /* loop over all dimensions */
	    offset = 0;
	    inbox = 1;
	    for (d = 0; d < dim; d++) {
	     
	      val = *(float *)(mat->data + i*(mat->strides[0]) + d*(mat->strides[1]) );
	      	      	      
	      /* compute indexes */
	      ii = (int)( (val - nmin[d]) / (nmax[d] - nmin[d]) * ndim[d] );	      
	      
	      /* compute offset */
	      offset = offset + ii*(h->strides[d]);	      
	      
	      /* if particle is out of the box */	      
	      if ( (ii < 0 ) || (ii >= ndim[d]) ) {
	        inbox = 0;
		}
		
	      //printf("val = %f, i=%d, d=%d ii=%d stride[d]=%d\n",val,i,d,ii,ii*(h->strides[d]));	
	      
	    }
	    
	    /* now, put the result at the right place */
	    if (inbox)
	      *(float *)(h->data + offset) = *(float *)(h->data + offset) + 1. ;
	    
	    
	  }
	  
	  

      	  
	  return PyArray_Return(h);
      }

/*********************************/
/* whistogram                    */
/*********************************/

static PyObject *
      myNumeric_whistogram(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *x;
	  PyArrayObject *m;
	  PyArrayObject *binx;
	  PyArrayObject *h;
	  
	  int	i,j,ix;
	  npy_intp   dim[1];
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOO",&x,&m,&binx))		
              return NULL;
	  
	  	  
	  /* check the types */	  
	     
	  if (x->descr->type_num != PyArray_DOUBLE){
	    PyErr_SetString(PyExc_ValueError,"type of first argument must be float.");
	    return NULL;
	  }

	  if (m->descr->type_num != PyArray_DOUBLE){
	    PyErr_SetString(PyExc_ValueError,"type of second argument must be float.");
	    return NULL;
	  }
	  
	  if (binx->descr->type_num != PyArray_DOUBLE){
	    PyErr_SetString(PyExc_ValueError,"type of third argument must be float.");
	    return NULL;
	  }	  
	  
	   	  
	  
	  
	  /* check the dimensions */
	  
	  if (x->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of first argument must be 1."); 
	    return NULL;
	  }

	  if (m->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of second argument must be 1."); 
	    return NULL;
	  }	
	  
	  if (binx->nd != 1){
	    PyErr_SetString(PyExc_ValueError,"dimension of third argument must be 1."); 
	    return NULL;
	  }	  
	  
	  /* -- */
	  
	  if (x->dimensions[0] != m->dimensions[0]){
	    PyErr_SetString(PyExc_ValueError,"first and second argument must have the same size."); 
	    return NULL;
	  }
	  
	  	  	  
	  /* create the output */
	  
	  dim[0]=binx->dimensions[0];
	  //h = (PyArrayObject *) PyArray_FromDims(1,dim,PyArray_DOUBLE); 
	  h = (PyArrayObject *) PyArray_SimpleNew(1,dim,NPY_DOUBLE);
	  
	  /* fill the output */
	  
	  /* loop over all elements of f1 and f2 */
	  for (i = 0; i < x->dimensions[0]; i++) {
	  	  
	    ix = binx->dimensions[0]-1;													
	  
	    /* find ix, loop over elements of binx */												
	    for (j = 0; j < binx->dimensions[0]-1; j++){  
	    
	      //printf("x[%d] binx[%d] %f - %f %f\n",i,j,*(double *)(x->data + i*(x->strides[0])),*(double *)(binx->data +     j*(binx->strides[0])),*(double *)(binx->data + (j+1)*(binx->strides[0])));

	    
	      /* smaller than the smallest */
	      if ( *(double *)(x->data + i*(x->strides[0])) < *(double *)(binx->data +     j*(binx->strides[0]))) {
	        ix = -1;
	        break;
	      }
	        	  
	    								
	      if ( *(double *)(x->data + i*(x->strides[0])) >= *(double *)(binx->data +     j*(binx->strides[0])) &&	
	    	   *(double *)(x->data + i*(x->strides[0])) <  *(double *)(binx->data + (j+1)*(binx->strides[0]))  ){	
	    	ix = j; 												
	    	break;
	      } 													
	    }														
	    														
	    if (ix != -1){			
	      *(double *)(h->data + ix*(h->strides[0])) = *(double *)(h->data + ix*(h->strides[0])) + *(double *)(m->data + i*(m->strides[0])) ; 
	    }	
	  
	  }  													
	  
	  
        
      	  
	  return PyArray_Return(h);
      }

/*********************************/
/* spline3d                      */
/*********************************/

static PyObject *
      myNumeric_spline3d(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *f1;
	  PyArrayObject *f2;
	  PyArrayObject *binx;
	  PyArrayObject *biny;
	  PyArrayObject *h;
	  
	  int	i,j,ix,iy;
	  int   dim[2];
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "OOOO",&f1,&f2,&binx,&biny))		
              return NULL;

	  return PyArray_Return(h);
      }      




/*********************************/
/* polint                        */
/*********************************/

static PyObject *
      myNumeric_polint(self, args)
          PyObject *self;
          PyObject *args;
      {
	  PyArrayObject *vxa,*vya;
	  int n,d,i;
    	  float x,y,dy;
	  	  
          if (!PyArg_ParseTuple(args, "OOf", &vxa,&vya,&x))		
              return NULL;
	  
	  
	  if ((vxa->dimensions[0])!=(vya->dimensions[0]))
	    {
              PyErr_SetString(PyExc_ValueError,"first and second arguments must have same dimension");
	      return NULL;
	    }  	  
	  
	  n = vxa->dimensions[0];
      
	  polint((float*)vxa->data,(float*)vya->data,n,x,&y,&dy); 

          return Py_BuildValue("f",y);

      }

/*********************************/
/* ratint                        */
/*********************************/

static PyObject *
      myNumeric_ratint(self, args)
          PyObject *self;
          PyObject *args;
      {
	  PyArrayObject *vxa,*vya;
	  int n,d,i;
    	  float x,y,dy;
	  	  
          if (!PyArg_ParseTuple(args, "OOf", &vxa,&vya,&x))		
              return NULL;
	  
	  
	  if ((vxa->dimensions[0])!=(vya->dimensions[0]))
	    {
              PyErr_SetString(PyExc_ValueError,"first and second arguments must have same dimension");
	      return NULL;
	    }  	  
	  
	  n = vxa->dimensions[0];
      
	  ratint((float*)vxa->data,(float*)vya->data,n,x,&y,&dy); 

          return Py_BuildValue("f",y);

      }


/*********************************/
/* spline                        */
/*********************************/

static PyObject *
      myNumeric_spline(self, args)
          PyObject *self;
          PyObject *args;
      {
	  PyArrayObject *vxa,*vya;
	  PyArrayObject *y2a;
	  int n,d,i;
    	  float dy;
	  float yp1,ypn;
	  	  
          if (!PyArg_ParseTuple(args, "OOff", &vxa,&vya,&yp1,&ypn))		
              return NULL;
	  
	  
	  if ((vxa->dimensions[0])!=(vya->dimensions[0]))
	    {
              PyErr_SetString(PyExc_ValueError,"first and second arguments must have same dimension");
	      return NULL;
	    }  	  
	  
	  n = vxa->dimensions[0];
	  
	  /* create output */
	  printf("myNumeric_spline : warning, we may have a problem here...");
	  //y2a = (PyArrayObject *) PyArray_FromDims(vxa->nd,vxa->dimensions,vxa->descr->type_num);                     
	  y2a = (PyArrayObject *) PyArray_SimpleNew(vxa->nd,vxa->dimensions,vxa->descr->type_num);
	  
	  spline((float*)vxa->data,(float*)vya->data,n,yp1,ypn,(float*)y2a->data);

          return PyArray_Return(y2a);

      }

/*********************************/
/* splint                        */
/*********************************/

static PyObject *
      myNumeric_splint(self, args)
          PyObject *self;
          PyObject *args;
      {
	  PyArrayObject *vxa,*vya,*y2a;
	  int n,d,i;
    	  float x,y,dy;
	  float yp1,ypn;
	  	  
          if (!PyArg_ParseTuple(args, "OOOf", &vxa,&vya,&y2a,&x))		
              return NULL;
	  
	  
	  if ((vxa->dimensions[0])!=(vya->dimensions[0]))
	    {
              PyErr_SetString(PyExc_ValueError,"first and second arguments must have same dimension");
	      return NULL;
	    }  	  
	  
	  n = vxa->dimensions[0];
      
	  splint((float*)vxa->data,(float*)vya->data,(float*)y2a->data,n,x,&y); 

          return Py_BuildValue("f",y);

      }      
/*********************************/
/* turnup                        */
/*********************************/
      
static PyObject *
      myNumeric_turnup(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *vec;
	  PyArrayObject *nvec;
	  
	  int	i,j,nx,ny;
	  int   axe,type;
	  	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "Oi", &vec,&axe))		
              return NULL;
	      
	  /* check the dimensions */
	  if (vec->nd != 2){
	    PyErr_SetString(PyExc_ValueError,"dimension of the first argument must be 2."); 
	    return NULL;
	  }
	  
	  /* check the value of axe */
	  if (axe != 0 && axe != 1){
	    PyErr_SetString(PyExc_ValueError,"value of the second argument must be 0 or 1."); 
	    return NULL;
	  }	  	      
	    
	  /* create a NumPy object similar to vec*/
	  printf("myNumeric_turnup : warning, we may have a problem here...");	  
	  //nvec = (PyArrayObject *) PyArray_FromDims(vec->nd,vec->dimensions,vec->descr->type_num);
	  nvec = (PyArrayObject *) PyArray_SimpleNew(vec->nd,vec->dimensions,vec->descr->type_num);

          nx = vec->dimensions[0];
	  ny = vec->dimensions[1];
	  
	  type = vec->descr->type_num;

	  switch (type)
	    {
	    /*****************/
	    /* astype(float) */
	    /*****************/
	    case PyArray_DOUBLE:	
	    
	     if (axe==0) {
               /* loops over all elements */
      	       for (i = 0; i < vec->dimensions[0]; i++) {
             	 for (j = 0; j < vec->dimensions[1]; j++) {
             	     *(double *)(nvec->data + i*(nvec->strides[0]) + (ny-j-1)*nvec->strides[1]) = 
             	     *(double *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
	     	 }
               }       
	     }
	     if (axe==1) {
               /* loops over all elements */
      	       for (i = 0; i < vec->dimensions[0]; i++) {
             	 for (j = 0; j < vec->dimensions[1]; j++) {
             	     *(double *)(nvec->data + (nx-i-1)*(nvec->strides[0]) + j*nvec->strides[1]) = 
             	     *(double *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
	     	 }
               }       
	     }
	     break;
	    /*****************/
	    /* astype(float0) */
	    /*****************/
	    case PyArray_FLOAT:		
	    
	     if (axe==0) {
               /* loops over all elements */
      	       for (i = 0; i < vec->dimensions[0]; i++) {
             	 for (j = 0; j < vec->dimensions[1]; j++) {
             	     *(float *)(nvec->data + i*(nvec->strides[0]) + (ny-j-1)*nvec->strides[1]) = 
             	     *(float *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
	     	 }
               }       
	     }
	     if (axe==1) {
               /* loops over all elements */
      	       for (i = 0; i < vec->dimensions[0]; i++) {
             	 for (j = 0; j < vec->dimensions[1]; j++) {
             	     *(float *)(nvec->data + (nx-i-1)*(nvec->strides[0]) + j*nvec->strides[1]) = 
             	     *(float *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
	     	 }
               }       
	     }
	     break;
	    /*****************/
	    /* astype(Int) */
	    /*****************/
	    case PyArray_LONG:		
	    
	     if (axe==0) {
               /* loops over all elements */
      	       for (i = 0; i < vec->dimensions[0]; i++) {
             	 for (j = 0; j < vec->dimensions[1]; j++) {
             	     *(long *)(nvec->data + i*(nvec->strides[0]) + (ny-j-1)*nvec->strides[1]) = 
             	     *(long *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
	     	 }
               }       
	     }
	     if (axe==1) {
               /* loops over all elements */
      	       for (i = 0; i < vec->dimensions[0]; i++) {
             	 for (j = 0; j < vec->dimensions[1]; j++) {
             	     *(long *)(nvec->data + (nx-i-1)*(nvec->strides[0]) + j*nvec->strides[1]) = 
             	     *(long *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
	     	 }
               }       
	     }
	     break;		    
//	    /*****************/
//	    /* astype(Int32) */
//	    /*****************/
//	    case PyArray_INT:		
//	    
//	     if (axe==0) {
//               /* loops over all elements */
//      	       for (i = 0; i < vec->dimensions[0]; i++) {
//             	 for (j = 0; j < vec->dimensions[1]; j++) {
//             	     *(int *)(nvec->data + i*(nvec->strides[0]) + (ny-j-1)*nvec->strides[1]) = 
//             	     *(int *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
//	     	 }
//               }       
//	     }
//	     if (axe==1) {
//               /* loops over all elements */
//      	       for (i = 0; i < vec->dimensions[0]; i++) {
//             	 for (j = 0; j < vec->dimensions[1]; j++) {
//             	     *(int *)(nvec->data + (nx-i-1)*(nvec->strides[0]) + j*nvec->strides[1]) = 
//             	     *(int *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
//	     	 }
//               }       
//	     }
//	     break;		    
	    /*****************/
	    /* astype(Int16) */
	    /*****************/
	    case PyArray_SHORT:		
	    
	     if (axe==0) {
               /* loops over all elements */
      	       for (i = 0; i < vec->dimensions[0]; i++) {
             	 for (j = 0; j < vec->dimensions[1]; j++) {
             	     *(short *)(nvec->data + i*(nvec->strides[0]) + (ny-j-1)*nvec->strides[1]) = 
             	     *(short *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
	     	 }
               }       
	     }
	     if (axe==1) {
               /* loops over all elements */
      	       for (i = 0; i < vec->dimensions[0]; i++) {
             	 for (j = 0; j < vec->dimensions[1]; j++) {
             	     *(short *)(nvec->data + (nx-i-1)*(nvec->strides[0]) + j*nvec->strides[1]) = 
             	     *(short *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
	     	 }
               }       
	     }
	     break;	    
	    /*****************/
	    /* astype(Int0) */		/* same than Int32 in numpy */
	    /*****************/
//	    case PyArray_SBYTE:
//	      	    
//	     if (axe==0) {
//               /* loops over all elements */
//      	       for (i = 0; i < vec->dimensions[0]; i++) {
//             	 for (j = 0; j < vec->dimensions[1]; j++) {
//             	     *(char *)(nvec->data + i*(nvec->strides[0]) + (ny-j-1)*nvec->strides[1]) = 
//             	     *(char *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
//	     	 }
//               }       
//	     }
//	     if (axe==1) {
//               /* loops over all elements */
//      	       for (i = 0; i < vec->dimensions[0]; i++) {
//             	 for (j = 0; j < vec->dimensions[1]; j++) {
//             	     *(char *)(nvec->data + (nx-i-1)*(nvec->strides[0]) + j*nvec->strides[1]) = 
//             	     *(char *)(vec->data + i*(vec->strides[0]) + j*vec->strides[1]);
//	     	 }
//               }       
//	     }
//	     break;	    
	     
	  
	  
	    }
	  return PyArray_Return(nvec);

      }
      
/*********************************/
/* expand                        */
/*********************************/
      
static PyObject *
      myNumeric_expand(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *vec;
	  PyArrayObject *nvec;
	  
	  int	i,j,ii,jj;
	  int   fx,fy,type;
	  npy_intp   ndimensions[2];
	  	  
	  
	  /* parse arguments */    
	        
          if (!PyArg_ParseTuple(args, "Oii", &vec,&fx,&fy))		
              return NULL;
	      
	  /* check the dimensions */
	  if (vec->nd != 2){
	    PyErr_SetString(PyExc_ValueError,"dimension of the first argument must be 2."); 
	    return NULL;
	  }
	  
	  /* check the value of axe */
	  if (fx <= 0 && fy <= 0){
	    PyErr_SetString(PyExc_ValueError,"value of the second and third argument must be greater or equal to 1"); 
	    return NULL;
	  }	  	      
	    
	  /* create a NumPy object similar to vec*/	
	  ndimensions[0]=vec->dimensions[0]*fx;
	  ndimensions[1]=vec->dimensions[1]*fy;
	    
	  //nvec = (PyArrayObject *) PyArray_FromDims(vec->nd,ndimensions,vec->descr->type_num);
	  nvec = (PyArrayObject *) PyArray_SimpleNew(vec->nd,ndimensions,vec->descr->type_num);
          type = vec->descr->type_num;
	  
	  switch (type)
	    {
	    /*****************/
	    /* astype(float) */
	    /*****************/
	    case PyArray_DOUBLE:	
	      /* loops over all elements */		   
              for (j = 0; j < vec->dimensions[1]; j++) {   
	        for (i = 0; i < vec->dimensions[0]; i++) {
	          for (jj = 0; jj < fy; jj++) {   
		    for (ii = 0; ii < fx; ii++) {
	 	      *(double *)(nvec->data + (i*fx+ii)*(nvec->strides[0]) + (j*fy+jj)*nvec->strides[1]) = 
	 	      *(double *)( vec->data + i*( vec->strides[0]) + j*vec->strides[1]);
	            }
	          }
	        }
	      }    
	     break;
	    /*****************/
	    /* astype(float0) */
	    /*****************/
	    case PyArray_FLOAT:	
	      /* loops over all elements */		   
              for (j = 0; j < vec->dimensions[1]; j++) {   
	        for (i = 0; i < vec->dimensions[0]; i++) {
	          for (jj = 0; jj < fy; jj++) {   
		    for (ii = 0; ii < fx; ii++) {
	 	      *(float *)(nvec->data + (i*fx+ii)*(nvec->strides[0]) + (j*fy+jj)*nvec->strides[1]) = 
	 	      *(float *)( vec->data + i*( vec->strides[0]) + j*vec->strides[1]);
	            }
	          }
	        }
	      }    
	     break;	     
	    /*****************/
	    /* astype(int) */
	    /*****************/
	    case PyArray_LONG:	
	      /* loops over all elements */		   
              for (j = 0; j < vec->dimensions[1]; j++) {   
	        for (i = 0; i < vec->dimensions[0]; i++) {
	          for (jj = 0; jj < fy; jj++) {   
		    for (ii = 0; ii < fx; ii++) {
	 	      *(long *)(nvec->data + (i*fx+ii)*(nvec->strides[0]) + (j*fy+jj)*nvec->strides[1]) = 
	 	      *(long *)( vec->data + i*( vec->strides[0]) + j*vec->strides[1]);
	            }
	          }
	        }
	      }    
	     break;	     
//	    /*****************/
//	    /* astype(int32) */
//	    /*****************/
//	    case PyArray_INT:	
//	      /* loops over all elements */		   
//              for (j = 0; j < vec->dimensions[1]; j++) {   
//	        for (i = 0; i < vec->dimensions[0]; i++) {
//	          for (jj = 0; jj < fy; jj++) {   
//		    for (ii = 0; ii < fx; ii++) {
//	 	      *(int *)(nvec->data + (i*fx+ii)*(nvec->strides[0]) + (j*fy+jj)*nvec->strides[1]) = 
//	 	      *(int *)( vec->data + i*( vec->strides[0]) + j*vec->strides[1]);
//	            }
//	          }
//	        }
//	      }    
//	     break;	     
	    /*****************/
	    /* astype(int16) */
	    /*****************/
	    case PyArray_SHORT:	
	      /* loops over all elements */		   
              for (j = 0; j < vec->dimensions[1]; j++) {   
	        for (i = 0; i < vec->dimensions[0]; i++) {
	          for (jj = 0; jj < fy; jj++) {   
		    for (ii = 0; ii < fx; ii++) {
	 	      *(short *)(nvec->data + (i*fx+ii)*(nvec->strides[0]) + (j*fy+jj)*nvec->strides[1]) = 
	 	      *(short *)( vec->data + i*( vec->strides[0]) + j*vec->strides[1]);
	            }
	          }
	        }
	      }    
	     break;		     
	    /*****************/
	    /* astype(int0) */		/* same than Int32 in numpy */
	    /*****************/
//	    case PyArray_SBYTE:	
//	      /* loops over all elements */		   
//              for (j = 0; j < vec->dimensions[1]; j++) {   
//	        for (i = 0; i < vec->dimensions[0]; i++) {
//	          for (jj = 0; jj < fy; jj++) {   
//		    for (ii = 0; ii < fx; ii++) {
//	 	      *(char *)(nvec->data + (i*fx+ii)*(nvec->strides[0]) + (j*fy+jj)*nvec->strides[1]) = 
//	 	      *(char *)( vec->data + i*( vec->strides[0]) + j*vec->strides[1]);
//	            }
//	          }
//	        }
//	      }    
//	     break;	     
	     }
	    
     
	  
	  
	  return PyArray_Return(nvec);

      }





/*********************************/
/* Interpolate_From_1d_Array        */
/*********************************/
      
static PyObject *
      myNumeric_Interpolate_From_1d_Array(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *idx,*mat;
	  
	  int i;
	  float ix;
	  int x1,x2;
	  float y1,y2;
	  PyArrayObject *out;
	   
	  /* parse arguments */    
          if (!PyArg_ParseTuple(args, "OO", &idx,&mat))		
              return NULL;
	      
	  /* look at the dimension */
	  if ((idx->nd!=1))
	    {
              PyErr_SetString(PyExc_ValueError,"dimension of arguments 1 must be 1.\n");
	      return NULL;	
	    }    	  

	  /* look at the dimension */
	  if ((mat->nd)!=1)
	    {
              PyErr_SetString(PyExc_ValueError,"dimension of argument 2 must be 1.\n");
	      return NULL;	
	    }     
	  
	  	  
	  /* create the output */
	  //out = (PyArrayObject *) PyArray_FromDims(idx->nd,idx->dimensions,idx->descr->type_num);
	  out = (PyArrayObject *) PyArray_SimpleNew(idx->nd,idx->dimensions,PyArray_FLOAT);
	  
	  
          for (i = 0; i < idx->dimensions[0]; i++) 
	    {
	  
	      ix  = *(float *) (idx->data + i*(idx->strides[0])); 
	
	      if (ix <= 0)
	              *(float*)(out->data + i*(out->strides[0])) = *(float*)(mat->data + 0*(mat->strides[0]));
	      else
	        {
	          if (ix >= (mat->dimensions[0]-1))
	            {
	              *(float*)(out->data + i*(out->strides[0])) = *(float*)(mat->data + (mat->dimensions[0]-1)*(mat->strides[0]));
	            }			
	          else
	            {
	              
	              x1 = (int)ix;
	              x2 = x1+1;
	        			      
	              y1 = *(float*)(mat->data + (x1)*(mat->strides[0]));
	              y2 = *(float*)(mat->data + (x2)*(mat->strides[0]));
		      
	              
	              *(float*)(out->data + i*(out->strides[0])) = (ix - x1)/(x2-x1)*(y2-y1) + y1;
		      // *(float*)(out->data + i*(out->strides[0])) = y1;
	              
	            }
	        }
		
	    }
	    
	  return PyArray_Return(out);
      }
      


/*********************************/
/* Interpolate_From_2d_Array        */
/*********************************/
      
static PyObject *
      myNumeric_Interpolate_From_2d_Array(self, args)
          PyObject *self;
          PyObject *args;
      {
      	  
	  PyArrayObject *idx,*idy,*mat;
	  
	  int i;
	  float ix,iy;
	  int x1,x2,y1,y2;
	  float f1,f2,f3,f4;
	  float w1,w2,w3,w4;
	  int nx,ny;
	  PyArrayObject *out;
	   
	  /* parse arguments */    
          if (!PyArg_ParseTuple(args, "OOO", &idx,&idy,&mat))		
              return NULL;
	      
	  /* look at the dimension */
	  if ((idx->nd!=1) || (idy->nd!=1))
	    {
              PyErr_SetString(PyExc_ValueError,"dimension of arguments 1 and 2 must be 1.\n");
	      return NULL;	
	    }    	  

	  /* look at the dimension */
	  if ((idx->dimensions[0])!=(idy->dimensions[0]))
	    {
              PyErr_SetString(PyExc_ValueError,"Arguments 1 and 2 must have the same size.\n");
	      return NULL;	
	    }    	 
	    	  
	  
	  nx = mat->dimensions[0];
	  ny = mat->dimensions[1];
	  
	   	  
	  /* create the output */
	  //out = (PyArrayObject *) PyArray_FromDims(idx->nd,idx->dimensions,idx->descr->type_num);
	  out = (PyArrayObject *) PyArray_SimpleNew(idx->nd,idx->dimensions,PyArray_FLOAT);
	  	  
	  
          for (i = 0; i < idx->dimensions[0]; i++) 
	    {
	    	  
	      	  
	      ix  = *(float *) (idx->data + i*(idx->strides[0])); 
	      iy  = *(float *) (idy->data + i*(idy->strides[0]));
	      
		
	      /* 5 different cases */
	      
	      
	      if ( ((int)ix>=0) && ((int)ix<nx-1) && ((int)iy>=0) && ((int)iy<ny-1) )
	        {
		  
		  x1 = (int)ix;
		  x2 = (int)ix + 1;
		  y1 = (int)iy;
		  y2 = (int)iy + 1;
		  
		  
		  w1 = (x2-ix)*(y2-iy);
                  w2 = (x2-ix)*(iy-y1);
                  w3 = (ix-x1)*(y2-iy);
                  w4 = (ix-x1)*(iy-y1);
		  		  
		  
		  f1 = *(float*)(mat->data + (x1)*(mat->strides[0]) + (y1)*(mat->strides[1]));
		  f2 = *(float*)(mat->data + (x1)*(mat->strides[0]) + (y2)*(mat->strides[1]));
		  f3 = *(float*)(mat->data + (x2)*(mat->strides[0]) + (y1)*(mat->strides[1]));
		  f4 = *(float*)(mat->data + (x2)*(mat->strides[0]) + (y2)*(mat->strides[1]));
		  
		  *(float*)(out->data + i*(out->strides[0])) = (w1*f1 + w2*f2 + w3*f3 + w4*f4);
		
		  		  
		}
	      else
	        {
	          
		  
		  
		  if ( ((int)ix<0) && ((int)iy<0) )
		    {
		      *(float*)(out->data + i*(out->strides[0])) = *(float*)(mat->data + (0)*(mat->strides[0]) + (0)   *(mat->strides[1]));
		    }
		    
		  if ( ((int)ix<0) && ((int)iy>=ny-1) )
		    {
		      *(float*)(out->data + i*(out->strides[0])) = *(float*)(mat->data + (0)*(mat->strides[0]) + (ny-1)*(mat->strides[1]));
		    }		    
		    
		  if ( ((int)ix>=nx-1) && ((int)iy<0) )
		    {
		      *(float*)(out->data + i*(out->strides[0])) = *(float*)(mat->data + (nx-1)*(mat->strides[0]) + (0)   *(mat->strides[1]));
		    }
		    
		  if ( ((int)ix>=nx-1) && ((int)iy>=ny-1) )
		    {
		      *(float*)(out->data + i*(out->strides[0])) = *(float*)(mat->data + (nx-1)*(mat->strides[0]) + (ny-1)*(mat->strides[1]));	
		    }		  
		  
		  if ( ((int)ix>=0) && ((int)ix<nx-1) &&  ((int)iy<0) )
		    {
                      x1 = (int)ix;
	              x2 = x1+1;
	              y1 = *(float*)(mat->data + (x1)	*(mat->strides[0]) + (0)*(mat->strides[1]));
	              y2 = *(float*)(mat->data + (x2)	*(mat->strides[0]) + (0)*(mat->strides[1]));		       
		      *(float*)(out->data + i*(out->strides[0])) = (ix - x1)/(x2-x1)*(y2-y1) + y1;
		    }
		    
		  if ( ((int)ix>=0) && ((int)ix<nx-1) &&  ((int)iy>=ny-1) )
                    {
                      x1 = (int)ix;
	              x2 = x1+1;
	              y1 = *(float*)(mat->data + (x1)	*(mat->strides[0]) + (ny-1)*(mat->strides[1]));
	              y2 = *(float*)(mat->data + (x2)	*(mat->strides[0]) + (ny-1)*(mat->strides[1])); 	       
		      *(float*)(out->data + i*(out->strides[0])) = (ix - x1)/(x2-x1)*(y2-y1) + y1;
		    }
		    
		  if ( ((int)iy>=0) && ((int)iy<ny-1) &&  ((int)ix<0) )
                    {
                      x1 = (int)iy;
	              x2 = x1+1;
	              y1 = *(float*)(mat->data + (0)   *(mat->strides[0]) + (x1)*(mat->strides[1]));
	              y2 = *(float*)(mat->data + (0)   *(mat->strides[0]) + (x2)*(mat->strides[1]));		       
		      *(float*)(out->data + i*(out->strides[0])) = (iy - x1)/(x2-x1)*(y2-y1) + y1;
		    }
		    
		  if ( ((int)iy>=0) && ((int)iy<ny-1) &&  ((int)ix>=nx-1) )
                    {
                      x1 = (int)iy;
	              x2 = x1+1;
	              y1 = *(float*)(mat->data + (nx-1)   *(mat->strides[0]) + (x1)*(mat->strides[1]));
	              y2 = *(float*)(mat->data + (nx-1)   *(mat->strides[0]) + (x2)*(mat->strides[1])); 	       
		      *(float*)(out->data + i*(out->strides[0])) = (iy - x1)/(x2-x1)*(y2-y1) + y1;
		    }		  
		  
		  		  		    
		  
	        }
				
		
	    }
	    
	  return PyArray_Return(out);
      }

/*************************/       
/* rotx                  */
/*************************/ 
      
static PyObject *
      myNumeric_rotx(self, args)
          PyObject *self;
          PyObject *args;
      {
          PyArrayObject *pos, *theta;
	  PyArrayObject *rpos;
	  
	  float cs,ss;
          float xs;
	  float *x,*y,*z;
	  float rx,ry,rz;
	  int i;
	            
          if (!PyArg_ParseTuple(args, "OO", &pos, &theta))
              return NULL;
       
	  	  
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
		
		cs = cos(*(float *)(theta->data + i*(theta->strides[0])));
                ss = sin(*(float *)(theta->data + i*(theta->strides[0])));
		
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
      myNumeric_roty(self, args)
          PyObject *self;
          PyObject *args;
      {
          PyArrayObject *pos, *theta;
	  PyArrayObject *rpos;
	  
	  float cs,ss;
          float xs;
	  float *x,*y,*z;
	  float rx,ry,rz;
	  int i;
	            
          if (!PyArg_ParseTuple(args, "OO", &pos, &theta))
              return NULL;
        	  
	  
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
		
		cs = cos(*(float *)(theta->data + i*(theta->strides[0])));
                ss = sin(*(float *)(theta->data + i*(theta->strides[0])));
				
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
      myNumeric_rotz(self, args)
          PyObject *self;
          PyObject *args;
      {
          PyArrayObject *pos, *theta;
	  PyArrayObject *rpos;
	  
	  float cs,ss;
          float xs;
	  float *x,*y,*z;
	  float rx,ry,rz;
	  int i;
	            
          if (!PyArg_ParseTuple(args, "OO", &pos, &theta))
              return NULL;
        	  
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

		cs = cos(*(float *)(theta->data + i*(theta->strides[0])));
                ss = sin(*(float *)(theta->data + i*(theta->strides[0])));
				
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
      



            
/* definition of the method table */      
      
static PyMethodDef myNumericMethods[] = {

          {"test",  myNumeric_test, METH_VARARGS,
           "Some test on PyArray object."},  

          {"lininterp1d",  myNumeric_lininterp1d, METH_VARARGS,
           "Linear interpolation of 1d function given by two vectors."},  


          {"quadinterp1d",  myNumeric_quadinterp1d, METH_VARARGS,
           "Quadratic interpolation of 1d function given by two vectors."},  

          {"quaddinterp1d",  myNumeric_quaddinterp1d, METH_VARARGS,
           "Quadratic interpolation of 1d function given by two vectors (the slope is continuous)."},  


          {"vprod",  myNumeric_vprod, METH_VARARGS,
           "Calculate the vectorial product of two vectors."}, 
	   	   
          {"getmask",  myNumeric_getmask, METH_VARARGS,
           "Return a mask of the same type as x which has ones where elemets of x that have a corespondant in y and zeros instead."},  	   

          {"histogram2d",  myNumeric_histogram2d, METH_VARARGS,
           "Return a 2d matrix corresponding to the histrogram of two   vector values in given ranges."},  	   

          {"hnd",  myNumeric_hnd, METH_VARARGS,
           "Return a 3d matrix corresponding to the histrogram in n dim of a vector 3xn"}, 

          {"whistogram",  myNumeric_whistogram, METH_VARARGS,
           "Return a weighted histogram."},  	   

          {"spline3d",  myNumeric_spline3d, METH_VARARGS,
           "Return a 3d interpolation."}, 
	   
          {"polint",  myNumeric_polint, METH_VARARGS,
           "Polynomial interpolation."},		    

          {"ratint",  myNumeric_ratint, METH_VARARGS,
           "Polynomial interpolation."},	

          {"spline",  myNumeric_spline, METH_VARARGS,
           "spline."},	
	   
          {"splint",  myNumeric_splint, METH_VARARGS,
           "splint."},		   

          {"turnup",  myNumeric_turnup, METH_VARARGS,
           "Turn up a matrix."},

          {"expand",  myNumeric_expand, METH_VARARGS,
           "Expand a matrix."},	    	   	   	   

          {"Interpolate_From_1d_Array",  myNumeric_Interpolate_From_1d_Array, METH_VARARGS,
           "Interpolate values from a given array."},	    

          {"Interpolate_From_2d_Array",  myNumeric_Interpolate_From_2d_Array, METH_VARARGS,
           "Interpolate values from a given array."},	    

          {"rotx",  myNumeric_rotx, METH_VARARGS,
           "Rotation around the x axis."},	
	   
          {"roty",  myNumeric_roty, METH_VARARGS,
           "Rotation around the y axis."},
	   
          {"rotz",  myNumeric_rotz, METH_VARARGS,
           "Rotation around the z axis."},	   	       
  
	   	   
          {NULL, NULL, 0, NULL}        /* Sentinel */
      };      
      
      

      
void initmyNumeric(void)
      {    
          (void) Py_InitModule("myNumeric", myNumericMethods);	
	  
	  import_array();
      }      
      
