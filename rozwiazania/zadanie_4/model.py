from cashflower import variable

from input import runplan, bond, base_interest_rate
from settings import settings


@variable()
def t_end():
    months_elapsed = (runplan.get("valuation_year") - bond.get("issue_year")) * 12 + (runplan.get("valuation_month") - bond.get("issue_month"))
    return bond.get("term") - months_elapsed


@variable()
def calendar_month(t):
    if t == 0:
        return runplan.get("valuation_month")
    elif calendar_month(t - 1) == 12:
        return 1
    else:
        return calendar_month(t - 1) + 1


@variable()
def coupon(t):
    if calendar_month(t) == bond.get("issue_month") and t <= t_end():
        return bond.get("nominal") * bond.get("coupon_rate")
    else:
        return 0


@variable()
def nominal_value(t):
    if t == t_end():
        return bond.get("nominal")
    return 0


@variable()
def interest_rate():
    return base_interest_rate * (1 + runplan.get("stress"))


@variable()
def present_value(t):
    if t == settings["T_MAX_CALCULATION"]:
        return coupon(t) + nominal_value(t)
    v = 1 / (1 + interest_rate())
    return coupon(t) + nominal_value(t) + v * present_value(t+1)
