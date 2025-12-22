
def apply_tax(profit, brackets):
    tax = 0
    for limit, rate in brackets:
        if profit > limit:
            tax += (profit - limit) * rate
            profit = limit
    return tax

def calculate(lump, monthly, years, rate_min, rate_max, fee_rate, tax_rules):
    invested = lump + (monthly * 12 * years)

    min_val = invested * ((1 + rate_min) ** years)
    max_val = invested * ((1 + rate_max) ** years)

    fees = monthly * fee_rate * 12 * years

    profit_min = min_val - invested
    profit_max = max_val - invested

    tax_min = apply_tax(profit_min, tax_rules)
    tax_max = apply_tax(profit_max, tax_rules)

    return {
        "min": round(min_val, 2),
        "max": round(max_val, 2),
        "profit_min": round(profit_min, 2),
        "profit_max": round(profit_max, 2),
        "fees": round(fees, 2),
        "tax_min": round(tax_min, 2),
        "tax_max": round(tax_max, 2)
    }
