import unittest
import json
from pathlib import Path
from itertools import permutations
from oracle import is_efx,verify_witness,tables
from capacity import diagnostics
from restoration_moves import lift_preserving_start,source_analysis,improving_transfers

V=[[4,4,8,1,8,1,1,5,1,4],
   [3,1,9,1,3,8,5,1,1,7],
   [1,1,1,1,5,1,2,1,1,5],
   [19,1,17,1,19,1,7,7,7,14]]
A=[3,12,48,448]

class RestorationMovesTests(unittest.TestCase):
    def assert_obstruction(self,V):
        own=tuple(sum(V[i][h] for h in range(10) if A[i]>>h&1) for i in range(4))
        analysis=source_analysis(V,A,9)
        self.assertEqual(analysis['sources'],[0,3]);self.assertFalse(analysis['moves'])
        for p in permutations(A):
            if is_efx(V,p):
                utilities=tuple(sum(V[i][h] for h in range(10) if p[i]>>h&1) for i in range(4))
                self.assertLessEqual(utilities,own)
                self.assertFalse(any(t['feasible'] for t in diagnostics(V,p,9)))

    def test_obstruction_and_one_transfer_escape(self):
        self.assert_obstruction(V)
        moves=improving_transfers(V,A,9)
        self.assertIn([11,4,48,448],[x['predecessor'] for x in moves])
        w={'predecessor':[11,4,48,448],'deleted':9,'recipient':1,'allocation':[11,516,48,448]}
        self.assertTrue(verify_witness(V,w))

    def test_nondegenerate_lift_retains_obstruction(self):
        q=lift_preserving_start(V,A,9);W=q['values']
        sums,_,_,_=tables(W)
        for row in sums:self.assertEqual(len(set(map(int,row))),1024)
        self.assertTrue(is_efx(W,A));self.assert_obstruction(W)

    def test_no_common_least_obstructions_and_escapes(self):
        for profile in ['1125','1224','2223']:
            path=Path(__file__).resolve().parent/'experiment-results/restoration'/('obstruction-'+profile+'.json')
            case=json.loads(path.read_text());W=case['integer_values'];start=case['initial']
            self.assertFalse(any(all(row[g]==min(row) for row in W) for g in range(10)))
            self.assertFalse(source_analysis(W,start,9)['moves'])
            own=tuple(sum(W[i][h] for h in range(10) if start[i]>>h&1) for i in range(4))
            for B in permutations(start):
                if is_efx(W,B):
                    self.assertFalse(any(t['feasible'] for t in diagnostics(W,B,9)))
                    utility=tuple(sum(W[i][h] for h in range(10) if B[i]>>h&1) for i in range(4))
                    self.assertLessEqual(utility,own)
            self.assertTrue(verify_witness(W,case['nearest_escape']['witness']))
        case=json.loads((Path(__file__).resolve().parent/'experiment-results/restoration/obstruction-1125.json').read_text())
        W=lift_preserving_start(case['integer_values'],case['initial'],9)['values']
        self.assertFalse(source_analysis(W,case['initial'],9)['moves'])
        self.assertTrue(verify_witness(W,case['nearest_escape']['witness']))

    def test_large_source_can_temporarily_release_six_goods(self):
        W=[[10]*4+[1]*6 for _ in range(4)]
        q=source_analysis(W,[1,2,4,1008],3)
        self.assertEqual(q['sources'],[3])
        self.assertTrue(any(m['allocation']==[1,2,4,8] and m['unallocated'].bit_count()==6 for m in q['moves']))

if __name__=='__main__':unittest.main()
