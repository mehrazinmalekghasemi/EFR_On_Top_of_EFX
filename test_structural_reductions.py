import json,unittest
from pathlib import Path
import z3
from structural_reductions import catalog,graph_data
from structural_efr_search import build
from oracle import is_efx,integer_rows,verify_witness
from capacity import diagnostics
from restoration_moves import source_analysis

class StructuralReductionTests(unittest.TestCase):
    def test_exact_catalog_and_remaining_pair_blockers(self):
        cases,s=catalog()
        self.assertEqual(s['labeled_dags'],{1:316,2:198,3:28,4:1})
        self.assertEqual((s['before'],s['after_source_lemmas'],s['after_triple_source_lemma'],s['after_pair_lemma']),(1344,196,174,156))
        self.assertEqual(s['by_sources'],{2:140,3:15,4:1})
        for c in cases:
            self.assertGreaterEqual(len(c['sources']),2)
            for k in c['sources']:
                self.assertGreaterEqual(c['profile'][k],2)
                if c['profile'][k]==2:
                    self.assertTrue(any(c['profile'][i]!=2 and not c['reach'][k][i] for i in range(4)))

    def test_blocked_four_source_example_in_search_domain(self):
        x=json.loads((Path(__file__).resolve().parent/'experiment-results/structural-reduction/four-source-example.json').read_text())
        V=x['values'];A=x['initial']
        self.assertTrue(is_efx(V,A))
        self.assertEqual(source_analysis(V,A,9)['sources'],[0,1,2,3])
        self.assertFalse(source_analysis(V,A,9)['moves'])
        self.assertFalse(any(t['feasible'] for t in diagnostics(V,A,9)))
        case=next(c for c in catalog()[0] if c['id']=='2223_000');solver,v=build(case)
        for i,row in enumerate(V):
            for h,value in enumerate(row):solver.add(v[i][h]==z3.RealVal(value)/sum(row))
        self.assertEqual(solver.check(),z3.sat)
        self.assertTrue(verify_witness(V,x['nearest_escape']['witness']))

    def test_singleton_source_blocker_gives_safe_singleton_move(self):
        A=[1,6,56,448]
        V=[[6 if A[i]>>h&1 and i==0 else 3 if A[i]>>h&1 and i==1 else 2 if A[i]>>h&1 else 1 for h in range(9)]+[100] for i in range(4)]
        self.assertTrue(is_efx(V,A))
        self.assertEqual(source_analysis(V,A,9)['sources'],[0,1,2,3])
        self.assertFalse(diagnostics(V,A,9)[0]['feasible'])
        B=A.copy();B[1]=512
        self.assertTrue(is_efx(V,B))
        self.assertGreater(V[1][9],sum(V[1][h] for h in [1,2]))

    def test_short_pilot_cases_remain_in_final_catalog(self):
        report=json.loads((Path(__file__).resolve().parent/'experiment-results/structural-pilot/summary.json').read_text())
        cases={c['id']:c for c in catalog()[0]}
        for r in report['results']:self.assertEqual(cases[r['case']['id']],r['case'])

if __name__=='__main__':unittest.main()
