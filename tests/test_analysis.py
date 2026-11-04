import unittest

import pandas as pd

from src.decompose import age_standardized_rate, shift_share
from src.indicators import supplementary_indicators, validate_against_published


class IndicatorTests(unittest.TestCase):
    def test_supplementary_formulas(self):
        result = supplementary_indicators(*[pd.Series([x]) for x in (5, 100, 3, 4, 6)])
        self.assertAlmostEqual(result.loc[0, 'official'], 5)
        self.assertAlmostEqual(result.loc[0, 'supp1'], 8)
        self.assertAlmostEqual(result.loc[0, 'supp2'], 15 / 110 * 100)
        self.assertAlmostEqual(result.loc[0, 'supp3'], 18 / 110 * 100)

    def test_tolerance_uses_unrounded_difference(self):
        result = validate_against_published(pd.Series([5.1004, 5.1]), pd.Series([5., 5.]))
        self.assertEqual(result['exceeds_tol'].tolist(), [True, False])

    def test_missing_or_infinite_comparisons_do_not_pass(self):
        result = validate_against_published(
            pd.Series([5., float('inf')], index=['a', 'b']),
            pd.Series([5., 5.], index=['b', 'c']),
        )
        self.assertTrue(result['invalid_data'].all())
        self.assertTrue(result['exceeds_tol'].all())

    def test_nullable_missing_comparison_does_not_pass(self):
        result = validate_against_published(
            pd.Series([pd.NA], dtype='Float64'), pd.Series([5.])
        )
        self.assertTrue(result.loc[0, 'invalid_data'])
        self.assertTrue(result.loc[0, 'exceeds_tol'])


class DecompositionTests(unittest.TestCase):
    def setUp(self):
        self.population = pd.Series([100., 200.], index=['15-19', '20-24'])
        self.rates = pd.Series([0.4, 0.6], index=self.population.index)

    def test_effects_sum_to_employment_change(self):
        pop1 = self.population + pd.Series([10., -20.], index=self.population.index)
        rate1 = self.rates + pd.Series([0.1, -0.05], index=self.population.index)
        result = shift_share(self.population, self.rates, pop1, rate1)
        expected = (pop1 * rate1 - self.population * self.rates).sum()
        self.assertAlmostEqual(result.loc['합계', 'total'], expected)

    def test_shift_share_rejects_missing_groups(self):
        with self.assertRaises(ValueError):
            shift_share(self.population, self.rates.iloc[:1], self.population, self.rates)

    def test_shift_share_rejects_missing_values(self):
        with self.assertRaises(ValueError):
            shift_share(self.population, self.rates * float('nan'), self.population, self.rates)

    def test_shift_share_aligns_reordered_groups(self):
        result = shift_share(self.population, self.rates.iloc[::-1], self.population, self.rates)
        self.assertAlmostEqual(result.loc['합계', 'total'], 0)

    def test_shift_share_rejects_nullable_missing_values(self):
        with self.assertRaises(ValueError):
            shift_share(self.population, self.rates.astype('Float64') * pd.NA,
                        self.population, self.rates)

    def test_age_standardization_uses_population_weights(self):
        rates = pd.DataFrame([[0.4, 0.7]], columns=self.population.index)
        self.assertAlmostEqual(age_standardized_rate(rates, self.population).iloc[0], 0.6)

    def test_age_standardization_preserves_incomplete_dates(self):
        rates = pd.DataFrame([[0.4, float('nan')]], columns=self.population.index)
        self.assertTrue(age_standardized_rate(rates, self.population).isna().iloc[0])

    def test_age_standardization_rejects_invalid_base_population(self):
        for base in (self.population * 0, self.population * -1, self.population * float('nan'),
                     self.population.astype('Float64') * pd.NA):
            with self.subTest(base=base.tolist()), self.assertRaises(ValueError):
                age_standardized_rate(pd.DataFrame([self.rates]), base)


if __name__ == '__main__':
    unittest.main()
