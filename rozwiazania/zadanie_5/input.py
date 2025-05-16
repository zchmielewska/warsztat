from cashflower import ModelPointSet
import pandas as pd
import numpy as np

policy = ModelPointSet(data=pd.DataFrame({
    "premium": [19000],
    "guaranteed_benefit": [100_000],
    "term": [5],
}))

np.random.seed(123)
n_scenarios = 1000
n_years = 5

stochastic_scenarios = pd.DataFrame({
    "scenario": np.repeat(np.arange(1, n_scenarios + 1), n_years),
    "t": list(range(1, n_years + 1)) * n_scenarios,
    "rate": np.random.normal(loc=0.04, scale=0.10, size=n_scenarios * n_years),
}).set_index(["scenario", "t"])

interest_rate = 0.03
