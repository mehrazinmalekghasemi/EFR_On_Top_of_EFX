import json,unittest
from pathlib import Path
from itertools import permutations
from fractions import Fraction
from efr.dangerous_moves import both_champions_progress,residual_singleton_relay
from efr.compensation import compensated_relay
from efr.restoration_moves import lift_preserving_start,source_analysis
from efr.capacity import diagnostics

ROOT=Path(__file__).resolve().parents[1]


def literal_check(V,A,B,priority=None):
    """Independent set/sum check; does not use the allocation oracle."""
    bundles=[{h for h in range(10) if b>>h&1} for b in B]
    assert sum(map(len,bundles))==len(set.union(*bundles))
    value=lambda i,S:sum(Fraction(str(V[i][h])) for h in S)
    old=[value(i,{h for h in range(10) if A[i]>>h&1}) for i in range(4)]
    new=[value(i,bundles[i]) for i in range(4)]
    for i in range(4):
        for j in range(4):
            if i!=j:
                for h in bundles[j]:assert new[i]>=value(i,bundles[j]-{h})
    if priority is None:assert all(x>=y for x,y in zip(new,old)) and new!=old
    else:assert tuple(new[i] for i in priority)>tuple(old[i] for i in priority)


class DangerousMovesTests(unittest.TestCase):
    def setUp(self):
        self.cases=json.loads((ROOT/'experiment-results/dangerous-items/witnesses.json').read_text())

    def test_all_constructive_branches_and_agent_relabelings(self):
        kinds=set()
        for case in self.cases[:5]:
            V,A=case['values'],case['initial']
            result=both_champions_progress(V,A,9,1,2,3)
            self.assertEqual(result,case['certificate']);kinds.add(result['kind'])
            literal_check(V,A,result['allocation'])
            for p in permutations(range(4)):
                W=[None]*4;C=[None]*4
                for i in range(4):W[p[i]]=V[i];C[p[i]]=A[i]
                moved=both_champions_progress(W,C,9,p[1],p[2],p[3])
                literal_check(W,C,moved['allocation'])
        self.assertEqual(kinds,{'triple_replacement','dangerous_exchange','three_agent_mixed_repair','four_agent_disjoint_pairs'})

    def test_all_C1_proposals_fail_but_complete_EFX_exists(self):
        case=self.cases[5];V,A=case['values'],case['initial']
        checked=0
        for s,i,t in permutations(range(4),3):
            mask=A[t]
            while True:
                checked+=1
                self.assertIsNone(compensated_relay(V,A,9,s,i,t,mask|(1<<9)))
                if not mask:break
                mask=(mask-1)&A[t]
        self.assertEqual(checked,132)
        self.assertEqual(source_analysis(V,A,9)['graph'],[[1],[],[0],[0]])
        self.assertEqual(source_analysis(V,A,9)['moves'],[])
        self.assertFalse(any(row['feasible'] for row in diagnostics(V,A,9)))
        self.assertEqual(sum(b.bit_count() for b in case['full_efx']),10)
        literal_check(V,A,case['full_efx'])

    def test_residual_relay_escapes_existing_two_agent_trap(self):
        data=json.loads((ROOT/'experiment-results/two-source/verified-obstruction.json').read_text())
        A=data['initial'];V=data['values']
        for rows in (V,lift_preserving_start(V,A,9)['values']):
            result=residual_singleton_relay(rows,A,9,2,0,3,5)
            self.assertIsNotNone(result)
            self.assertEqual(result['allocation'],[544,2,1,448])
            literal_check(rows,A,result['allocation'],(0,1,2,3))
            self.assertIsNone(residual_singleton_relay(rows,A,9,2,0,3,5,(3,2,1,0)))

    def test_all_C1_thresholds_fail_but_residual_succeeds(self):
        case=self.cases[6];V,A=case['values'],case['initial']
        checked=0
        for s,i,t in permutations(range(4),3):
            mask=A[t]
            while True:
                checked+=1
                self.assertIsNone(compensated_relay(V,A,9,s,i,t,mask|(1<<9)))
                if not mask:break
                mask=(mask-1)&A[t]
        self.assertEqual(checked,168)
        move=residual_singleton_relay(V,A,9,2,0,3,5)
        self.assertEqual(move,case['certificate'])
        literal_check(V,A,move['allocation'],(0,1,2,3))
