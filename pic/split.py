#!/usr/bin/env python

'''
Divide image into 4
'''

import cv2
import sys

im = cv2.imread( sys.argv[1] )
R,C,D = im.shape
cv2.imwrite( sys.argv[2], im[0:(R/2), 0:(C/2)] )
cv2.imwrite( sys.argv[3], im[(R/2):R, 0:(C/2)] )
cv2.imwrite( sys.argv[4], im[0:(R/2), (C/2):C] )
cv2.imwrite( sys.argv[5], im[(R/2):R, (C/2):C] )
