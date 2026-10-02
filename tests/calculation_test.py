"""Independent arithmetic QA. Uses eligible historical and synthetic data only.
Run: python -m unittest discover -s tests -p calculation_test.py -v
"""
import copy
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import calculate


def history_fixture(company):
    rows = calculate.historical(company)
    return rows, calculate.values(rows, '2025Q2')


def baseline_assumptions(company, b):
    if company == 'PG':
        return dict(sales_growth=0, gross_margin=b['gross_profit']/b['net_sales'],
                    sga_ratio=b['sga']/b['net_sales'],
                    net_nonoperating_income=b['pretax_income']-b['operating_income'],
                    effective_tax_rate=b['income_taxes']/b['pretax_income'],
                    noncontrolling_income=b['noncontrolling_income'],
                    diluted_shares=b['diluted_shares'],
                    ocf_to_net_income=b['operating_cash_flow']/b['net_income'],
                    capex_ratio=-b['capital_expenditures_signed']/b['net_sales'])
    return dict(earned_premium_growth=0, written_premium_growth=0,
                underlying_combined_ratio=b['underlying_combined_ratio']/100,
                catastrophe_losses=-b['catastrophe_losses_signed'],
                favorable_reserve_development=b['favorable_prior_year_development'],
                investment_income=b['investment_income_pretax'],
                other_income_including_interest=b['other_income_including_interest'],
                effective_tax_rate=b['core_income_tax']/b['core_pretax_income'],
                diluted_shares=b['diluted_shares'])


class FinancialArithmeticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.history, cls.base, cls.assumptions = {}, {}, {}
        for c in ('PG', 'TRV'):
            cls.history[c], cls.base[c] = history_fixture(c)
            cls.assumptions[c] = baseline_assumptions(c, cls.base[c])

    def test_pg_reconstructs_seasonal_financials_and_positive_capex(self):
        b = self.base['PG']; a = self.assumptions['PG']
        out = calculate.compute('PG', a, b)
        for metric in ('net_sales','gross_profit','sga','operating_income','pretax_income',
                       'income_taxes','net_income','net_income_attributable','operating_cash_flow'):
            self.assertAlmostEqual(out[metric], b[metric], places=7, msg=metric)
        self.assertAlmostEqual(out['capital_expenditures'], -b['capital_expenditures_signed'])
        self.assertAlmostEqual(out['free_cash_flow'], b['operating_cash_flow']+b['capital_expenditures_signed'])
        self.assertAlmostEqual(out['diluted_eps'], b['net_income_attributable']/b['diluted_shares'])

    def test_trv_reconstructs_signs_core_bridge_and_percent_conversion(self):
        b = self.base['TRV']; out = calculate.compute('TRV', self.assumptions['TRV'], b)
        for metric in ('net_earned_premiums','net_written_premiums','underwriting_gain',
                       'investment_income_pretax','core_pretax_income','core_income_tax','core_income'):
            self.assertAlmostEqual(out[metric], b[metric], places=7, msg=metric)
        self.assertAlmostEqual(out['underlying_underwriting_gain'],
                               b['underwriting_gain']-b['favorable_prior_year_development']-b['catastrophe_losses_signed'])
        self.assertAlmostEqual(out['underlying_combined_ratio'], .847)
        self.assertAlmostEqual(out['combined_ratio'], b['combined_ratio']/100, delta=.0005)
        self.assertNotAlmostEqual(out['basis_adjustment'], 0)

    def test_trv_catastrophe_and_reserves_have_opposite_aftertax_effects(self):
        a=self.assumptions['TRV']; b=self.base['TRV']; initial=calculate.compute('TRV',a,b)
        for driver, sign in [('catastrophe_losses',-1),('favorable_reserve_development',1)]:
            changed=calculate.compute('TRV',dict(a,**{driver:a[driver]+100}),b)
            self.assertAlmostEqual(changed['core_income']-initial['core_income'], sign*100*(1-a['effective_tax_rate']))
        higher_ratio=calculate.compute('TRV',dict(a,underlying_combined_ratio=a['underlying_combined_ratio']+.01),b)
        self.assertAlmostEqual(higher_ratio['underwriting_gain']-initial['underwriting_gain'],-b['net_earned_premiums']*.01)

    def test_written_premiums_do_not_double_count_earned_revenue(self):
        a=self.assumptions['TRV']; b=self.base['TRV']; first=calculate.compute('TRV',a,b)
        second=calculate.compute('TRV',dict(a,written_premium_growth=.10),b)
        self.assertAlmostEqual(second['net_written_premiums'],b['net_written_premiums']*1.10)
        for key in ('net_earned_premiums','underwriting_gain','core_income'):
            self.assertEqual(first[key],second[key])

    def test_shares_affect_only_per_share_results(self):
        for company, per_share, profit in [('PG','diluted_eps','net_income_attributable'),
                                           ('TRV','core_income_per_diluted_share_proxy','core_income')]:
            a=self.assumptions[company]; b=self.base[company]
            first=calculate.compute(company,a,b)
            second=calculate.compute(company,dict(a,diluted_shares=a['diluted_shares']*.9),b)
            self.assertEqual(first[profit],second[profit])
            self.assertAlmostEqual(second[per_share],first[per_share]/.9)

    def test_pg_sga_and_cash_conversion_have_distinct_channels(self):
        a=self.assumptions['PG']; b=self.base['PG']; first=calculate.compute('PG',a,b)
        changed=calculate.compute('PG',dict(a,sga_ratio=a['sga_ratio']+.01),b)
        self.assertAlmostEqual(changed['net_income']-first['net_income'],-b['net_sales']*.01*(1-a['effective_tax_rate']))
        cash=calculate.compute('PG',dict(a,ocf_to_net_income=a['ocf_to_net_income']+.1),b)
        self.assertEqual(cash['net_income'],first['net_income'])
        self.assertAlmostEqual(cash['operating_cash_flow']-first['operating_cash_flow'],first['net_income']*.1)

    def test_failed_eighth_freeze_prevents_any_actual_read(self):
        calls=[]
        def gate(path):
            calls.append(path)
            if len(calls)==8: raise ValueError('synthetic invalid freeze')
            return {}
        with tempfile.TemporaryDirectory() as td:
            with patch.object(calculate,'ROOT',Path(td)), patch.object(calculate,'replay',side_effect=gate), patch.object(calculate,'read') as reader:
                with self.assertRaisesRegex(ValueError,'invalid freeze'): calculate.main()
                reader.assert_not_called()
        self.assertEqual(len(calls),8)

    def test_full_synthetic_pipeline_accuracy_bridges_and_original_units(self):
        # Synthetic target values: no held-out company outcome is read by this test.
        events=[]; model_actual={}; raw_actual={}
        for c in ('PG','TRV'):
            a=copy.deepcopy(self.assumptions[c]); b=self.base[c]
            if c=='PG': a['sales_growth']=.075
            else: a['earned_premium_growth']=.075
            metrics=calculate.compute(c,a,b)
            if c=='PG':
                metrics.update(net_nonoperating_income=a['net_nonoperating_income'],
                               noncontrolling_income=a['noncontrolling_income'],diluted_shares=a['diluted_shares'])
            else:
                metrics.update(other_income_including_interest=a['other_income_including_interest'],diluted_shares=a['diluted_shares'])
                # A deliberate target basis difference must stay visible in the residual.
                metrics['core_pretax_income']+=10
                metrics['core_income_tax']+=2
                metrics['core_income']+=8
            model_actual[c]=metrics
            raw_actual[c]={'underlying_combined_ratio':84.7} if c=='TRV' else {'effective_tax_rate':19.8}
        data={'companies':{c:{'model_metrics':model_actual[c],'raw_metrics':raw_actual[c]} for c in model_actual}}
        def frozen(path):
            events.append('freeze:'+path.name); c=path.name.split('_')[0]
            offset={'pre_history':0,'pre_market':.01,'mid_history':.02,'mid_market':.03}['_'.join(path.name.split('_')[1:])]
            assumptions=copy.deepcopy(self.assumptions[c]); assumptions['sales_growth' if c=='PG' else 'earned_premium_growth']=offset
            return {'assumptions':[dict(driver=k,bear=v,base=v,bull=v) for k,v in assumptions.items()]}
        def reader(path):
            if path.name=='actuals.json':events.append('actual_read');return copy.deepcopy(data)
            if path.name=='history_tidy.json':return []
            if path.name=='freeze.json':return {'synthetic':True}
            if path.name=='output.json':return {'decision':'pass'}
            raise AssertionError('Unexpected read: '+str(path))
        with tempfile.TemporaryDirectory() as td:
            with patch.object(calculate,'ROOT',Path(td)),patch.object(calculate,'replay',side_effect=frozen),patch.object(calculate,'read',side_effect=reader),patch.object(calculate,'historical',side_effect=lambda c:self.history[c]),redirect_stdout(io.StringIO()):
                calculate.main()
            output=json.loads((Path(td)/'outputs/analysis.json').read_text())
            checks=json.loads((Path(td)/'outputs/calculation_checks.json').read_text())
        self.assertEqual(events[8],'actual_read')
        self.assertTrue(all(x.startswith('freeze:') for x in events[:8]))
        self.assertEqual(len(checks),30)
        self.assertTrue(all(abs(x['difference'])<=x['tolerance'] for x in checks))
        for c in ('PG','TRV'):
            d=output[c]; self.assertEqual(len(d['forecasts']),12)
            for row in d['accuracy']:
                self.assertAlmostEqual(row['absolute_percentage_error'],abs(row['base_profit']-row['actual_profit'])/abs(row['actual_profit']))
            self.assertEqual(d['actual']['raw_metrics'],raw_actual[c])
            mid=next(f for f in d['forecasts'] if f['vintage']=='mid_market' and f['case']=='base')
            metric='net_income_attributable' if c=='PG' else 'core_income'
            self.assertAlmostEqual(mid['metrics'][metric]+sum(x['profit_change'] for x in d['actual_bridge']),model_actual[c][metric])
            for row in d['variances']:
                self.assertAlmostEqual(row['difference'],row['actual']-row['forecast'])
                if row['forecast']:self.assertAlmostEqual(row['relative_difference'],row['difference']/abs(row['forecast']))
        self.assertNotAlmostEqual(output['TRV']['actual_bridge'][-1]['profit_change'],0)


if __name__=='__main__':unittest.main()
