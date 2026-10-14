from fractions import Fraction as F
import itertools, random, sys
class G:
    __slots__=('r','i')
    def __init__(s,r,i=0): s.r=F(r); s.i=F(i)
    def __add__(s,o): o=o if isinstance(o,G) else G(o); return G(s.r+o.r,s.i+o.i)
    __radd__=__add__
    def __sub__(s,o): o=o if isinstance(o,G) else G(o); return G(s.r-o.r,s.i-o.i)
    def __rsub__(s,o): return G(o)-s
    def __neg__(s): return G(-s.r,-s.i)
    def __mul__(s,o): o=o if isinstance(o,G) else G(o); return G(s.r*o.r-s.i*o.i,s.r*o.i+s.i*o.r)
    __rmul__=__mul__
    def conj(s): return G(s.r,-s.i)
    def n2(s): return s.r*s.r+s.i*s.i
    def __truediv__(s,o): o=o if isinstance(o,G) else G(o); d=o.n2(); t=s*o.conj(); return G(t.r/d,t.i/d)
    def iszero(s): return s.r==0 and s.i==0
    def __eq__(s,o): o=o if isinstance(o,G) else G(o); return s.r==o.r and s.i==o.i
    def __hash__(s): return hash((s.r,s.i))
    def __repr__(s): return f"({s.r})+({s.i})i"
def det(M):
    M=[row[:] for row in M]; n=len(M); d=G(1)
    for k in range(n):
        p=next((r for r in range(k,n) if not M[r][k].iszero()),None)
        if p is None: return G(0)
        if p!=k: M[k],M[p]=M[p],M[k]; d=-d
        d=d*M[k][k]
        for r in range(k+1,n):
            f=M[r][k]/M[k][k]
            if not f.iszero():
                for cc in range(k,n): M[r][cc]=M[r][cc]-f*M[k][cc]
    return d
def kern(cs):
    n=len(cs); a=[G(1)/x.conj() for x in cs]; t=[-x/x.conj() for x in cs]; m=n//2
    dP,dQ=(m,m-1) if n%2==0 else (m,m)
    def pw(x,j):
        r=G(1)
        for _ in range(j): r=r*x
        return r
    rows=[[pw(t[k],j) for j in range(dP+1)]+[-a[k]*pw(t[k],j) for j in range(dQ+1)] for k in range(n)]
    N=n+1; v=[]
    for j in range(N):
        sub=[[rows[k][l] for l in range(N) if l!=j] for k in range(n)]
        dd=det(sub); v.append(dd if j%2==0 else -dd)
    return v[:dP+1], v[dP+1:]
def second(c,d): return (c.conj()*d-c*d.conj())/(c.conj()-d.conj())
def miquel(cs): P,Q=kern(cs); return -Q[1]/P[2]
def tri(a,b,c): return det([[G(1),a,a.conj()],[G(1),b,b.conj()],[G(1),c,c.conj()]])
def cyc(a,b,c): return det([[z,z*z.conj(),z.conj()] for z in (a,b,c)])
def genpos(c):
    n=len(c)
    for i in range(n):
        for j in range(i+1,n):
            if (c[i].conj()*c[j]-c[i]*c[j].conj()).iszero(): return False
    for S in itertools.combinations(range(n),3):
        x=[c[i] for i in S]
        if tri(*x).iszero() or cyc(*x).iszero(): return False
    return True
