#define _CRT_SECURE_NO_WARNINGS

/* From standard C library */
#include <math.h>
#include <stdio.h>
#include <errno.h>
#include <stdarg.h>
#include <stdlib.h>
//#include "unistd.h"

/* From OpenCV library */
#include <opencv/cv.h>
#include <opencv/cxcore.h>
#include <opencv/highgui.h>

#define MAX_OBJECTS 1

typedef struct params {
	CvPoint loc1[MAX_OBJECTS];
	CvPoint loc2[MAX_OBJECTS];
	IplImage* objects[MAX_OBJECTS];
	char* win_name;
	IplImage* orig_img;
	IplImage* cur_img;
	int n;
} params;


#ifndef TRUE
#define TRUE 1
#endif
#ifndef FALSE
#define FALSE 0
#endif
#ifndef MIN
#define MIN(x,y) ( ( x < y )? x : y )
#endif
#ifndef MAX
#define MAX(x,y) ( ( x > y )? x : y )
#endif
#ifndef ABS
#define ABS(x) ( ( x < 0 )? -x : x )
#endif


void mouse( int event, int x, int y, int flags, void* param )
{
	params* p = (params*)param;
	CvPoint* loc;
	int n;
	IplImage* tmp;
	static int pressed = FALSE;
  
	/* on left button press, remember first corner of rectangle around object */
	if( event == CV_EVENT_LBUTTONDOWN )
	{
		n = p->n;
		if( n == MAX_OBJECTS ){ return; }
		loc = p->loc1;
		loc[n].x = x;
		loc[n].y = y;
		pressed = TRUE;
	}

	/* on left button up, finalize the rectangle and draw it in black */
	else if( event == CV_EVENT_LBUTTONUP )
	{
		n = p->n;
		if( n == MAX_OBJECTS ){ return; }
		loc = p->loc2;
		loc[n].x = x;
		loc[n].y = y;
		cvReleaseImage( &(p->cur_img) );
		p->cur_img = NULL;
		cvRectangle( p->orig_img, p->loc1[n], loc[n], CV_RGB(0,0,0), 1, 8, 0 );
		cvShowImage( p->win_name, p->orig_img );
		pressed = FALSE;
		p->n++;
	}

	/* on mouse move with left button down, draw rectangle as defined in white */
	else if( event == CV_EVENT_MOUSEMOVE  &&  flags & CV_EVENT_FLAG_LBUTTON )
	{
		n = p->n;
		if( n == MAX_OBJECTS ){ return; }
		tmp = (IplImage*)cvClone( p->orig_img );
		loc = p->loc1;
		cvRectangle( tmp, loc[n], cvPoint(x, y), CV_RGB(255,255,255), 1, 8, 0 );
		cvShowImage( p->win_name, tmp );
		if( p->cur_img )
		{
			cvReleaseImage( &(p->cur_img) );
		}
		p->cur_img = tmp;
	}
}


int get_regions( IplImage* frame, CvRect** regions )
{
	char* win_name = "First frame";
	params p;
	CvRect* r;
	int i, x1, y1, x2, y2, w, h;
  
	/* use mouse callback to allow user to define object regions */
	p.win_name = win_name;
	p.orig_img = (IplImage*)cvClone( frame );
	p.cur_img = NULL;
	p.n = 0;
	cvNamedWindow( win_name, 1 );
	cvShowImage( win_name, frame );
	cvSetMouseCallback( win_name, &mouse, &p );
	cvWaitKey( 0 );
	cvDestroyWindow( win_name );
	cvReleaseImage( &(p.orig_img) );
	if( p.cur_img )
	{
		cvReleaseImage( &(p.cur_img) );
	}

	/* extract regions defined by user; store as an array of rectangles */
	if( p.n == 0 )
	{
		*regions = NULL;
		return 0;
	}
	r = (CvRect*)malloc( p.n * sizeof( CvRect ) );
	for( i = 0; i < p.n; i++ )
	{
		x1 = MIN( p.loc1[i].x, p.loc2[i].x );
		x2 = MAX( p.loc1[i].x, p.loc2[i].x );
		y1 = MIN( p.loc1[i].y, p.loc2[i].y );
		y2 = MAX( p.loc1[i].y, p.loc2[i].y );
		w = x2 - x1;
		h = y2 - y1;

		/* ensure odd width and height */
		w = ( w % 2 )? w : w+1;
		h = ( h % 2 )? h : h+1;
		r[i] = cvRect( x1, y1, w, h );
	}
	*regions = r;
	return p.n;
}




/*********************************** Main ************************************/
#define LIM_W 200
#define LIM_H 160

int main( int argc, char** argv )
{
	CvCapture* video;
	IplImage *frame, *vis;
	// IplImage* frames[2048];
	int i = 0, num_objects = 0;
	CvRect* regions = NULL;
	int x0,y0, x1,y1, w,h;
	int flag = 1;
	
	char srcpath[256], dstpath[256];
	strcpy( srcpath, (argc > 1) ? argv[1] : "C:\\Users\\du\\Pictures\\B.jpg" );
	strcpy( dstpath, (argc > 2) ? argv[2] : "C:\\Users\\du\\Pictures\\B_resized.jpg" );
	
	video = cvCaptureFromFile( srcpath );
	frame = cvQueryFrame( video );
	while( flag )
	{
		vis = cvCloneImage( frame );
		while( 0 == num_objects )
		{
			fprintf( stderr, "Please select a object\n" );
			num_objects = get_regions( vis, &regions );
		}
		num_objects = 0;

		x0 = regions->x;
		y0 = regions->y;
		w  = regions->width;
		h  = regions->height;
		x1 = x0 + w - 1;
		y1 = y0 + h - 1;
		cvRectangle( vis, cvPoint( x0, y0 ), cvPoint( x1, y1 ), CV_RGB(255,0,0), 2, 8, 0 );

		if( w > LIM_W && h > LIM_H )
		{
			flag = 0;
			cvSetImageROI( frame, cvRect(x0,y0,LIM_W,LIM_H) );
			cvSaveImage( dstpath, frame, 0 );
			cvResetImageROI( frame );
		}
		else
		{
			printf( "the size (%3d,%3d) is too small\n\n", w, h );
		}

		cvNamedWindow( "Video", 1 );
		cvShowImage( "Video", vis );
		if(cvWaitKey( 5 ) == 27){ break; }
		cvDestroyWindow( "Video" );
	}
	//
	cvReleaseCapture( &video );
}