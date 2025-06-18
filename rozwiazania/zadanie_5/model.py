from cashflower import variable

from input import policy, interest_rate, stochastic_scenarios


@variable()
def investment_return(t, stoch):
    if t == 0 or t > policy.get("term"):
        return 0
    return stochastic_scenarios.loc[(stoch, t), "rate"]


@variable()
def fund_value(t, stoch):
    if t == 0:
        return policy.get("premium")
    elif t < policy.get("term"):
        return fund_value(t - 1, stoch) * (1 + investment_return(t, stoch)) + policy.get("premium")
    else:
        return fund_value(t - 1, stoch) * (1 + investment_return(t, stoch))


@variable()
def shortfall(t, stoch):
    if t == policy.get("term"):
        shortfall = max(0, policy.get("guaranteed_benefit") - fund_value(t, stoch))
        return shortfall
    return 0


@variable()
def tvog(t, stoch):
    if t == policy.get("term"):
        return shortfall(t, stoch)
    return tvog(t+1, stoch) * (1 / (1 + interest_rate))
