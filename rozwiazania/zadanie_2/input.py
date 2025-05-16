from cashflower import ModelPointSet
import pandas as pd

policy = ModelPointSet(data=pd.DataFrame({
    "id": [1, 2],
    "benefit": [2000, 3000],
    "mortality_rate": [0.004, 0.005],
    "remaining_term": [120, 48],
}))


interest_rate = 0.003
