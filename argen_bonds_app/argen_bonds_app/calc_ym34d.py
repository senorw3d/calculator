import math
from datetime import datetime

# YM34D parameters
clean_price = 98.50
coupon_rate = 8.75
frequency = 2
last_coupon_date = datetime(2026, 6, 30)
settlement_date = datetime(2026, 8, 3) # T+1
maturity_date = datetime(2026, 12, 31)

# Accrued interest (30/360)
# Days between 2026-06-30 and 2026-08-03: (0)*360 + (8-6)*30 + (3-30) = 60 - 27 = 33 days (30/360)
d1 = min(30, 30)
d2 = 3
days_accrued = (2026-2026)*360 + (8-6)*30 + (d2 - d1) # 33 days
accrued_interest = (coupon_rate / 100.0) * 100.0 * (days_accrued / 360.0)

dirty_price = clean_price + accrued_interest
technical_value = 100.0 + accrued_interest
parity = (dirty_price / technical_value) * 100.0

# Cash flow on 2026-12-31: Amort 100 + Coupon 4.375 = 104.375
cf_date = datetime(2026, 12, 31)
diff_days = (cf_date - settlement_date).days
t_years = diff_days / 365.0

# Solve YTM where dirty_price = 104.375 / (1 + y/2)^(t_years * 2)
# 1 + y/2 = (104.375 / dirty_price) ^ (1 / (t_years * 2))
cf_amount = 104.375
y_semi = (cf_amount / dirty_price) ** (1.0 / (t_years * 2)) - 1.0
tir = y_semi * 2 * 100.0

print(f"Ticker: YM34D (YPF S.A.)")
print(f"Fecha de Liquidacion (T+1): {settlement_date.strftime('%d/%m/%Y')}")
print(f"Precio Limpio (Clean Price): ${clean_price:.2f}")
print(f"Interes Corrido (IC): ${accrued_interest:.2f}")
print(f"Precio Sucio (Dirty Price): ${dirty_price:.2f}")
print(f"Valor Tecnico: ${technical_value:.2f}")
print(f"Paridad: {parity:.2f}%")
print(f"TIR / YTM Anualizada: {tir:.2f}%")
print(f"Vencimiento: {maturity_date.strftime('%d/%m/%Y')} (dias al vencimiento: {diff_days}d / {t_years:.2f} anos)")
