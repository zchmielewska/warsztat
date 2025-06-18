from cashflower import variable

from input import policy, interest_rate
from settings import settings


@variable()
def survival_rate(t):
    if t == 0:
        return 1
    else:
        q = policy.get("mortality_rate")
        return survival_rate(t - 1) * (1 - q)


@variable()
def expected_benefit(t):
    if t == 0 or t > policy.get("term"):
        return 0
    else:
        B = policy.get("sum_assured")
        q = policy.get("mortality_rate")
        return B * survival_rate(t-1) * q


@variable()
def net_single_premium(t):
    if t == settings["T_MAX_CALCULATION"]:
        return expected_benefit(t)
    else:
        v = 1 / (1 + interest_rate)
        return expected_benefit(t) + v * net_single_premium(t+1)
