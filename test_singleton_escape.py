import unittest
from singleton_escape import escape
from capacity import diagnostics, repair
from oracle import verify_witness

class SingletonEscapeTests(unittest.TestCase):
    def test_blocked_instance_with_different_minima(self):
        V=[[6,5,5,1,1,1,1,1,1,20],
           [1,3,3,3,3,3,1,1,1,20],
           [1,1,1,2,2,2,3,3,3,20],
           [1,1,1,1,1,1,2,2,2,20]]
        A=[1,6,56,448]
        self.assertFalse(any(all(row[g]==min(row) for row in V) for g in range(10)))
        self.assertFalse(any(t['feasible'] for t in diagnostics(V,A,9)))
        r=escape(V,A,9,0)
        self.assertEqual(r['status'],'IMPROVED_EFX_PREDECESSOR')
        self.assertEqual(r['movement']['distance'],2)
        self.assertEqual(r['utilities_after'],['10','20','6','6'])
        q=repair(V,r['predecessor'],r['deleted'])
        self.assertEqual(q['status'],'FOUND')
        self.assertTrue(verify_witness(V,q))

    def test_large_source_trap_not_claimed_solved(self):
        V=[[10]*4+[1]*6 for _ in range(4)]
        r=escape(V,[1,2,4,1008],3,3)
        self.assertEqual(r['status'],'NOT_APPLICABLE')

if __name__=='__main__':unittest.main()
