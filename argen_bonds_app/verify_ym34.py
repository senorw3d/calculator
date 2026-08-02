import math
from datetime import datetime

# Simulate the exact JS generateCashFlows and calculateTIR for YM34D
def generate_cash_flows(maturity, coupon_rate, frequency, structure_type):
    mat_parts = [int(x) for x in maturity.split('-')]
    mat_year, mat_month, mat_day = mat_parts[0], mat_parts[1], mat_parts[2]
    freq = frequency
    interval_months = 12 // freq

    cur_y, cur_m = 2025, mat_month
    while cur_y > 2025 or (cur_y == 2025 and cur_m > 1):
        cur_m -= interval_months
        if cur_m <= 0:
            cur_m += 12
            cur_y -= 1

    flow_dates = []
    while cur_y < mat_year or (cur_y == mat_year and cur_m <= mat_month):
        formatted_date = f"{cur_y:04d}-{cur_m:02d}-{mat_day:02d}"
        if formatted_date not in flow_dates:
            flow_dates.append(formatted_date)
        cur_m += interval_months
        if cur_m > 12:
            cur_m -= 12
            cur_y += 1

    if maturity not in flow_dates:
        flow_dates.append(maturity)
    flow_dates.sort()

    residual = 100.0
    period_coupon_pct = coupon_rate / freq
    is_amortizable = (structure_type == "Amortizable")
    amort_years = [mat_year - 2, mat_year - 1, mat_year]

    result = []
    for i, date_str in enumerate(flow_dates):
        y, m, d = [int(x) for x in date_str.split('-')]
        is_last = (i == len(flow_dates) - 1)
        amort = 0.0
        if is_amortizable and m == mat_month and y in amort_years:
            if y == mat_year:
                amort = residual
            else:
                amort = 33.33
        elif not is_amortizable and is_last:
            amort = 100.0
        
        if is_last:
            amort = residual

        cpn_amount = round((residual * period_coupon_pct) / 100.0, 3)
        total_amount = round(amort + cpn_amount, 3)
        next_residual = max(0.0, round(residual - amort, 2))
        
        result.append({
            "date": date_str,
            "amortization": amort,
            "coupon": period_coupon_pct,
            "amount": total_amount,
            "residual": next_residual
        })
        residual = next_residual
    return result

cfs = generate_cash_flows("2034-01-15", 9.50, 2, "Amortizable")
print("Generated Cashflows for YM34D:")
for cf in cfs:
    parts = cf["date"].split('-')
    fmt_date = f"{parts[2]}/{parts[1]}/{parts[0]}"
    print(f"  {fmt_date}: Amort={cf['amortization']}%, Coupon={cf['coupon']}%, Total=${cf['amount']}, Residual={cf['residual']}%")
