import os

N = 81

if not os.path.exists( r'./div4' ):
    os.mkdir( './div4' )
if not os.path.exists( r'./div16' ):
    os.mkdir( './div16' )


# makeup_feature
cmd = os.path.join( os.path.curdir, 'split.py' )
pic = os.path.join( os.path.curdir, 'img', '%04d.bmp' )
ret = os.path.join( os.path.curdir, 'div4', '%04d.bmp' )

f = open('run_me_1st.bat', 'w')
for i in range(1,N+1):
    bat = ' '.join([
        os.path.abspath(cmd),
        os.path.abspath(pic%i),
        os.path.abspath(ret%(4*i-4)),
        os.path.abspath(ret%(4*i-3)),
        os.path.abspath(ret%(4*i-2)),
        os.path.abspath(ret%(4*i-1))
    ])
    f.write( bat + '\n' )
f.write( 'pause\n\n' )
f.close()


N = N * 4

# makeup_feature
cmd = os.path.join( os.path.curdir, 'split.py' )
pic = os.path.join( os.path.curdir, 'div4', '%04d.bmp' )
ret = os.path.join( os.path.curdir, 'div16', '%04d.bmp' )

f = open('run_me_2nd.bat', 'w')
for i in range(N):
    bat = ' '.join([
        os.path.abspath(cmd),
        os.path.abspath(pic%i),
        os.path.abspath(ret%(4*i)),
        os.path.abspath(ret%(4*i+1)),
        os.path.abspath(ret%(4*i+2)),
        os.path.abspath(ret%(4*i+3))
    ])
    f.write( bat + '\n' )
f.write( 'pause\n\n' )
f.close()
