import copy
import importlib.util
import unittest
import tempfile
from unittest.mock import patch
from pathlib import Path
spec=importlib.util.spec_from_file_location('workflow',Path(__file__).resolve().parents[1]/'src/workflow.py')
w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.p={'company':'Test','sector':'insurance','cutoff':'2026-03-31',
                'target_period':{'start':'2026-04-01','end':'2026-06-30'},
                'history':[{'source_id':'s1','published_at':'2026-01-20','period_end':'2025-12-31','source_excerpt':'Revenue 100'}],
                'evidence':[],'driver_contract':[{'driver':'growth','unit':'decimal','min':-1,'max':1}]}
    def test_date_gate(self):
        self.p['history'][0]['published_at']='2026-04-02'
        with self.assertRaises(ValueError):w.validate_packet(self.p)
    def test_holdout_gate(self):
        self.p['nested']={'actuals':100}
        with self.assertRaises(ValueError):w.validate_packet(self.p)
    def test_period_gate(self):
        self.p['history'][0]['period_end']='2026-06-30'
        with self.assertRaises(ValueError):w.validate_packet(self.p)
    def test_citation_and_bounds(self):
        output={'role':'scenario','limitations':[],'narrative':'Test','assumptions':[{'driver':'growth','unit':'decimal','bear':-.1,'base':.1,'bull':.2,'basis':'Illustrative','source_ids':['s1']}]}
        w.validate_output('scenario',output,self.p)
        bad=copy.deepcopy(output);bad['assumptions'][0]['source_ids']=['invented']
        with self.assertRaises(ValueError):w.validate_output('scenario',bad,self.p)
        bad=copy.deepcopy(output);bad['assumptions'][0]['bull']=2
        with self.assertRaises(ValueError):w.validate_output('scenario',bad,self.p)
    def test_qa_cannot_self_attest(self):
        del self.p['history'][0]['source_excerpt']
        with self.assertRaises(ValueError):
            w.validate_output('qa',{'role':'qa','limitations':[],'decision':'pass','source_accuracy':'checked_against_provided_excerpts','findings':[]},self.p)
    def test_replay_checks_freeze_before_reading_actuals(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)
            w.write(path/'packet.json',self.p)
            w.write(path/'freeze.json',{'files':{'packet.json':'wrong'}})
            with patch.object(w.subprocess,'run',side_effect=AssertionError('Replay cannot invoke model')):
                with self.assertRaisesRegex(ValueError,'Frozen file changed'):
                    w.unlock_actuals(path,path/'nonexistent_actuals.json')
    def test_control_excludes_market_evidence(self):
        self.p['vintage']='mid_history'
        self.p['evidence']=[{'source_id':'s2','published_at':'2026-03-01'}]
        with self.assertRaises(ValueError):w.validate_packet(self.p)
    def test_role_envelope_rejects_hidden_actuals(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.object(w.subprocess,'run',side_effect=AssertionError('No model call allowed')):
                with self.assertRaisesRegex(ValueError,'Target actuals forbidden'):
                    w.model_role('scenario',{'packet':self.p,'prior_outputs':{'actuals':100}},Path(folder)/'run')
    def test_excluded_source_gate(self):
        self.p['history'][0]['excluded_from_model']=True
        with self.assertRaisesRegex(ValueError,'Excluded source'):
            w.validate_packet(self.p)
    def test_review_cannot_modify_frozen_run(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder);w.write(path/'freeze.json',{'status':'frozen'})
            with self.assertRaisesRegex(ValueError,'Already frozen'):
                w.review_qa(path,path/'missing.json')
    def test_review_rejects_future_source_before_archiving(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder);w.write(path/'packet.json',self.p)
            outputs={
                'finance':{'role':'finance','limitations':[],'mappings':[],'issues':[]},
                'research':{'role':'research','limitations':[],'signals':[]},
                'scenario':{'role':'scenario','limitations':[],'narrative':'Test','assumptions':[{'driver':'growth','unit':'decimal','bear':-.1,'base':0,'bull':.1,'basis':'Test','source_ids':['s1']}]},
                'qa':{'role':'qa','limitations':[],'decision':'revise','source_accuracy':'not_verified','findings':[]}}
            for role,output in outputs.items():
                (path/role).mkdir();w.write(path/role/'output.json',output)
            w.write(path/'supplement.json',{'reviews':[{'source_id':'s1','publication_date':'2026-04-01'}]})
            with self.assertRaisesRegex(ValueError,'Post-cutoff source'):
                w.review_qa(path,path/'supplement.json')
            self.assertFalse((path/'qa_initial').exists())
    def test_canonical_hash(self):
        self.assertEqual(w.digest({'a':1,'b':2}),w.digest({'b':2,'a':1}))
        with self.assertRaises(ValueError):w.digest({'a':float('nan')})
if __name__=='__main__':unittest.main()
