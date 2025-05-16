from cashflower import ModelPointSet, Runplan
import pandas as pd

runplan = Runplan(data=pd.DataFrame({
    "version": [1, 2, 3],
    "valuation_year": [2024, 2024, 2024],
    "valuation_month": [12, 12, 12],
    "stress": [0, 0.1, -0.1]
}))


bond = ModelPointSet(data=pd.DataFrame({
    "nominal": [1000],
    "coupon_rate": [0.03],
    "term": [120],
    "issue_year": [2024],
    "issue_month": [6],
}))

base_interest_rate = 0.002
