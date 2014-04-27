#!/usr/bin/env python

'''
Multitarget planar tracking
==================

Example of using features2d framework for interactive video homography matching.
ORB features and FLANN matcher are used. This sample provides PlaneTracker class
and an example of its usage.

video: http://www.youtube.com/watch?v=pzVbhxx6aog

Usage
-----
plane_tracker.py [<video source>]

Keys:
   SPACE  -  pause video
   c      -  clear targets

Select a textured planar object to track by drawing a box with a mouse.
'''

import numpy as np
import cv2
import video
import common


class App:
    def __init__(self, src):
        self.cap = video.create_capture(src)
        self.frame = None
        self.rect_obj = None

        cv2.namedWindow('plane')
        self.rect_sel = common.RectSelector('plane', self.on_rect)

    def on_rect(self, rect):
        self.rect_obj = (rect[0], rect[1], 200, 160)

    def run(self):
        while True:
            if (not self.rect_sel.dragging) or (self.frame is None):
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.frame = frame.copy()

            vis = self.frame.copy()
            if self.rect_obj:
                l = self.rect_obj[0]
                t = self.rect_obj[1]
                r = self.rect_obj[0] + self.rect_obj[2]
                b = self.rect_obj[1] + self.rect_obj[3]
                cv2.rectangle( vis, (l,t), (r,b), (255,255,0), 2 )
            
            self.rect_sel.draw(vis)
            cv2.imshow('plane', vis)
            
            ch = cv2.waitKey(1)
            if ch == ord(' '):
                cv2.imwrite( './cap.jpg', frame[t:b, l:r] )
                break
            if ch == 27:
                break

        cv2.destroyWindow('plane')

class App2:
    def __init__(self, src):
        self.dst = './resized_' + src[-8:]
        self.frame = cv2.imread(src)
        self.rect_obj = None

        cv2.namedWindow('plane')
        self.rect_sel = common.RectSelector('plane', self.on_rect)

    def on_rect(self, rect):
        self.rect_obj = (rect[0], rect[1], 200, 160)

    def run(self):
        while True:
            vis = self.frame.copy()
            if self.rect_obj:
                l = self.rect_obj[0]
                t = self.rect_obj[1]
                r = self.rect_obj[0] + self.rect_obj[2]
                b = self.rect_obj[1] + self.rect_obj[3]
                cv2.rectangle( vis, (l,t), (r,b), (255,255,0), 2 )
            
            self.rect_sel.draw(vis)
            cv2.imshow('plane', vis)
            
            ch = cv2.waitKey(1)
            if ch == ord(' '):
                cv2.imwrite( self.dst, self.frame[t:b, l:r] )
                break
            if ch == 27:
                break

        cv2.destroyWindow('plane')


if __name__ == '__main__':
    print __doc__

    import sys
    
    try:
        image_src = sys.argv[1]
        App2(image_src).run()
        
    except:
        video_src = 0
        App(video_src).run()
    
