import io
import itertools
from pathlib import Path
import tarfile
import tempfile
import unittest
from unittest.mock import patch
import ci

class WorkflowTests(unittest.TestCase):
    def checkpoint(self,path,goal='extension',shards=4,shard=1):
        ci.save(path/'campaign.json',ci.identity(goal,shards,shard))
        ci.save(path/'config.json',{'goal':goal})
        ci.save(path/'nodes'/'r_0_0_0.json',{'id':'r_0_0_0','status':'OPEN','witnesses':[]})
    def test_archive_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.checkpoint(p/'one');ci.pack(p/'one',p/'saved.tar.gz')
            ci.restore(p/'saved.tar.gz',p/'two',ci.identity('extension',4,1))
            self.assertEqual((p/'one/nodes/r_0_0_0.json').read_bytes(),(p/'two/nodes/r_0_0_0.json').read_bytes())
    def test_reject_mismatched_goal_sharding_and_code(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);self.checkpoint(p/'one');ci.pack(p/'one',p/'saved.tar.gz')
            for field,value in [('goal','efr'),('shards',20),('shard',2),('code_sha256','wrong')]:
                expected=ci.identity('extension',4,1);expected[field]=value
                with self.assertRaises(ValueError):ci.restore(p/'saved.tar.gz',p/'two',expected)
    def test_reject_unsafe_archive_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            with tarfile.open(p/'bad.tar.gz','w:gz') as t:
                entry=tarfile.TarInfo('../escape');entry.size=1;t.addfile(entry,io.BytesIO(b'x'))
            with self.assertRaises(ValueError):ci.restore(p/'bad.tar.gz',p/'out',ci.identity('extension',4,1))
    def reports(self):
        out=[]
        for i in range(4):
            out.append({**ci.identity('extension',4,i),'run_id':'123','status':'VERIFIED',
                        'verification':{'verdict':'VERIFIED_SHARD_ONLY','goal':'extension','shards':4,
                        'shard':i,'all_required_roots':220,'roots_checked':55,'roots_verified':55}})
        return out
    def test_all_shards_required(self):
        reports=self.reports()
        self.assertEqual(ci.combine_reports(reports,'extension',4,'123')['verdict'],'ALL_SHARDS_VERIFIED')
        self.assertEqual(ci.combine_reports(reports[:-1],'extension',4,'123')['verdict'],'INCOMPLETE_NO_THEOREM')
        reports[-1]['verification']['roots_verified']=54
        self.assertEqual(ci.combine_reports(reports,'extension',4,'123')['verdict'],'INCOMPLETE_NO_THEOREM')
    def test_reject_duplicate_or_stale_reports(self):
        with self.assertRaises(ValueError):ci.combine_reports(self.reports()*2,'extension',4,'123')
        with self.assertRaises(ValueError):ci.combine_reports(self.reports(),'extension',4,'999')
    def test_input_validation(self):
        env={'GOAL':'extension','MODE':'search','SHARDS':'4','MINUTES':'15','RESUME_RUN':'$(anything)'}
        with patch.dict('os.environ',env):
            with self.assertRaises(ValueError):ci.plan()
    def test_progress_excludes_other_shards(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)
            for fav in itertools.combinations_with_replacement(range(10),3):
                key='r_'+'_'.join(map(str,fav));ci.save(p/'nodes'/f'{key}.json',{'id':key,'status':'COVERED'})
            r=ci.shard_progress(p,'extension',4,1)
            self.assertEqual(r['owned_roots'],55);self.assertEqual(r['search_covered_roots'],55)

if __name__=='__main__':unittest.main()
