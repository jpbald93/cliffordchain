import sys, itertools
sys.path.insert(0,'.')
from gq import *
v=[int(x) for x in sys.argv[1:]]
c=[G(v[2*k],v[2*k+1]) for k in range(6)]
print('c',c,'genpos',genpos(c))
P,Q=kern(c); print('P3',P[3],'Q2',Q[2])
def concyc(z):  # 4x4 det rows (|z|^2,x,y,1) over Fractions
    M=[[G(w.n2()),G(w.r),G(w.i),G(1)] for w in z]; return det(M).r
# Gamma circles all genuine (seconds noncollinear) and level-4 points
for S in itertools.combinations(range(6),4):
    cs=[c[k] for k in S]; m=miquel(cs)
    for T in itertools.combinations(range(4),3):
        s=[second(cs[a],cs[b]) for a,b in itertools.combinations(T,2)]
        assert concyc(s+[m])==0
lines=[]
for i in range(6):
    sub=[c[k] for k in range(6) if k!=i]
    pts=[miquel([sub[k] for k in T]) for T in itertools.combinations(range(5),4)]
    col=[((p-pts[0])*(pts[1]-pts[0]).conj()).i for p in pts]
    print('sub',i,'pts',pts,'distinct',len(set(pts)),'collinear',all(x==0 for x in col))
    lines.append((pts[0],pts[1]-pts[0]))
# concurrency of L0 L1 L2
import fractions
def coeffs(L):
    p,d=L; # line: Im((z-p)*conj d)=0 -> a x + b y = e
    # (x+iy - p)(d.r - i d.i): imag = y d.r - x d.i - (p.i d.r - p.r d.i)
    return (-d.i, d.r, p.i*d.r-p.r*d.i)
a=[coeffs(L) for L in lines]
D=lambda u,v,w: u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0])
print('concurrency dets of triples:',[D(a[i],a[j],a[k]) for i,j,k in itertools.combinations(range(6),3)][:6])
