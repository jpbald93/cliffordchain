import sys, itertools
sys.path.insert(0,'.')
from gq import *
from fractions import Fraction as Fr
import sympy as sp
c=[G(3,-6),G(6,-3),G(1,2),G(-2,-1),G(0,-4),G(4,0)]
def lit(z):
    def f(x):
        x=Fr(x)
        s = str(x.numerator) if x.denominator==1 else f"{x.numerator}/{x.denominator}"
        return s
    return f"⟨{f(z.r)}, {f(z.i)}⟩"
def name(k): return f"cx{k}"
out=[]
P=out.append
P("import Clifford.General\n\n/-!\n# A counterexample to `CliffordChain 6`\n\nSee `GENERAL_REPORT.md`. For the six centres `cx` below (exact Gaussian integers) `GenPosN cx`\nholds, every level-4 point is forced to be the classical Miquel point, the six level-5 objects\nare forced to be lines (five distinct collinear Miquel points each), and three of these lines\nare not concurrent, so no level-6 point exists.\n-/\n\nnamespace Clifford\n\nopen Complex ComplexConjugate\n\nnamespace Counter6\n")
P("/-- Six centres in general position (`GenPosN`) without a level-6 Clifford object. -/")
P("def cx : Fin 6 → ℂ := !["+", ".join(lit(z) for z in c)+"]\n")
P("theorem cx_transversal (i j : Fin 6) (h : i ≠ j) : Transversal (cx i) (cx j) := by\n  fin_cases i <;> fin_cases j <;>\n    first\n    | exact absurd rfl h\n    | (intro h; have := congrArg Complex.im h; simp [cx] at this; norm_num at this)\n")
P("theorem cx_genTriple (i j k : Fin 6) (h1 : i < j) (h2 : j < k) :\n    GenTriple (cx i) (cx j) (cx k) := by\n  fin_cases i <;> fin_cases j <;> fin_cases k <;> simp at h1 h2 <;>\n    refine ⟨fun h => ?_, fun h => ?_⟩ <;> have := congrArg Complex.im h <;>\n    simp [cx, triP, cycP, det3] at this <;> norm_num at this\n")
P("theorem cx_genPosN : GenPosN cx := ⟨cx_transversal, cx_genTriple⟩\n")
# seconds
sec={}
for a,b in itertools.combinations(range(6),2):
    s=second(c[a],c[b]); sec[(a,b)]=s
    P(f"theorem s{a}{b} : second {lit(c[a])} {lit(c[b])} = {lit(s)} := by\n  apply second_eq\n  · intro h; have h1 := congrArg Complex.re h; norm_num at h1\n  · apply Complex.ext <;> norm_num\n")
# level-4 lemmas
subsets=[]
for i in [4,5,0]:
    sub=[k for k in range(6) if k!=i]
    for j in range(3):
        fam=[sub[k] for k in range(5) if k!=j]
        subsets.append(tuple(fam))
x,y=sp.symbols('x y')
def cDpoly(a,b,cc,q):
    M=sp.Matrix([[sp.Rational(w.r)**2+sp.Rational(w.i)**2, sp.Rational(w.r), sp.Rational(w.i),1] if not isinstance(w,tuple) else [w[0]**2+w[1]**2,w[0],w[1],1] for w in (a,b,cc,q)])
    return sp.expand(M.det())
