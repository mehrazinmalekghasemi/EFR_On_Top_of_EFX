import json
import unittest
from itertools import permutations
from pathlib import Path
from efr.source_strategies import surplus_lift,quad_replacement
from efr.dangerous_moves import full_star_progress
from tests.test_dangerous_moves import literal_check
from efr.oracle import is_efx

ROOT=Path(__file__).resolve().parents[1]

class SourceStrategiesTests(unittest.TestCase):
    def test_surplus_lift_resolves_top_up_failure(self):
        c=json.loads((ROOT/'experiment-results/dangerous-items/singleton-top-up-witnesses.json').read_text())[-1]
        V,A=c['values'],c['initial'];p=c['priority']
        move=surplus_lift(V,A,9,2,0,3,5,p)['move']
        self.assertIsNotNone(move);literal_check(V,A,move['allocation'],p)
        B=[76,2,1,944]
        self.assertEqual(sum(x.bit_count() for x in B),10);literal_check(V,A,B)
        for perm in permutations(range(4)):
            W=[None]*4;C=[None]*4
            for j in range(4):W[perm[j]]=V[j];C[perm[j]]=A[j]
            order=[perm[j] for j in p]
            result=surplus_lift(W,C,9,perm[2],perm[0],perm[3],5,order)
            literal_check(W,C,result['move']['allocation'],order)

    def test_non_envying_pair_owner_in_every_saved_kernel_branch(self):
        cases=json.loads((ROOT/'experiment-results/dangerous-items/sole-champion-witnesses.json').read_text())
        cases+=json.loads((ROOT/'experiment-results/dangerous-items/witnesses.json').read_text())[:5]
        for case in cases:
            V=[row[:] for row in case['values']];V[1][0]=0;A=case['initial']
            for perm in permutations(range(4)):
                W=[None]*4;C=[None]*4
                for j in range(4):W[perm[j]]=V[j];C[perm[j]]=A[j]
                B=full_star_progress(W,C,9,perm[1],perm[2],perm[3])['allocation']
                literal_check(W,C,B)

    def test_quad_criterion_and_minimal_certificate_patterns(self):
        A=[1,6,24,480]
        for name,v,z,own,certificate_size in [('star',[5,2,2,1],4,10,0),('triangle',[3,3,3,1],5,10,3),('disjoint',[3,3,3,3],7,12,2)]:
            V=[[own,0,0,0,0]+v+[z],[11,5,5,0,0,0,0,0,0,0],[0,0,0,5,5,0,0,0,0,0],[0,0,0,0,0,2,2,2,2,3]]
            result=quad_replacement(V,A,9,3)
            self.assertEqual(len(result['intersection_obstruction']),certificate_size)
            for x in (5,6,7,8):
                B=list(A);B[3]=(A[3]^(1<<x))|(1<<9)
                self.assertEqual(is_efx(V,B),x in result['common_items'])
            if result['move']:literal_check(V,A,result['move']['allocation'])

    def test_quad_common_item_still_needs_owner_gain(self):
        A=[1,6,24,480]
        V=[[10,0,0,0,0,5,2,2,1,4],[11,5,5,0,0,0,0,0,0,0],[0,0,0,5,5,0,0,0,0,0],[0,0,0,0,0,2,2,2,2,2]]
        result=quad_replacement(V,A,9,3)
        self.assertEqual(result['common_items'],[5]);self.assertIsNone(result['move'])
