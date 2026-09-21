from fractions import Fraction
import itertools
import unittest
from capacity import diagnostics,repair,validate
from oracle import is_efr
from search import visit_budgets,should_split

A=[7,24,96,384]
V=[[2,2,2,6,6,1,1,1,1,1],
   [1,1,1,3,3,6,6,1,1,1],
   [1,1,1,1,1,3,3,6,6,1],
   [3,3,3,1,1,1,1,3,3,1]]

class Improvements(unittest.TestCase):
    def test_escalation_and_split(self):
        opts={'slice_seconds':60,'smt_seconds':10,'split_after':2}
        self.assertEqual(visit_budgets({},opts),(60,10))
        self.assertEqual(visit_budgets({'visits':1},opts),(120,20))
        self.assertEqual(visit_budgets({'visits':99},opts),(240,40))
        self.assertFalse(should_split({'visits':1},opts))
        self.assertTrue(should_split({'visits':2},opts))
        self.assertFalse(should_split({'visits':99},{**opts,'no_split':True}))
    def test_least_good_obstruction_and_repair(self):
        validate(V,A,9)
        self.assertTrue(all(row[9]<=min(row[:9]) for row in V))
        self.assertFalse(any(t['feasible'] for t in diagnostics(V,A,9)))
        r=repair(V,A,9)
        self.assertEqual(r['status'],'FOUND');self.assertTrue(r['rotations'])
        validate(V,r['predecessor'],9)
        self.assertTrue(is_efr(V,r['allocation']))
    def test_fixed_deletion_obstruction(self):
        r=repair([[1]*9+[2] for _ in range(4)],A,9)
        self.assertEqual(r['status'],'NO_INSERTION_AFTER_THIS_REPAIR')
    def test_empty_target_and_rationals(self):
        v=[['1/3','1/2'],['2/3','1/7'],['0','0'],['0','0']]
        r=repair(v,[1,0,0,0],1)
        self.assertEqual(r['status'],'FOUND')
        self.assertTrue(is_efr([[Fraction(x) for x in row] for row in v],r['allocation']))
    def test_exhaustive_small_common_least(self):
        # Two agents, three old goods, every binary positive valuation and EFX predecessor.
        checked=0
        for entries in itertools.product((1,2),repeat=6):
            v=[list(entries[:3])+[1],list(entries[3:])+[1]]
            for mask in range(8):
                a=[mask,7^mask]
                try:validate(v,a,3)
                except ValueError:continue
                r=repair(v,a,3);self.assertEqual(r['status'],'FOUND')
                # Independent full EFR check, including the recipient's comparisons.
                for i in range(2):
                    own=sum(v[i][g] for g in range(4) if r['allocation'][i]>>g&1)
                    for b in r['allocation']:
                        s=b.bit_count();total=sum(v[i][g] for g in range(4) if b>>g&1)
                        self.assertGreaterEqual(s*own,(s-1)*total)
                checked+=1
        self.assertGreater(checked,0)

if __name__=='__main__':unittest.main()
