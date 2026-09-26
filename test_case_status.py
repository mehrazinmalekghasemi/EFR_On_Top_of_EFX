import json,unittest
from collections import Counter
from pathlib import Path
from case_status import classify,render,ROOT


class CaseStatusTests(unittest.TestCase):
    def test_disjoint_complete_classification(self):
        rows=classify();self.assertEqual(len(rows),1344)
        self.assertEqual(len({r['id'] for r in rows}),1344)
        c=Counter(r['status'] for r in rows)
        self.assertEqual(sum(n for k,n in c.items() if k.startswith('T')),1189)
        self.assertEqual((c['CP1'],c['CP2'],c['OPEN']),(49,3,103))
        self.assertEqual(Counter(len(r['sources']) for r in rows if r['status']=='OPEN'),{2:94,3:9})
        self.assertTrue(all(r['profile'] not in ([1,1,1,6],[2,2,2,3]) for r in rows if r['status']=='OPEN'))

    def test_generated_documents_current(self):
        for name,content in render().items():self.assertEqual((ROOT/name).read_text(),content,name)

    def test_three_source_topology(self):
        cases=[r for r in classify() if r['status']=='OPEN' and len(r['sources'])==3]
        self.assertEqual(len(cases),9)
        self.assertTrue(all(r['profile'][0]==1 and all(b==0 for a,b in r['edges']) for r in cases))

if __name__=='__main__':unittest.main()
