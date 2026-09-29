import json,unittest
from pathlib import Path
from itertools import permutations
from efr.dangerous_moves import full_star_progress,repair_pair_blocker,residual_singleton_relay
from tests.test_dangerous_moves import literal_check

ROOT=Path(__file__).resolve().parents[1]

class FullStarTests(unittest.TestCase):
    def test_all_sole_branches_and_relabelings(self):
        cases=json.loads((ROOT/'experiment-results/dangerous-items/sole-champion-witnesses.json').read_text())
        kinds=set()
        for case in cases:
            V,A=case['values'],case['initial']
            move=full_star_progress(V,A,9,1,2,3)
            self.assertEqual(move,case['certificate']);kinds.add(move['kind'])
            literal_check(V,A,move['allocation'])
            # Reversing the role arguments must not change the physical problem.
            literal_check(V,A,full_star_progress(V,A,9,1,3,2)['allocation'])
            for p in permutations(range(4)):
                W=[None]*4;C=[None]*4
                for j in range(4):W[p[j]]=V[j];C[p[j]]=A[j]
                result=full_star_progress(W,C,9,p[1],p[2],p[3])
                literal_check(W,C,result['allocation'])
        self.assertEqual(len(kinds),7)

    def test_both_champion_branch_still_supported(self):
        cases=json.loads((ROOT/'experiment-results/dangerous-items/witnesses.json').read_text())
        for case in cases[:5]:
            V,A=case['values'],case['initial']
            literal_check(V,A,full_star_progress(V,A,9,1,2,3)['allocation'])

    def test_donor_before_champion_can_still_allow_progress(self):
        data=json.loads((ROOT/'experiment-results/two-source/verified-obstruction.json').read_text())
        order=(2,3,0,1)
        move=residual_singleton_relay(data['values'],data['initial'],9,2,0,3,5,order)
        self.assertIsNotNone(move)
        literal_check(data['values'],data['initial'],move['allocation'],order)

    def test_pair_blocker_repaired_without_omitted_good(self):
        A=[1,6,56,448]
        V=[[10,1,1,1,1,1,1,1,1,1],
           [1,2,2,1,2,1,1,1,1,1],
           [1,3,1,4,1,1,1,1,1,1],
           [1]*10]
        move=repair_pair_blocker(V,A,9,2,1,3,1,4)
        self.assertIsNotNone(move)
        literal_check(V,A,move['allocation'])
        self.assertFalse(any(b>>9&1 for b in move['allocation']))
