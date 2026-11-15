"""KPI-számítás tesztjei – hálózat nélkül, kézzel megadott adatokkal.

Futtatás a projekt gyökeréből:  python -m unittest discover -s tests -t .
"""

import math
import unittest

import pandas as pd

from src.indicators import calculate_indicators


def make_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "year": [2020, 2021, 2023],
            "total_population": [1000, 1000, 1000],
            "population_0_14": [200, 0, 100],
            "population_15_64": [600, 660, 650],
            "population_65_plus": [200, 340, 250],
            "gdp": [10.0, 11.0, 12.0],
        }
    )


class TestIndicators(unittest.TestCase):
    def test_ageing_index(self):
        result = calculate_indicators(make_df())
        self.assertAlmostEqual(result.loc[0, "ageing_index"], 100.0)  # 200 / 200 * 100
        self.assertAlmostEqual(result.loc[2, "ageing_index"], 250.0)  # 250 / 100 * 100

    def test_working_age_ratio(self):
        result = calculate_indicators(make_df())
        self.assertAlmostEqual(result.loc[0, "working_age_ratio"], 60.0)
        self.assertAlmostEqual(result.loc[1, "working_age_ratio"], 66.0)

    def test_division_by_zero_gives_nan(self):
        result = calculate_indicators(make_df())
        self.assertTrue(math.isnan(result.loc[1, "ageing_index"]))  # 0–14 = 0

    def test_missing_input_gives_nan(self):
        df = make_df()
        df.loc[0, "population_65_plus"] = None
        result = calculate_indicators(df)
        self.assertTrue(math.isnan(result.loc[0, "elderly_ratio"]))

    def test_yoy_only_for_consecutive_years(self):
        result = calculate_indicators(make_df())
        self.assertAlmostEqual(result.loc[1, "population_15_64_yoy_pct"], 10.0)  # 2020 -> 2021
        self.assertTrue(math.isnan(result.loc[2, "population_15_64_yoy_pct"]))   # 2021 -> 2023: rés

    def test_input_not_modified(self):
        df = make_df()
        original = df.copy()
        calculate_indicators(df)
        pd.testing.assert_frame_equal(df, original)


if __name__ == "__main__":
    unittest.main()
