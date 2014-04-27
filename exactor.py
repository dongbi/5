import cv2
import random
import numpy as np

SZ = 5
NUM = 50

def generate_sub_box(w,h):
    l,t,r,b = 0,0,w,h

    '''
    while True:
        nl, nr = random.randint(l,r), random.randint(l,r)
        if nl < nr:
            break
    while True:
        nt, nb = random.randint(t,b), random.randint(t,b)
        if nt < nb:
            break
    '''
    while True:
        nl = random.randint(l,r)
        nr = nl + SZ
        if nr < r:
            break
    while True:
        nt = random.randint(t,b)
        nb = nt + SZ
        if nb < b:
            break

    return (nl, nt, SZ, SZ)

def ROI(src, roi):
    l = roi[0]
    t = roi[1]
    r = l + roi[2]
    b = t + roi[3]
    return src[t:b, l:r].reshape([-1,1])

        

class SparseBase:
    def __init__(self,w=200,h=150):
        self.val = []
        self.box = []
        self.color = []
        for i in range(NUM):
            n23 = random.choice([2,3])
            self.val.append([ random.choice([-1,1]) for i in range(n23) ])
            self.box.append([ generate_sub_box(w,h) for i in range(n23) ])
            self.color.append([ (random.randint(0,255),random.randint(0,255),random.randint(0,255)) for i in range(n23) ])

    def __repr__(self):
        ss = ''
        for i in range(len(self.val)):
            ss += '%d\n' % i
            for j in range(len(self.val[i])):
                ss += "%2d:" % self.val[i][j]
                ss += "[%d,%d,%d,%d]\n" % (self.box[i][j][0],self.box[i][j][1],self.box[i][j][2],self.box[i][j][3])
            ss += '\n'
        return ss

    def represent(self,src):
        src = cv2.cvtColor( src, 7 )
        arr = np.zeros([SZ**2,NUM], dtype=np.int32)
        for i in range(len(self.val)):
            for j in range(len(self.val[i])):
                arr[:,i] += self.val[i][j] * ROI(src,self.box[i][j])[:,0]
        return arr

    def drawRect(self,src):
        for i in range(len(self.val)):
            for j in range(len(self.val[i])):
                l = self.box[i][j][0]
                t = self.box[i][j][1]
                r = l + self.box[i][j][2]
                b = t + self.box[i][j][3]
                cv2.rectangle( src, (l,t), (r,b), self.color[i][j], 2 )

if __name__ == '__main__':

    import os, sys
    path = os.path.join( os.path.expanduser('~'), 'Pictures', 'B.jpg' )
    
    im = cv2.imread( path )
    R,C,D = im.shape
    base = SparseBase(C,R)

    base.drawRect( im )
    while True:
        cv2.imshow( 'win', im )
        ch = cv2.waitKey(1)
        if 27 == ch:
            break
    cv2.destroyWindow( 'win' )
                                         
