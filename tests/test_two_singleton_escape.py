import json
import unittest
from pathlib import Path
from itertools import permutations
from efr.two_singleton_escape import pair_source_escape,retain_dominant_rotation
from efr.source_strategies import surplus_lift
from efr.capacity import diagnostics
from efr.oracle import is_efr
from tests.test_dangerous_moves import literal_check

ROOT=Path(__file__).resolve().parents[1]

class TwoSingletonEscapeTests(unittest.TestCase):
    def test_pair_path_insertion_and_self_improvement(self):
        A=[1,2,12,496]
        V=[[10,11,0,0,0,0,0,0,0,0],[0,10,4,4,0,0,0,0,0,8],[3,0,1,1,0,0,0,0,0,0],[0,0,0,0,6,1,1,1,1,4]]
        result=pair_source_escape(V,A,9,2,3)
        self.assertEqual(result['path'],[2,0,1]);literal_check(V,A,result['allocation'])
        for p in permutations(range(4)):
            W=[None]*4;B=[None]*4
            for j in range(4):W[p[j]]=V[j];B[p[j]]=A[j]
            result=pair_source_escape(W,B,9,p[2],p[3]);literal_check(W,B,result['allocation'])
        W=[r[:] for r in V];W[1][9]=0
        result=pair_source_escape(W,A,9,2,3)
        self.assertEqual(result['kind'],'pair_source_efr_insertion');self.assertTrue(is_efr(W,result['allocation']))
        W[2][9]=2
        result=pair_source_escape(W,A,9,2,3)
        self.assertEqual(result['kind'],'pair_source_self_improvement');literal_check(W,A,result['allocation'])

    def test_new_frame_and_simple_replacement_escape_joint_failure(self):
        A=[1,2,28,480]
        for x,p,B in [(2,[0,1,2,3],[513,92,2,416]),(6,[3,0,1,2],[513,452,2,56])]:
            V=[[10,0,0,0,0,4,0,0,0,7],[0,4,1,1,1,0,1,1,1,3],[5,5,1,1,1,0,0,0,0,2],[0,0,x,x,x,18,4,4,4,3]]
            self.assertFalse(any(d['feasible'] for d in diagnostics(V,A,9)))
            self.assertIsNone(surplus_lift(V,A,9,2,0,3,5,p)['move'])
            result=retain_dominant_rotation(V,A,9,2,0,3,5,p)
            self.assertIsNotNone(result);literal_check(V,A,result['allocation'],p)
            literal_check(V,A,B,p);self.assertEqual(sum(b.bit_count() for b in B),10)
            C=list(A);C[2]=536;literal_check(V,A,C)

    def test_reachability_scope_counts(self):
        counts={}
        for profile in ([1,1,2,5],[1,1,3,4]):
            selected=[]
            for c in json.loads((ROOT/'research/case-status.json').read_text())['cases']:
                if c['status']!='OPEN' or c['profile']!=profile:continue
                reach={2}
                while True:
                    new=reach|{b for a,b in c['edges'] if a in reach}
                    if new==reach:break
                    reach=new
                if {0,1}<=reach:selected.append(c['id'])
            counts[tuple(profile)]=len(selected)
        self.assertEqual(counts,{(1,1,2,5):6,(1,1,3,4):11})
