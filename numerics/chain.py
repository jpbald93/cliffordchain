import mpmath as mp, itertools, random, sys
mp.mp.dps=60
def second(c,d): return (mp.conj(c)*d-c*mp.conj(d))/(mp.conj(c)-mp.conj(d))
def circ3(p,q,r):
    # circle through 3 points: returns (o, r) or ('line', p, v)
    a=q-p; b=r-p
    den=2*mp.im(mp.conj(a)*b)
    if abs(den)<mp.mpf(10)**-40: return None
    o=p+ 1j*(abs(a)**2*b-abs(b)**2*a)/den* -1
    # verify
    return (o, abs(p-o))
def fixo(p,q,r):
    # robust circumcenter
    A=mp.matrix([[2*mp.re(q-p),2*mp.im(q-p)],[2*mp.re(r-p),2*mp.im(r-p)]])
    B=mp.matrix([abs(q)**2-abs(p)**2,abs(r)**2-abs(p)**2])
    s=mp.lu_solve(A,B); o=mp.mpc(s[0],s[1]); return (o,abs(p-o))
def interC(C1,C2):
    (o1,r1),(o2,r2)=C1,C2
    d=abs(o2-o1); a=(r1**2-r2**2+d**2)/(2*d); h=mp.sqrt(max(r1**2-a**2,0))
    e=(o2-o1)/d; m=o1+a*e
    return [m+1j*h*e, m-1j*h*e]
def classical(c):
    # returns dict frozenset(S)-> object; points as mpc, circles as (o,r)
    n=len(c); obj={}
    for S in itertools.combinations(range(n),2): obj[S]=second(c[S[0]],c[S[1]])
    for k in range(3,n+1):
        for S in itertools.combinations(range(n),k):
            subs=[tuple(x for x in S if x!=i) for i in S]
            if k%2==1:
                pts=[obj[s] for s in subs]
                C=fixo(*pts[:3]); res=max(abs(abs(p-C[0])-C[1]) for p in pts)
                obj[S]=C; 
                if res>1e-25: print('odd fail',S,res)
            else:
                cs=[obj[s] for s in subs]
                cand=interC(cs[0],cs[1])
                best=min(cand,key=lambda p:max(abs(abs(p-C[0])-C[1]) for C in cs))
                res=max(abs(abs(best-C[0])-C[1]) for C in cs)
                obj[S]=best
                if res>1e-25: print('even fail',S,res)
    return obj
def formula(cs):
    # rational interpolation in line picture: a=1/conj c, t=-c/conj c
    n=len(cs); a=[1/mp.conj(x) for x in cs]; t=[-x/mp.conj(x) for x in cs]
    m=n//2
    if n%2==0: dP,dQ=m,m-1
    else: dP,dQ=m,m
    rows=[[t[k]**j for j in range(dP+1)]+[-a[k]*t[k]**j for j in range(dQ+1)] for k in range(n)]
    M=mp.matrix(rows) # n x (n+1)
    # null vector via minors
    N=n+1; v=[]
    for j in range(N):
        sub=mp.matrix([[rows[k][l] for l in range(N) if l!=j] for k in range(n)])
        v.append((-1)**j*mp.det(sub))
    P=v[:dP+1]; Q=v[dP+1:]
    if n%2==0: return ('pt', -Q[m-1]/P[m])
    else: return ('circ', mp.conj(Q[0]/P[0]), abs(Q[m]/P[0]))
if __name__=='__main__':
    random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 1)
    for n in range(3,9):
        c=[mp.mpc(random.uniform(-2,2),random.uniform(-2,2)) for _ in range(n)]
        obj=classical(c)
        full=tuple(range(n)); o=obj[full]; f=formula(c)
        if n%2==0: print(n,'pt',mp.nstr(abs(o-f[1]),5))
        else: print(n,'circ',mp.nstr(abs(o[0]-f[1]),5),mp.nstr(abs(o[1]-f[2]),5))
