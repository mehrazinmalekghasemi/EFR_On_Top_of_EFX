import json,unittest
from itertools import permutations
from pathlib import Path
from efr.compensation import compensated_relay
from efr.priority import report,automorphisms,priority_representatives
from efr.oracle import is_efx

ROOT=Path(__file__).resolve().parents[1]

class CompensationTests(unittest.TestCase):
    def setUp(self):
        data=json.loads((ROOT/'experiment-results/two-source/verified-obstruction.json').read_text())
        self.V=data['values'];self.A=data['initial'];self.T=(1<<5)|(1<<9)

    def test_loss_allowed_only_after_fixed_priority_gain(self):
        move=compensated_relay(self.V,self.A,9,2,0,3,self.T)
        self.assertIsNotNone(move)
        self.assertEqual(move['compensation_value'],692)
        self.assertEqual(move['fairness_floor'],363)
        self.assertTrue(is_efx(self.V,move['allocation']))
        self.assertIsNone(compensated_relay(self.V,self.A,9,2,0,3,self.T,(3,2,1,0)))

    def test_relabeling_carries_agent_priority(self):
        original=compensated_relay(self.V,self.A,9,2,0,3,self.T)
        for p in permutations(range(4)):
            V=[None]*4;A=[None]*4;B=[None]*4
            for j in range(4):V[p[j]]=self.V[j];A[p[j]]=self.A[j];B[p[j]]=original['allocation'][j]
            mapped=compensated_relay(V,A,9,p[2],p[0],p[3],self.T,p)
            self.assertIsNotNone(mapped)
            self.assertEqual(mapped['allocation'],B)

    def test_priority_orbits_cover_every_order_exactly(self):
        result=report()
        for case in result['cases']:
            orbits=[{tuple(p[i] for i in order) for p in automorphisms(case)}
                    for order in priority_representatives(case)]
            self.assertEqual(sum(map(len,orbits)),24)
            self.assertEqual(set.union(*orbits),set(permutations(range(4))))
        saved=json.loads((ROOT/'research/priority-cases.json').read_text())
        self.assertEqual(json.loads(json.dumps(result)),saved)

    def test_invalid_priority_rejected(self):
        with self.assertRaises(ValueError):
            compensated_relay(self.V,self.A,9,2,0,3,self.T,(0,0,2,3))
