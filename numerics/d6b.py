import mpmath as mp, itertools, random, sys
sys.path.insert(0,'.')
from d6 import kern, nrm, genpos_min
mp.mp.dps=40
n=int(sys.argv[2]); m=n//2
def F(cc):
    P,Q=kern(cc); return P[m]/nrm(P,Q)
def vec(c): return [x for z in c for x in (mp.re(z),mp.im(z))]
def unvec(v): return [mp.mpc(v[2*i],v[2*i+1]) for i in range(len(v)//2)]
for seed in range(int(sys.argv[1]),int(sys.argv[1])+10):
    random.seed(seed)
    c=[mp.mpc(random.uniform(-2,2),random.uniform(-2,2)) for _ in range(n)]
    v=vec(c); ok=False
    for it in range(60):
        fx=F(unvec(v))
        if abs(fx)<mp.mpf(10)**-35: ok=True; break
        h=mp.mpf(10)**-18; J=[]
        for k in range(len(v)):
            w=list(v); w[k]+=h; d=(F(unvec(w))-fx)/h; J.append(d)
        # least-norm Gauss-Newton: solve 2x2 (J J^T) y = -f
        A=mp.matrix([[sum(mp.re(a)*mp.re(a) for a in J), sum(mp.re(a)*mp.im(a) for a in J)],[sum(mp.re(a)*mp.im(a) for a in J), sum(mp.im(a)*mp.im(a) for a in J)]])
        y=mp.lu_solve(A,mp.matrix([-mp.re(fx),-mp.im(fx)]))
        step=[mp.re(a)*y[0]+mp.im(a)*y[1] for a in J]
        s=mp.sqrt(sum(x*x for x in step))
        if s>0.2: step=[x*0.2/s for x in step]
        v=[a+b for a,b in zip(v,step)]
    c=unvec(v)
    print('seed',seed,'ok' if ok else 'no','|F|',mp.nstr(abs(F(c)),3),'genpos',mp.nstr(genpos_min(c),5))
    if ok: print([mp.nstr(z,30) for z in c])
