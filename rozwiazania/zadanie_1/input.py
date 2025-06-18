from cashflower import ModelPointSet
import pandas as pd

policy = ModelPointSet(data=pd.DataFrame({
    "sum_assured": [100_000],
    "mortality_rate": [0.03],
    "term": [36],
}))


interest_rate = 0.005