def R(f): return sp.Rational(f.numerator,f.denominator)
def GR(z): return (R(z.r),R(z.i))
def toG(t): return t
mq={}
for fam in sorted(set(subsets)):
    xa,ya,za,wa=fam
    m=miquel([c[k] for k in fam]); mq[fam]=m
    def S(a,b): return sec[(min(a,b),max(a,b))]
    triples=[(S(za,wa),S(ya,wa),S(ya,za)),(S(za,wa),S(xa,wa),S(xa,za)),(S(ya,wa),S(xa,wa),S(xa,ya))]
    eqs=[sp.Matrix([[R(w.r)**2+R(w.i)**2,R(w.r),R(w.i),1] for w in t]+[[x**2+y**2,x,y,1]]).det().expand() for t in triples]
    # find coefficients l1..l3 with sum l_i eq_i = x - mr (resp y - mi)
    l=sp.symbols('l1:4'); res=[]
    for target in [x-R(m.r), y-R(m.i)]:
        e=sp.expand(sum(li*ei for li,ei in zip(l,eqs))-target)
        sol=sp.solve(sp.Poly(e,x,y).coeffs(),l,dict=True)
        assert sol, fam
        res.append([sol[0].get(li,0) for li in l])
    name="q"+"".join(map(str,fam))
    vec="!["+", ".join(lit(c[k]) for k in fam)+"]"
    secs=[f"s{min(a,b)}{max(a,b)}" for a,b in [(za,wa),(ya,wa),(ya,za),(xa,wa),(xa,za),(xa,ya)]]
    lc=lambda r: " + ".join(f"({sp.sstr(v)}) * h{k+1}" for k,v in enumerate(r) if v!=0)
    P(f"theorem {name} {{q : ℂ}} (h : Chain 4 {vec} {{q}}) : q = {lit(m)} := by\n  obtain ⟨h1, h2, h3, -⟩ := chain4_cD h\n  simp only [{', '.join(sorted(set(secs)))}] at h1 h2 h3\n  simp only [cD, det4, det3] at h1 h2 h3\n  apply Complex.ext\n  · linear_combination {lc(res[0])}\n  · linear_combination {lc(res[1])}\n")
# main
P("theorem not_chain6 {X : Set ℂ} : ¬ Chain 6 cx X := by\n  intro h\n  obtain ⟨p, -, h⟩ := (h : ∃ p, X = {p} ∧ ∀ i : Fin 6, ∃ Y, Chain 5 (cx ∘ i.succAbove) Y ∧ p ∈ Y)")
lines=[]
for idx,i in enumerate([4,5,0]):
    sub=[k for k in range(6) if k!=i]
    vec="!["+", ".join(lit(c[k]) for k in sub)+"]"
    P(f"  have e{i} : cx ∘ Fin.succAbove {i} = {vec} := by funext k; fin_cases k <;> rfl")
    P(f"  obtain ⟨Y{i}, hY{i}, p{i}⟩ := h {i}\n  rw [e{i}] at hY{i}\n  obtain ⟨g{i}, a{i}, b{i}, c{i}⟩ := chain5_mem hY{i}")
    fams=subsets[3*idx:3*idx+3]
    qs=[mq[f] for f in fams]
    for t,(f,v) in enumerate(zip(fams,"abc")):
        P(f"  obtain ⟨r{i}{v}, hr{i}{v}, m{i}{v}⟩ := {v}{i}\n  rw [q{''.join(map(str,f))} hr{i}{v}] at m{i}{v}")
    P(f"  have l{i} := cD_eq_zero g{i} m{i}a m{i}b m{i}c p{i}")
    P(f"  simp only [cD, det4, det3] at l{i}")
    lines.append(sp.Matrix([[R(w.r)**2+R(w.i)**2,R(w.r),R(w.i),1] for w in qs]+[[x**2+y**2,x,y,1]]).det().expand())
l=sp.symbols('l1:4')
e=sp.expand(sum(li*ei for li,ei in zip(l,lines))-1)
sol=sp.solve(sp.Poly(e,x,y).coeffs(),l,dict=True); assert sol
r=[sol[0].get(li,0) for li in l]
P("  have : (1 : ℝ) = 0 := by\n    linear_combination "+" + ".join(f"({sp.sstr(v)}) * l{k}" for v,k in zip(r,[4,5,0]) if v!=0))
P("  norm_num at this\n")
P("/-- **`CliffordChain 6` is false**: the centres `cx` are in general position (`GenPosN`) but admit\nno level-6 Clifford object. -/\ntheorem not_cliffordChain_six : ¬ CliffordChain 6 := fun H =>\n  let ⟨_, hX⟩ := H cx cx_genPosN\n  not_chain6 hX\n")
P("end Counter6\n\nend Clifford")
open('Counter6.lean','w').write("\n".join(out)+"\n")
