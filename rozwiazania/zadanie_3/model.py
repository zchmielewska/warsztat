from cashflower import variable
from input import mortgage


@variable()
def interest_rate():
    return mortgage.get("yearly_interest_rate") / 12


@variable()
def payment(t):
    if t > mortgage.get("term"):
        return 0

    L = mortgage.get("loan")
    j = interest_rate()
    n = mortgage.get("term")
    v = 1 / (1 + j)
    return L / ((1 - v**n) / j)


@variable()
def interest(t):
    if t == 0:
        return 0
    return balance(t-1) * interest_rate()


@variable()
def principal(t):
    return payment(t) - interest(t)


@variable()
def balance(t):
    if t == 0:
        return mortgage.get("loan")
    return balance(t - 1) - principal(t)

