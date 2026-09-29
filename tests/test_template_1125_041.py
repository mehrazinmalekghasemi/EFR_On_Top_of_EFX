import json,unittest
from pathlib import Path
from itertools import combinations
from fractions import Fraction
from efr.capacity import validate,diagnostics
from efr.oracle import is_efx
from efr.template_moves import weak_pair_path,exchange_pool_and_release
from tests.test_dangerous_moves import literal_check

ROOT=Path(__file__).resolve().parents[1]

class TemplateProbeTests(unittest.TestCase):
    def test_all_saved_points_and_claimed_menu_failures(self):
        cases=json.loads((ROOT/'experiment-results/template-1125-041/witnesses.json').read_text())
        for c in cases:
            A=c['initial'];V=validate(c['values'],A,9)
            val=lambda i,b:sum(V[i][g] for g in range(10) if b>>g&1)
            graph={(i,j) for i in range(4) for j in range(4) if i!=j and val(i,A[j])>100}
            self.assertEqual(graph,{(0,1),(2,0)})
            self.assertFalse(any(t['feasible'] for t in diagnostics(V,A,9)))
            for j in range(4):self.assertEqual(val(j,A[j]),100);self.assertLessEqual(V[j][9],100)
            for j in (2,3):
                for h in range(9):
                    if A[j]>>h&1:self.assertLessEqual(V[j][9]+V[j][h],100)
            for h in range(4,9):
                B=list(A);B[3]=(A[3]^(1<<h))|512;self.assertFalse(is_efx(V,B))
            for h in (2,3):
                for bits in range(32):
                    Y=sum(1<<(4+k) for k in range(5) if bits>>k&1)
                    if V[3][9]+V[3][h]>100 and val(3,Y)<=100-V[3][9]:self.assertLess(val(2,Y),V[2][h])
                    if c['stage']>=4:
                        B=list(A);B[2]=(A[2]^(1<<h))|Y;B[3]=(A[3]^Y)|(1<<h)
                        if val(2,B[2])>=100 and val(3,B[3])>=100 and (val(2,B[2])>100 or val(3,B[3])>100):self.assertFalse(is_efx(V,B))
            if c['stage']>=2:
                for bits in range(32):
                    C=512|sum(1<<(4+k) for k in range(5) if bits>>k&1)
                    if val(3,C)>100:
                        B=list(A);B[3]=C;self.assertFalse(is_efx(V,B))
            if c['stage']>=3:
                self.assertTrue(all(V[j][9]+V[j][h]<100 for j in (0,1) for h in (2,3)))
            literal_check(V,A,c['escape'])

    def test_weak_path_and_combined_exchange_certificates(self):
        cases=json.loads((ROOT/'experiment-results/template-1125-041/witnesses.json').read_text())
        c=cases[1];r=weak_pair_path(c['values'],c['initial'],9,[2,0],3)
        self.assertIsNotNone(r);literal_check(c['values'],c['initial'],r['allocation'])
        c=cases[3];r=exchange_pool_and_release(c['values'],c['initial'],9,2,3,2,1<<6,1<<7)
        self.assertEqual(r['allocation'],c['escape']);literal_check(c['values'],c['initial'],r['allocation'])
