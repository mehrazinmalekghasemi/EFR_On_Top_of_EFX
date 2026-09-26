import json,unittest
from pathlib import Path
from oracle import is_efx,verify_witness,tables,integer_rows
from two_source_moves import four_source_progress,local_moves,compensated_path
from verify_two_source import literal_verification

ROOT=Path(__file__).resolve().parent

class TwoSourceTests(unittest.TestCase):
    def test_four_source_compensation_and_triple_replacement(self):
        x=json.loads((ROOT/'experiment-results/structural-reduction/four-source-example.json').read_text())
        move=four_source_progress(x['values'],x['initial'],9)
        self.assertEqual(move['kind'],'compensated_pair')
        self.assertTrue(is_efx(x['values'],move['allocation']))
        A=[3,12,48,448]
        V=[[14 if A[i]>>h&1 else 8 if h>=6 else 12 for h in range(9)]+[14] for i in range(3)]+[[4]*6+[3]*3+[6]]
        move=four_source_progress(V,A,9)
        self.assertEqual(move['kind'],'triple_replacement')
        self.assertTrue(is_efx(V,move['allocation']))

    def test_nondegenerate_two_agent_trap_and_three_agent_escape(self):
        x=json.loads((ROOT/'experiment-results/two-source/verified-obstruction.json').read_text())
        V=x['lift']['values'];A=x['initial']
        a=local_moves(V,A,9,dominance='lex');self.assertEqual(a['status'],'ABSENT');self.assertEqual(a['checked'],8532)
        b=literal_verification(V,A,9)
        self.assertEqual(b['subset_value_counts'],[1024]*4)
        self.assertEqual(b['totals']['lex_improvements'],0);self.assertEqual(b['totals']['complete_efr'],0)
        moves=compensated_path(V,A,9);self.assertTrue(moves)
        self.assertTrue(any(m['allocation']==[544,2,1,28] for m in moves))
        self.assertTrue(verify_witness(V,{'allocation':x['three_agent_completion']['allocation']},'efr'))
        self.assertTrue(verify_witness(V,x['mode_c']['witnesses'][0]))

    def test_reduction_replay_scope_and_counts(self):
        p=ROOT/'experiment-results/two-source'
        counts=json.loads((p/'reduction-summary.json').read_text());self.assertEqual(counts['remaining'],103)
        records=json.loads((p/'cvc5-replay.json').read_text());self.assertEqual(len(records),53)
        self.assertTrue(all(r['replies']==['unsat'] and r['check_proofs'] for r in records))
        # The duplicate four-source replay was removed; every region appears once.
        self.assertEqual(len({Path(r['file']).name.split('-')[0] for r in records}),53)

if __name__=='__main__':unittest.main()
