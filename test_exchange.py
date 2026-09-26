import unittest
from exchange_search import ExchangeSearch,verify_trap
from oracle import verify_witness

class ExchangeTests(unittest.TestCase):
    def test_closed_trap(self):
        v=[[10]*4+[1]*6 for _ in range(4)];a=[1,2,4,1008]
        r=ExchangeSearch(v).solve(a,3)
        self.assertEqual(r['status'],'TRAPPED');self.assertEqual(r['states_expanded'],4)
        self.assertTrue(verify_trap(v,a,3,r['closed_component']))
        self.assertFalse(verify_trap(v,a,3,r['closed_component'][:-1]))
    def test_boundary_values(self):
        for h in [6,36,100]:
            r=ExchangeSearch([[h]*4+[1]*6 for _ in range(4)]).solve([1,2,4,1008],3)
            self.assertEqual(r['status'],'FOUND');self.assertEqual(r['exchange_depth'],0)
    def test_exchange_repairs_fixed_deletion(self):
        v=[[1]*9+[2] for _ in range(4)]
        r=ExchangeSearch(v).solve([7,24,96,384],9)
        self.assertEqual(r['status'],'FOUND');self.assertEqual(r['exchange_depth'],1)
        self.assertTrue(verify_witness(v,r['witness']))
    def test_caps_are_unknown(self):
        s=ExchangeSearch([[10]*4+[1]*6 for _ in range(4)])
        self.assertEqual(s.solve([1,2,4,1008],3,max_states=1)['status'],'UNKNOWN')
        self.assertEqual(s.solve([1,2,4,1008],3,seconds=0)['status'],'UNKNOWN')
    def test_ownership_repair(self):
        from test_improvements import V,A
        r=ExchangeSearch(V).solve(A,9)
        self.assertFalse(r['direct']);self.assertEqual(r['exchange_depth'],0)
        self.assertTrue(verify_witness(V,r['witness']))

if __name__=='__main__':unittest.main()
