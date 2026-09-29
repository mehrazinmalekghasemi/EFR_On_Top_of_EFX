import json
import unittest
from fractions import Fraction
from pathlib import Path
from itertools import product
from efr.eight_plus_two import extensions,search,validate_eight


def fair(V,A,kind):
    rows=[[Fraction(str(x)) for x in row] for row in V]
    def val(i,b):return sum(rows[i][g] for g in range(10) if b>>g&1)
    for i,j in product(range(4),repeat=2):
        if i==j:continue
        goods=[g for g in range(10) if A[j]>>g&1]
        if kind=='EFX':
            if any(val(i,A[i])<val(i,A[j])-rows[i][g] for g in goods):return False
        elif goods and len(goods)*val(i,A[i])<(len(goods)-1)*val(i,A[j]):return False
    return True


class EightPlusTwoTests(unittest.TestCase):
    def check_witness(self,V,w):
        A=w['predecessor'];B=w['allocation'];g,h=w['missing'];p,q=w['recipients']
        self.assertEqual(sum(A),1023^(1<<g)^(1<<h));self.assertEqual(sum(B),1023)
        for i,j in product(range(4),repeat=2):
            if i!=j:self.assertEqual(B[i]&B[j],0)
        C=A.copy();C[p]|=1<<g;C[q]|=1<<h
        self.assertEqual(C,B);self.assertTrue(fair(V,A,'EFX'));self.assertTrue(fair(V,B,'EFR'))

    def test_simultaneous_rescue(self):
        V=[[1]*8+[2,2] for _ in range(2)]+[[1]*8+[0,0] for _ in range(2)]
        A=[3,12,48,192]
        self.assertTrue(fair(V,A,'EFX'))
        for g,p in product([8,9],range(4)):
            B=A.copy();B[p]|=1<<g;self.assertFalse(fair(V,B,'EFR'))
        B=A.copy();B[0]|=1<<8;B[1]|=1<<9
        self.assertTrue(fair(V,B,'EFX'))
        got=extensions(V,A,[8,9]);self.assertTrue(any(w['allocation']==B for w in got))
        expected=[]
        for p,q in product(range(4),repeat=2):
            C=A.copy();C[p]|=1<<8;C[q]|=1<<9
            if fair(V,C,'EFR'):expected.append([p,q])
        self.assertEqual([w['recipients'] for w in got],expected)

    def test_arbitrary_pair_fails(self):
        V=[[1]*8+[100,100] for _ in range(4)]
        r=search(V,[8,9]);self.assertEqual(r['status'],'NO_BRIDGE');self.assertTrue(r['complete'])
        self.assertEqual(r['efx_predecessors'],2520)
        r=search(V);self.assertEqual(r['status'],'FOUND');self.check_witness(V,r['witness'])

    def test_recorded_witnesses(self):
        root=Path(__file__).resolve().parents[1]
        data=json.loads((root/'experiment-results/eight-plus-two/results.json').read_text())
        for w in data['instances']:
            source=json.loads((root/w['source']).read_text());s=source[w['index']] if isinstance(source,list) else source
            self.check_witness(s['values'],w['search']['witness'])
            if w['local_witness']:self.check_witness(s['values'],w['local_witness'])

    def test_local_obstruction_independently(self):
        root=Path(__file__).resolve().parents[1]
        w=json.loads((root/'experiment-results/eight-plus-two/no-local-1125.json').read_text())
        V=w['values'];A=w['initial'];self.assertTrue(fair(V,A,'EFX'))
        rows=[[Fraction(x) for x in row] for row in V]
        val=lambda i,b:sum(rows[i][h] for h in range(10) if b>>h&1)
        edges={(i,j) for i,j in product(range(4),repeat=2) if i!=j and val(i,A[j])>val(i,A[i])}
        self.assertEqual(edges,{(0,1),(2,0)})
        for p in range(4):
            B=A.copy();B[p]|=512;self.assertFalse(fair(V,B,'EFR'))
        removable=[]
        for t,b in enumerate(A):
            for h in range(9):
                if not b>>h&1:continue
                C=A.copy();C[t]^=1<<h
                if not fair(V,C,'EFX'):continue
                removable.append(h)
                for p,q in product(range(4),repeat=2):
                    B=C.copy();B[p]|=512;B[q]|=1<<h
                    self.assertFalse(fair(V,B,'EFR'))
        self.assertEqual(removable,[4,5,6,7])
        self.check_witness(V,w['unrestricted_bridge']['witness'])

    def test_timeout_and_invalid_input(self):
        self.assertEqual(search([[1]*10]*4,seconds=0)['status'],'UNKNOWN')
        with self.assertRaises(ValueError):validate_eight([[1]*10]*4,[3,3,48,192],[8,9])
        with self.assertRaises(ValueError):search([[1]*10]*4,[8,8])

    def test_big_integer_path(self):
        V=[[1]*8+[10**30,10**30+1] for _ in range(4)]
        r=search(V);self.assertEqual(r['status'],'FOUND');self.check_witness(V,r['witness'])

if __name__=='__main__':unittest.main()
