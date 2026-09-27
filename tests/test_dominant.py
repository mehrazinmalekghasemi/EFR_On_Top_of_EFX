import json
import unittest
from fractions import Fraction
from itertools import permutations
from pathlib import Path
from efr.dominant import dominant_relay
from efr.capacity import diagnostics
from tests.test_dangerous_moves import literal_check

ROOT = Path(__file__).resolve().parents[1]

class DominantTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((ROOT/'experiment-results/dangerous-items/dominant-item-witnesses.json').read_text())

    def test_certificates_and_all_priority_preserving_relabelings(self):
        for case in self.cases:
            V, A, order = case['values'], case['initial'], case['priority']
            result = dominant_relay(V,A,9,2,0,3,5,order)
            self.assertEqual(result,case['result'])
            for p in permutations(range(4)):
                W=[None]*4; B=[None]*4
                for j in range(4):W[p[j]]=V[j];B[p[j]]=A[j]
                pi=[p[j] for j in order]
                move=dominant_relay(W,B,9,p[2],p[0],p[3],5,pi)['move']
                self.assertEqual(move is None,result['move'] is None)
                if move:literal_check(W,B,move['allocation'],pi)

    def test_budget_is_insufficient_even_with_all_compensation_subsets(self):
        for case in self.cases[:2]:
            V,A=case['values'],case['initial'];H=[2,3,4,6,7,8]
            self.assertFalse(any(x['feasible'] for x in diagnostics(V,A,9)))
            graph=[[j for j in range(4) if sum(V[i][x] for x in range(10) if A[j]>>x&1)>sum(V[i][x] for x in range(10) if A[i]>>x&1)] for i in range(4)]
            self.assertEqual(graph,[[],[],[0,1],[]])
            valid=0
            for mask in range(64):
                C=sum(1<<H[k] for k in range(6) if mask>>k&1)
                B=[544,2,1,C]
                try:literal_check(V,A,B,case['priority'])
                except AssertionError:pass
                else:valid+=1
            self.assertEqual(valid,0)
            escape=case['complete_efx_escape']
            self.assertEqual(sum(b.bit_count() for b in escape),10)
            literal_check(V,A,escape)

    def test_priority_boundary_and_exact_rationals(self):
        late,early,deficit=self.cases[2:5]
        self.assertEqual(late['result']['move']['new_utilities'][-1],'21')
        self.assertEqual(early['result']['move']['new_utilities'][-1],'30')
        self.assertIsNone(deficit['result']['move'])
        self.assertTrue(all(b['agent']==0 for b in deficit['result']['obstructions'][0]['blockers']))
        V=[[str(Fraction(x,7)) for x in row] for row in late['values']]
        move=dominant_relay(V,late['initial'],9,2,0,3,5,late['priority'])['move']
        literal_check(V,late['initial'],move['allocation'],late['priority'])

    def test_direct_cover_and_invalid_assumptions(self):
        case=self.cases[-1]
        self.assertEqual(case['result']['move']['kind'],'dominant_minimal_cover')
        with self.assertRaises(ValueError):dominant_relay(case['values'],case['initial'],9,2,0,3,6)
        with self.assertRaises(ValueError):dominant_relay(case['values'],case['initial'],9,2,0,3,5,(0,0,2,3))
