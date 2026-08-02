from datetime import datetime

# Real YPF Class XXXIV (YM34D) parameters from Prospectus:
# Issued: Jan 15, 2025
# Maturity: Jan 15, 2034 (9 years)
# Amortization: 33.33% in Jan 2032, 33.33% in Jan 2033, 33.34% in Jan 2034.
# Coupon: 9.50% p.a. (payable semi-annually in Jan and Jul)

settlement_date = datetime(2026, 8, 3) # Today/T+1 in 2026

# Generate all 18 semi-annual cashflow dates from 2025-07-15 to 2034-01-15
cf_dates = []
for year in range(2025, 2034):
    cf_dates.append(f"{year}-07-15")
    cf_dates.append(f"{year+1}-01-15")

coupon_rate = 9.50 # %
freq = 2
coupon_pct = coupon_rate / freq # 4.75% per semester

cash_flows = []
residual = 100.0

for d in cf_dates:
    amort = 0.0
    if d == "2032-01-15":
        amort = 33.33
    elif d == "2033-01-15":
        amort = 33.33
    elif d == "2034-01-15":
        amort = 33.34
        
    coupon_amount = (residual * coupon_pct) / 100.0
    total_amount = amort + coupon_amount
    new_residual = max(0.0, residual - amort)
    
    cash_flows.append({
        "date": d,
        "amortization": amort,
        "coupon": coupon_pct,
        "amount": round(total_amount, 3),
        "residual": round(new_residual, 2)
    })
    residual = new_residual

# Calculate Accrued Interest at 2026-08-03:
# Last coupon was 2026-07-15.
# Days between 2026-07-15 and 2026-08-03 under 30/360: 18 days.
days_accrued = 18
accrued_interest = (coupon_rate / 100.0) * 100.0 * (days_accrued / 360.0) # 0.475

clean_price = 110.60
dirty_price = clean_price + accrued_interest
technical_value = 100.0 + accrued_interest
parity = (dirty_price / technical_value) * 100.0

# Calculate YTM using Newton-Raphson
def get_ytm(price, cfs, settl):
    settl_time = datetime.strptime(settl, "%Y-%m-%d")
    t_years = []
    amounts = []
    for cf in cfs:
        cf_time = datetime.strptime(cf["date"], "%Y-%m-%d")
        diff = (cf_time - settl_time).days
        if diff > 0:
            t_years.append(diff / 365.0)
            amounts.append(cf["amount"])
            
    y = 0.08
    for _ in range(100):
        npv = -price
        dnpv = 0
        for t, amt in zip(t_years, amounts):
            p = t * 2
            df = (1 + y/2)**p
            npv += amt / df
            dnpv -= (amt * p) / (2 * ((1 + y/2)**(p + 1)))
        if abs(npv) < 1e-6:
            break
        y = y - npv / dnpv
    return y * 100

tir = get_ytm(dirty_price, cash_flows, "2026-08-03")

print(f"--- YM34D PROSPECTUS-BASED CALCULATION ---")
print(f"Clean Price: ${clean_price:.2f}")
print(f"Accrued Interest (IC): ${accrued_interest:.2f}")
print(f"Dirty Price: ${dirty_price:.2f}")
print(f"Technical Value: ${technical_value:.2f}")
print(f"Parity: {parity:.2f}%")
print(f"TIR / YTM: {tir:.2f}% p.a.")
print("\nFuture Cash Flows:")
for cf in cash_flows:
    if cf["date"] > "2026-08-03":
        print(f"  {cf['date']}: Amort {cf['amortization']}%, Coupon {cf['coupon']}%, Total ${cf['amount']}, Residual {cf['residual']}%")
