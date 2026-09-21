import unittest
from itertools import permutations
import numpy as np
from rebundle import nearest,distances,movement
from oracle import tables,verify_witness

class RebundleTests(unittest.TestCase):
    def test_distance_matches_direct_good_assignments(self):
        a=[1,2,4,1008];g=3
        targets=[[1,2,4,1008],[17,34,68,392],[1,2,8,1008]]
        new_gs=[3,9,2]
        _,_,sizes,_=tables([[1]*10 for _ in range(4)])
        for b,h in zip(targets,new_gs):
            d=int(distances(np.array([b]),np.array(a),sizes,int(g==h))[0])
            brute=10-int(g==h)-max(sum((a[i]&b[p[i]]).bit_count() for i in range(4)) for p in permutations(range(4)))
            self.assertEqual(d,brute)
            self.assertEqual(d,movement(a,g,b,h)['distance'])
    def test_five_memberships_are_necessary_for_trap(self):
        v=[[10]*4+[1]*6 for _ in range(4)]
        r=nearest(v,[1,2,4,1008],3,seconds=60)
        self.assertEqual(r['status'],'FOUND');self.assertEqual(r['minimum_radius'],5)
        self.assertTrue(verify_witness(v,r['witness']))
        self.assertEqual([x['radius'] for x in r['completed_radii']],list(range(5)))
    def test_bounded_failure_is_not_nonexistence(self):
        r=nearest([[10]*4+[1]*6 for _ in range(4)],[1,2,4,1008],3,max_radius=4,seconds=60)
        self.assertEqual(r['status'],'ABSENT_WITHIN_RADIUS')
    def test_zero_deadline(self):
        self.assertEqual(nearest([[1]*10 for _ in range(4)],[7,24,96,384],9,seconds=0)['status'],'UNKNOWN')

if __name__=='__main__':unittest.main()
