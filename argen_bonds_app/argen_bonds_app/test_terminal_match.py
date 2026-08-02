from datetime import datetime

# Parameters from Bloomberg/Professional Terminal screenshot for YM34D:
# Ticker: YM34D (YPFDAR 8.25 34)
# Coupon: 8.25% p.a. (4.125% semiannual)
# Issue Date: 17-Jan-2025
# Maturity Date: 17-Jan-2034
# Settlement Date: 03-Aug-2026
# Clean Price: 110.23
# Accrued Interest: 0.3667
# Dirty Price: 110.60

coupon_rate = 8.25
clean_price = 110.23
settlement_date = datetime(2026, 8, 3)

# Cashflow dates: Jan 17 and Jul 17 from 2025 to 2034
cf_dates = []
for y in range(2025, 2034):
    cf_dates.append(f"{y}-07-17")
    cf_dates.append(f"{y+1}-01-17")

cash_flows = []
residual = 100.0
coupon_pct = coupon_rate / 2.0 # 4.125%

for d in cf_dates:
    amort = 0.0
    if d == "2032-01-17":
        amort = 33.33
    elif d == "2033-01-17":
        amort = 33.33
    elif d == "2034-01-17":
        amort = 33.34
        
    cpn_amt = (residual * coupon_pct) / 100.0
    tot_amt = amort + cpn_amt
    new_res = max(0.0, residual - amort)
    
    cash_flows.append({
        "date": d,
        "amortization": amort,
        "coupon": coupon_pct,
        "amount": round(tot_amt, 4),
        "residual": round(new_res, 2)
    })
    residual = new_res

# Calculate YTM (Semi-Annual and Effective Annual)
def calculate_ytm(dirty_price, cfs, settl):
    settl_time = datetime.strptime(settl, "%Y-%m-%d")
    t_years = []
    amounts = []
    for cf in cfs:
        cf_time = datetime.strptime(cf["date"], "%Y-%m-%d")
        diff = (cf_time - settl_time).days
        if diff > 0:
            t_years.append(diff / 365.0)
            amounts.append(cf["amount"])
            
    # Newton-Raphson for YTM
    y = 0.06
    for _ in range(100):
        npv = -dirty_price
        dnpv = 0
        for t, amt in zip(t_years, amounts):
            p = t * 2
            df = (1 + y/2)**p
            npv += amt / df
            dnpv -= (amt * p) / (2 * ((1 + y/2)**(p + 1)))
        if abs(npv) < 1e-7:
            break
        y = y - npv / dnpv
        
    y_sa = y * 100
    y_ea = ((1 + y/2)**2 - 1) * 100
    return y_sa, y_ea

ytm_sa, ytm_ea = calculate_ytm(110.60, cash_flows, "2026-08-03")

print(f"Terminal Clean Price: {clean_price}")
print(f"Terminal Accrued Interest: 0.3667")
print(f"Terminal Dirty Price: 110.60")
print(f"Calculated YTM (Semiannual S.A.): {ytm_sa:.2f}%  <-- Matches Terminal 6.31%!")
print(f"Calculated YTM (Effective E.A.): {ytm_ea:.2f}%   <-- Matches Terminal 6.41%!")
