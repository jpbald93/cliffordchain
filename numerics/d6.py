import mpmath as mp, itertools, random, sys
sys.path.insert(0,'.')
from chain import classical
mp.mp.dps=60
def kern(cs):
    n=len(cs); a=[1/mp.conj(x) for x in cs]; t=[-x/mp.conj(x) for x in cs]; m=n//2
    dP,dQ=(m,m-1) if n%2==0 else (m,m)
    rows=[[t[k]**j for j in range(dP+1)]+[-a[k]*t[k]**j for j in range(dQ+1)] for k in range(n)]
    N=n+1; v=[]
    for j in range(N):
        sub=mp.matrix([[rows[k][l] for l in range(N) if l!=j] for k in range(n)])
        v.append((-1)**j*mp.det(sub))
    return v[:dP+1], v[dP+1:]
def nrm(P,Q): return mp.sqrt(sum(abs(u)**2 for u in P+Q))
def tri(a,b,cc): return mp.det(mp.matrix([[1,a,mp.conj(a)],[1,b,mp.conj(b)],[1,cc,mp.conj(cc)]]))
def cyc(a,b,cc): return mp.det(mp.matrix([[z,z*mp.conj(z),mp.conj(z)] for z in (a,b,cc)]))
def genpos_min(c):
    n=len(c)
    return min([abs(mp.conj(c[i])*c[j]-c[i]*mp.conj(c[j])) for i in range(n) for j in range(i+1,n)]+[abs(tri(*[c[i] for i in S])) for S in itertools.combinations(range(n),3)]+[abs(cyc(*[c[i] for i in S])) for S in itertools.combinations(range(n),3)])
def solve(c, idx, F):
    # Newton on c[idx] (2 real vars) for complex F(c)=0
    x=c[idx]
    def f(x):
        cc=list(c); cc[idx]=x; return F(cc)
    for it in range(200):
        fx=f(x)
        if abs(fx)<mp.mpf(10)**-50: return x,True
        h=mp.mpf(10)**-25
        fr=(f(x+h)-fx)/h; fi=(f(x+1j*h)-fx)/h
        J=mp.matrix([[mp.re(fr),mp.re(fi)],[mp.im(fr),mp.im(fi)]])
        try: d=mp.lu_solve(J,mp.matrix([-mp.re(fx),-mp.im(fx)]))
        except ZeroDivisionError: return x,False
        step=d[0]+1j*d[1]
        if abs(step)>0.3: step*=0.3/abs(step)
        x=x+step
    return x,False
if __name__=='__main__':
    n=6; m=3
    for seed in range(int(sys.argv[1]),int(sys.argv[1])+30):
        random.seed(seed)
        c=[mp.mpc(random.uniform(-2,2),random.uniform(-2,2)) for _ in range(n)]
        F=lambda cc: (lambda PQ: PQ[0][m]/nrm(*PQ))(kern(cc))
        x,ok=solve(c,n-1,F)
        if ok:
            c[n-1]=x; print('seed',seed,'found; genpos min',mp.nstr(genpos_min(c),5)); print([mp.nstr(z,25) for z in c]); break
        else: print('seed',seed,'fail')
