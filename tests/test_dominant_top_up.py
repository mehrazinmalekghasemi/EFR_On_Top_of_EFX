import json
import unittest
from itertools import permutations
from pathlib import Path
from efr.dominant import dominant_relay, augment_dominant_blockers
from efr.capacity import diagnostics, validate
from tests.test_dangerous_moves import literal_check

ROOT = Path(__file__).resolve().parents[1]

class DominantTopUpTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((ROOT/'experiment-results/dangerous-items/singleton-top-up-witnesses.json').read_text())

    def test_repairs_extend_previous_move_class(self):
        for case in self.cases:
            V,A,p=case['values'],case['initial'],case['priority']
            self.assertIsNone(dominant_relay(V,A,9,2,0,3,5,p)['move'])
            result=augment_dominant_blockers(V,A,9,2,0,3,5,p)
            self.assertEqual(result,case['result'])
            if result['move']:literal_check(V,A,result['move']['allocation'],p)
        for case in self.cases[:2]:
            self.assertFalse(any(x['feasible'] for x in diagnostics(case['values'],case['initial'],9)))
            self.assertLess(case['values'][2][1],sum(case['values'][2][2:5]))
            self.assertEqual(sum(b.bit_count() for b in case['result']['move']['allocation']),10)

    def test_all_simultaneous_relabelings_preserve_priority(self):
        for case in self.cases:
            for p in permutations(range(4)):
                W=[None]*4; A=[None]*4
                for j in range(4):W[p[j]]=case['values'][j];A[p[j]]=case['initial'][j]
                order=[p[j] for j in case['priority']]
                move=augment_dominant_blockers(W,A,9,p[2],p[0],p[3],5,order)['move']
                self.assertEqual(move is None,case['result']['move'] is None)
                if move:literal_check(W,A,move['allocation'],order)

    def test_new_blocker_gain_can_precede_donor_without_resetting_priority(self):
        case=self.cases[1];order=[1,3,0,2]
        self.assertEqual(dominant_relay(case['values'],case['initial'],9,2,0,3,5,order)['branch'],'full_recovery')
        result=augment_dominant_blockers(case['values'],case['initial'],9,2,0,3,5,order)['move']
        self.assertEqual(result['top_up'],0)
        self.assertEqual(result['new_utilities'][3],'24')
        literal_check(case['values'],case['initial'],result['allocation'],order)

    def test_safety_failure_for_all_top_ups_and_mode_c_escape(self):
        case=self.cases[-1];V,A=case['values'],case['initial']
        leftover=[3,4,7,8];successes=0
        for bits in range(16):
            F=sum(1<<leftover[k] for k in range(4) if bits>>k&1)
            B=[68,2,1,544|F]
            try:literal_check(V,A,B,case['priority'])
            except AssertionError:pass
            else:successes+=1
        self.assertEqual(successes,0)
        attempt=case['result']['attempts'][0]
        self.assertEqual((attempt['deficit'],attempt['available_value']),('9','20'))
        self.assertEqual(len(attempt['minimal_top_ups']),5)
        w=case['mode_c_witness'];validate(V,w['predecessor'],w['deleted'])
        B=w['allocation'];self.assertEqual(sum(b.bit_count() for b in B),10)
        self.assertEqual(B[w['recipient']],w['predecessor'][w['recipient']]|(1<<w['deleted']))
        # Independent expected-deletion EFR check.
        val=lambda i,b:sum(V[i][g] for g in range(10) if b>>g&1)
        for i in range(4):
            for j in range(4):
                if i!=j:
                    n=B[j].bit_count()
                    self.assertGreaterEqual(n*val(i,B[i]),(n-1)*val(i,B[j]))
