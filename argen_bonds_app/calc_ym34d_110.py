import math
from datetime import datetime

coupon_rate = 8.75
frequency = 2
last_coupon_date = datetime(2026, 6, 30)
settlement_date = datetime(2026, 8, 3) # T+1
maturity_date = datetime(2026, 12, 31)

# Accrued interest (30/360)
d1 = min(30, 30)
d2 = 3
days_accrued = (2026-2026)*360 + (8-6)*30 + (d2 - d1) # 33 days
accrued_interest = (coupon_rate / 100.0) * 100.0 * (days_accrued / 360.0)

# Case 1: Clean Price = 110.60
clean_price_1 = 110.60
dirty_price_1 = clean_price_1 + accrued_interest
technical_value = 100.0 + accrued_interest
parity_1 = (dirty_price_1 / technical_value) * 100.0

cf_date = datetime(2026, 12, 31)
diff_days = (cf_date - settlement_date).days
t_years = diff_days / 365.0
cf_amount = 104.375

y_semi_1 = (cf_amount / dirty_price_1) ** (1.0 / (t_years * 2)) - 1.0
tir_1 = y_semi_1 * 2 * 100.0

# Case 2: Dirty Price = 110.60
dirty_price_2 = 110.60
clean_price_2 = dirty_price_2 - accrued_interest
parity_2 = (dirty_price_2 / technical_value) * 100.0
y_semi_2 = (cf_amount / dirty_price_2) ** (1.0 / (t_years * 2)) - 1.0
tir_2 = y_semi_2 * 2 * 100.0

print(f"CASE 1: Clean Price = ${clean_price_1:.2f}")
print(f"  Dirty Price: ${dirty_price_1:.2f}")
print(f"  Parity: {parity_1:.2f}%")
print(f"  TIR: {tir_1:.2f}%\n")

print(f"CASE 2: Dirty Price = ${dirty_price_2:.2f}")
print(f"  Clean Price: ${clean_price_2:.2f}")
print(f"  Parity: {parity_2:.2f}%")
print(f"  TIR: {tir_2:.2f}%")
