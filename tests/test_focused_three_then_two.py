import unittest
from itertools import permutations
from efr.focused_three_then_two import singleton_pair_mutual,single_observer_quad_escape,reverse_dangerous_transfer
from tests.test_dangerous_moves import literal_check

class FocusedThreeThenTwoTests(unittest.TestCase):
    def test_singleton_champion_mutual_cases_and_relabelings(self):
        A=[1,6,56,448]
        V=[[300,150,150,30,30,30,30,30,30,180],[0,570,30,540,30,30,0,300,300,0],[600,100,100,100,100,100,123,123,15,180],[600,100,100,123,123,15,100,100,100,180]]
        for repair in (True,False):
            W=[row[:] for row in V]
            if not repair:W[1]=[0,300,300,120,120,120,120,120,120,150]
            result=singleton_pair_mutual(W,A,9,1,2,3)
            self.assertEqual(result['kind'],'singleton_champion_four_agent_repair' if repair else 'singleton_champion_mutual_exchange')
            for p in permutations(range(4)):
                Z=[None]*4;C=[None]*4
                for j in range(4):Z[p[j]]=W[j];C[p[j]]=A[j]
                B=singleton_pair_mutual(Z,C,9,p[1],p[2],p[3])['allocation'];literal_check(Z,C,B)

    def test_single_observer_triangle_and_guard_failures(self):
        A=[1,6,24,480]
        V=[[10,0,0,0,0,3,3,3,1,5],[0,5,5,0,0,0,0,0,0,0],[0,0,0,5,5,0,0,0,0,0],[9,0,0,0,0,2,2,2,2,3]]
        literal_check(V,A,single_observer_quad_escape(V,A,9,3)['allocation'])
        W=[row[:] for row in V];W[3][0]=0
        self.assertIsNone(single_observer_quad_escape(W,A,9,3))
        W=[row[:] for row in V];W[1]=[0,5,5,0,0,3,3,3,1,5]
        self.assertIsNone(single_observer_quad_escape(W,A,9,3))

    def test_reverse_transfer_compensation_and_blocker_rotation(self):
        A=[1,2,28,480]
        V=[[20,0,1,1,1,1,1,1,1,2],[0,20,1,1,1,1,1,1,1,2],[11,11,6,2,2,7,0,0,0,2],[0,0,21,1,1,18,4,4,4,10]]
        for blocked in (False,True):
            W=[row[:] for row in V]
            if blocked:W[0]=[10,0,0,6,4,6,0,0,0,2]
            result=reverse_dangerous_transfer(W,A,9,2,3,2)
            self.assertEqual(result['kind'],'reverse_dangerous_blocker_escape' if blocked else 'reverse_dangerous_compensation')
            for p in permutations(range(4)):
                Z=[None]*4;C=[None]*4
                for j in range(4):Z[p[j]]=W[j];C[p[j]]=A[j]
                B=reverse_dangerous_transfer(Z,C,9,p[2],p[3],2)['allocation'];literal_check(Z,C,B)
        W=[row[:] for row in V];W[2][5:9]=[1,3,3,0]
        result=reverse_dangerous_transfer(W,A,9,2,3,2)
        self.assertEqual(result['compensation'],192);literal_check(W,A,result['allocation'])
        W[2][5:9]=[1,1,1,1]
        self.assertIsNone(reverse_dangerous_transfer(W,A,9,2,3,2))
