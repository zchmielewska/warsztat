from cashflower import ModelPointSet
import pandas as pd

mortgage = ModelPointSet(data=pd.DataFrame({
    "loan": [100_000],
    "yearly_interest_rate": [0.1],
    "term": [360],
}))
