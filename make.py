import os
import cv2
import csv
import exactor

N = 1296

if not os.path.exists( r'./tmp' ):
    os.mkdir( './tmp' )

# exactor_feature
# pic = os.path.join( os.path.expanduser('~'), 'Pictures', 'coal' )
cmd = os.path.join( os.path.curdir, 'exactor.exe' )
pic = os.path.join( os.path.curdir, 'pic', 'div16' )
out = os.path.join( os.path.curdir, 'tmp' )

for i in range(N):
    path = os.path.join( pic, '%04d'%i + r'.bmp' )
    im = cv2.imread( path )

    path = os.path.join( out, '%04d'%i + r'.csv' )
    writer = csv.writer( file(path,'wb') )
    
    base = exactor.SparseBase()
    mat = base.represent( im ).tolist()

    for line in mat:
        writer.writerow( line )

    print i

    '''
    base.drawRect( im )
    while True:
        cv2.imshow( 'win', im )
        ch = cv2.waitKey(1)
        if 27 == ch:
            break
    cv2.destroyWindow( 'win' )
    '''
