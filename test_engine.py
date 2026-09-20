"""Run: python3 -m unittest -v test_engine. Deliberately independent small oracle."""
import itertools,json,tempfile,unittest
from pathlib import Path
from fractions import Fraction
import numpy as np
import z3
import oracle as o
import search
import verify

def brute_counts(V,missing):
    m=len(V[0]);goods=[g for g in range(m) if g!=missing]
    efx=0;ext=0
    for owners in itertools.product(range(4),repeat=len(goods)):
        A=[[] for _ in range(4)]
        for g,i in zip(goods,owners):A[i].append(g)
        ok=True
        for i in range(4):
            own=sum(V[i][g] for g in A[i])
            for j in range(4):
                if i==j:continue
                for h in A[j]:
                    if own<sum(V[i][g] for g in A[j] if g!=h):ok=False;break
                if not ok:break
            if not ok:break
        if not ok:continue
        efx+=1
        for k in range(4):
            B=[list(x) for x in A];B[k].append(missing)
            ok=True
            for i in range(4):
                own=sum(V[i][g] for g in B[i])
                for j in range(4):
                    if i==j or not B[j]:continue
                    # Original definition, average of actual removals.
                    total=sum(sum(V[i][g] for g in B[j] if g!=h) for h in B[j])
                    if len(B[j])*own<total:ok=False;break
                if not ok:break
            ext+=ok
    return efx,ext

def kernel_counts(V,g,jit=True):
    rows=o.integer_rows(V);s,m,z,fast=o.tables(rows)
    goods=[h for h in range(len(V[0])) if h!=g]
    lift=np.array([sum(1<<h for q,h in enumerate(goods) if mask>>q&1)
                   for mask in range(1<<len(goods))])
    parts=lift[o.partitions(len(goods))]
    mb,mc=o.matching_tables()
    f=o.scan_kernel if fast and jit else o.scan_kernel.py_func
    a,n,ec,sc,hist,vis,done=f(parts,s,m,z,np.array([row[g] for row in rows],dtype=np.int64 if fast else object),
                           1,mb,mc,o.PERMS,1,True)
    return int(ec),int(sc)

class Tests(unittest.TestCase):
    def test_partition_census(self):
        self.assertEqual(len(o.partitions(9)),11051)
        self.assertEqual(len(o.partitions(10)),43947)
        # Includes every LABELED allocation, including repeated empty slots.
        import math
        for m in (3,6,9):
            count=sum(24//math.factorial(sum(x==0 for x in p)) for p in o.partitions(m))
            self.assertEqual(count,4**m)
    def test_matching_every_graph(self):
        bits,counts=o.matching_tables()
        # Independent Hall-condition test for all 65,536 bipartite graphs.
        for graph in range(65536):
            hall=True
            for subset in range(1,16):
                union=0
                for i in range(4):
                    if subset>>i&1:union|=(graph>>(4*i))&15
                if union.bit_count()<subset.bit_count():hall=False;break
            self.assertEqual(bool(bits[graph]),hall)
    def test_exhaustive_small_instances(self):
        rng=np.random.default_rng(2)
        cases=[[[0]*6 for _ in range(4)],[[1]*6 for _ in range(4)]]
        cases += [rng.integers(0,5,size=(4,6)).tolist() for _ in range(12)]
        for V in cases:
            for g in (0,5):self.assertEqual(kernel_counts(V,g),brute_counts(V,g))
    def test_fixed_deletion_obstruction(self):
        V=[[1]*9+[2] for _ in range(4)]
        r=o.oracle(V,deleted=9,scan_all=True)
        self.assertEqual(r['status'],'ABSENT')
        self.assertEqual(r['profiles'][0]['efx_count'],30240)
        self.assertEqual(o.oracle(V)['status'],'FOUND')
    def test_balanced_predecessor_is_not_universal(self):
        V=[[100]+[1]*9 for _ in range(4)]
        r=o.oracle(V,predecessor_pattern=(2,2,2,3))
        self.assertEqual(r['status'],'ABSENT')
        self.assertEqual(o.oracle(V)['status'],'FOUND')
    def test_all_zero_counts(self):
        r=o.oracle([[0]*10 for _ in range(4)],deleted=9,scan_all=True)
        self.assertEqual(r['profiles'][0]['efx_count'],4**9)
        self.assertEqual(r['profiles'][0]['extension_count'],4**10)
    def test_big_integer_fallback(self):
        V=[[1,2,0,10**30+i,3,2] for i in range(4)]
        self.assertEqual(kernel_counts(V,5),brute_counts(V,5))
    def test_scaling_and_rational(self):
        V=[[1]*9+[2] for _ in range(4)]
        W=[[str(Fraction(x,i+7)) for x in row] for i,row in enumerate(V)]
        self.assertEqual(o.oracle(V,deleted=9)['status'],o.oracle(W,deleted=9)['status'])
    def test_search_formula_equivalence(self):
        # Capacity formula vs independent final EFR formula on an EFX predecessor.
        V=[[1]*10 for _ in range(4)]; w=o.oracle(V,limit=1)['witnesses'][0]
        node={'prefixes':[[0],[0],[0]],'witnesses':[w]}
        v=search.variables(10)
        p=search.witness_constraints(v,w,'extension')
        # Independent full formula uses separate variable names; substitute.
        full=verify.make_instance(node,'extension',10)[-1]
        full=z3.substitute(full,*[(z3.Real(f'x{i}_{g}'),v[i][g]) for i in range(4) for g in range(10)])
        s=z3.Solver();s.add(*[x>=0 for row in v for x in row])
        s.add(z3.Xor(z3.Not(z3.And(p)),full))
        self.assertEqual(s.check(),z3.unsat)
    def test_no_false_coverage_and_missing_child(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'nodes').mkdir()
            conf={'schema':1,'goal':'efx9','goods':9,'zero_tolerant_efx':True,'normalized_row_sum':1,'agent0_sorted':True}
            (root/'config.json').write_text(json.dumps(conf))
            n=next(search.root_nodes(9));n['status']='COVERED'
            (root/'nodes'/f"{n['id']}.json").write_text(json.dumps(n))
            r=verify.verify(tmp,1)
            self.assertEqual(r['verdict'],'INCOMPLETE_NO_THEOREM')
            self.assertEqual(r['checks'][0]['verdict'],'sat')
            n['status']='SPLIT';n['split_agent']=1;n['children']=['bogus']
            (root/'nodes'/f"{n['id']}.json").write_text(json.dumps(n))
            with self.assertRaises(AssertionError):verify.verify(tmp,1)
    def test_independent_verifier_positive_control(self):
        # For one good, every complete allocation is EFR. Test the independent
        # formula builder/solver's UNSAT path; production census still enforces m=9/10.
        import time
        node={'id':'unit','prefixes':[[0],[0],[0]],'witnesses':[{'allocation':[1,0,0,0]}]}
        result=verify.solve_leaf((node,'efr',1,2,time.time()+10))
        self.assertEqual(result['verdict'],'unsat')
        bad={'id':'bad','prefixes':[[0],[0],[0]],'witnesses':[{'allocation':[1,1,0,0]}]}
        with self.assertRaises(AssertionError):verify.make_instance(bad,'efr',1)
    def test_deadline_is_unknown(self):
        self.assertEqual(o.oracle([[1]*10]*4,deadline=0)['status'],'UNKNOWN')

if __name__=='__main__':unittest.main()
