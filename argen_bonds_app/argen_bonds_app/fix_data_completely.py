import re

# Base maturity year and month/day per ticker prefix
MATURITY_SPEC = {
    # YPF
    'YM34': ('2026-12-31', 8.75, 98.50),
    'YM35': ('2027-07-28', 9.00, 97.20),
    'YM37': ('2027-02-12', 8.50, 99.10),
    'YM38': ('2027-09-30', 8.50, 98.80),
    'YM39': ('2029-03-23', 9.00, 96.50),
    'YM40': ('2027-07-15', 8.75, 98.00),
    'YM41': ('2028-11-15', 9.00, 95.80),
    'YM42': ('2027-09-30', 9.00, 97.50),
    'YM43': ('2031-06-30', 9.50, 92.40),
    'YFCG': ('2027-02-14', 7.00, 99.50),
    'YFCI': ('2027-03-05', 7.50, 99.00),
    'YFCJ': ('2027-06-30', 7.50, 98.80),
    'YFCK': ('2027-04-15', 8.00, 98.20),
    'YFCL': ('2027-09-15', 8.00, 98.00),
    'YFCM': ('2028-03-15', 8.25, 97.60),
    'YFCN': ('2028-09-15', 8.50, 97.10),
    'YFCO': ('2029-11-30', 8.75, 95.00),
    'YMCI': ('2026-12-15', 7.00, 100.20),
    'YMCJ': ('2027-04-30', 7.50, 99.10),
    'YMCX': ('2027-10-15', 8.00, 98.30),
    'YMCY': ('2028-06-30', 8.50, 96.90),
    'YMCZ': ('2029-09-30', 9.00, 94.50),
    # Telecom
    'TLCM': ('2027-07-18', 8.00, 99.80),
    'TLCO': ('2027-08-06', 8.00, 99.50),
    'TLCP': ('2027-11-15', 8.50, 98.90),
    'TLCT': ('2028-07-18', 9.50, 96.20),
    'TLCU': ('2029-04-10', 9.50, 95.10),
    'TLCV': ('2031-03-15', 10.00, 91.50),
    'TLCW': ('2032-12-15', 10.25, 89.90),
    'T662': ('2026-11-20', 6.50, 100.10),
    'T672': ('2027-03-15', 7.00, 99.40),
    'LCMZ': ('2027-07-18', 8.00, 99.00),
    # IRSA
    'IRCF': ('2026-12-22', 7.00, 100.50),
    'IRCN': ('2027-03-25', 7.75, 99.20),
    'IRCO': ('2028-06-30', 8.75, 97.80),
    'IRCP': ('2028-09-15', 8.75, 97.20),
    # Pan American Energy
    'PN35': ('2026-12-30', 7.00, 100.10),
    'PN36': ('2027-01-20', 7.50, 99.60),
    'PN38': ('2027-05-15', 7.75, 99.00),
    'PN41': ('2027-11-30', 8.00, 98.40),
    'PN42': ('2028-06-15', 8.50, 97.00),
    'PN43': ('2029-02-28', 8.75, 95.80),
    'PNXC': ('2027-08-31', 8.00, 98.20),
    'PECM': ('2027-10-31', 8.25, 98.00),
    'PECN': ('2028-12-15', 8.50, 96.50),
    # Arcor
    'ARC1': ('2027-07-06', 6.00, 101.20),
    # AA2000
    'AERB': ('2031-02-01', 8.50, 93.80),
    # Banks
    'BACG': ('2027-05-15', 7.50, 99.30),
    'BACH': ('2026-11-07', 8.00, 99.90),
    'SBC1': ('2026-11-10', 7.25, 100.00),
    'SBC2': ('2027-01-18', 7.75, 99.10),
    'SBC3': ('2027-10-05', 8.25, 98.00),
    'BF37': ('2026-12-15', 7.50, 100.10),
    'BF39': ('2027-12-01', 8.00, 98.70),
    'GPS1': ('2027-06-30', 8.00, 98.50),
    'RCCR': ('2027-02-28', 8.50, 97.90),
    'RUCD': ('2026-11-15', 7.50, 99.80),
    'RUCE': ('2027-04-15', 8.00, 98.60),
    # Central Puerto
    'CP37': ('2026-12-08', 7.50, 100.00),
    'CP38': ('2027-06-14', 8.00, 99.20),
    'CP40': ('2028-03-20', 8.50, 97.50),
    # Cresud
    'CS45': ('2026-12-03', 7.00, 100.10),
    'CS47': ('2027-02-26', 7.50, 99.40),
    'CS48': ('2027-08-11', 8.00, 98.60),
    'CS49': ('2028-02-21', 8.25, 97.90),
    'CS50': ('2028-11-03', 8.50, 97.00),
    'CS51': ('2029-05-12', 8.75, 96.10),
    'CS52': ('2029-12-20', 9.00, 94.80),
    # Edenor
    'DNC3': ('2026-11-24', 9.75, 94.50),
    'DNC5': ('2027-02-20', 9.75, 94.00),
    'DNC7': ('2030-05-12', 9.75, 90.20),
    'DNC9': ('2027-10-15', 9.50, 95.00),
    'DNCA': ('2028-04-20', 9.75, 93.20),
    'DNCB': ('2029-09-30', 9.75, 91.80),
    # Gen. Mediterranea
    'MGCE': ('2026-12-15', 9.25, 95.00),
    'MGCM': ('2027-03-10', 9.50, 94.20),
    'MGCN': ('2027-09-20', 9.50, 93.80),
    'MGCO': ('2028-04-15', 9.75, 92.50),
    'MGCQ': ('2028-11-01', 9.75, 92.00),
    'MGCR': ('2029-05-30', 10.00, 90.50),
    'MGCT': ('2030-01-15', 10.25, 88.00),
    # Vista Energy / VBC
    'VSCP': ('2026-12-10', 7.50, 100.20),
    'VSCQ': ('2027-03-20', 8.00, 99.40),
    'VSCR': ('2027-07-04', 8.50, 98.60),
    'VSCU': ('2028-03-18', 8.50, 98.00),
    'VSCV': ('2028-10-12', 8.75, 97.10),
    'VSCX': ('2029-06-30', 9.00, 95.50),
    'VSCZ': ('2030-04-15', 9.25, 93.20),
    'VBC1': ('2027-12-05', 8.00, 98.80),
    'VBC2': ('2027-12-05', 8.50, 97.90),
    # Tecpetrol
    'TTC8': ('2026-12-18', 6.75, 100.30),
    'TTC9': ('2027-01-15', 7.25, 99.80),
    'TTCA': ('2027-08-22', 7.75, 99.10),
    'TTCB': ('2028-04-10', 8.00, 98.20),
    'TTCD': ('2028-11-15', 8.25, 97.60),
    'TTCE': ('2029-05-21', 8.50, 96.50),
    # TGS
    'TSC3': ('2026-11-02', 6.75, 100.40),
    'TSC4': ('2031-05-02', 8.50, 94.00),
    # Loma Negra
    'LOC5': ('2026-10-10', 7.50, 99.50),
    'LOC6': ('2029-01-23', 8.50, 96.00),
    'LMS7': ('2027-04-15', 7.75, 98.80),
    'LMS8': ('2028-09-20', 8.25, 97.30),
    # Mastellone
    'MCC1': ('2026-11-15', 8.00, 99.00),
    'MCC2': ('2027-06-30', 8.50, 97.80),
    'MCC3': ('2028-11-20', 9.00, 95.50),
    'MTC2': ('2027-06-30', 8.50, 97.80),
    # Mirgor
    'MR43': ('2026-12-15', 8.50, 98.50),
    'MR44': ('2027-05-10', 8.75, 97.90),
    'MR46': ('2028-01-25', 9.00, 96.80),
    'MR47': ('2028-10-10', 9.25, 95.40),
    # Pluspetrol
    'PLC1': ('2026-11-15', 7.00, 100.00),
    'PLC2': ('2027-03-01', 7.50, 99.20),
    'PLC3': ('2027-05-20', 7.75, 98.90),
    'PLC4': ('2027-12-10', 8.00, 98.10),
    'PLC5': ('2028-08-15', 8.25, 97.40),
    'PLC6': ('2029-03-20', 8.75, 95.90),
    'PLC7': ('2030-01-10', 9.00, 94.00),
    # PCR
    'PQCR': ('2026-11-15', 8.00, 99.10),
    'PQCS': ('2028-07-20', 8.75, 97.00),
    # Rizobacter
    'RZBC': ('2027-06-14', 8.25, 98.30),
    # San Miguel
    'SNEB': ('2026-11-10', 9.00, 96.50),
    'SNSB': ('2027-10-14', 9.50, 95.00),
    'SNSD': ('2028-08-20', 9.75, 93.80),
    # 360 Energy
    'GYC4': ('2026-11-15', 8.50, 98.00),
    'GYC5': ('2028-02-28', 9.00, 96.00),
    # MSU Energy
    'EAC4': ('2026-12-05', 9.00, 96.80),
    'MSSF': ('2028-06-15', 9.50, 94.50),
    'MSSG': ('2028-06-15', 9.50, 94.50),
    # Genneia
    'GN49': ('2028-09-02', 8.75, 96.80),
    # Oiltanking
    'OT41': ('2026-11-10', 7.50, 99.80),
    'OT42': ('2027-04-25', 8.00, 98.50),
    'OTS2': ('2028-01-15', 8.50, 97.20),
    'OTS5': ('2029-05-20', 9.00, 95.00),
    # Capex
    'CAC5': ('2026-10-25', 8.50, 98.70),
    'CACB': ('2029-08-25', 9.25, 94.20),
    'CACD': ('2029-08-25', 9.25, 94.20),
    # Oldelval
    'OLC5': ('2026-12-10', 7.75, 99.40),
    'OLC6': ('2027-11-20', 8.25, 98.00),
    'OLC7': ('2029-04-15', 8.75, 95.50),
    # Ledesma
    'LDCG': ('2027-07-30', 8.00, 98.50),
    # Holcim
    'HJCF': ('2026-11-30', 7.50, 99.60),
    'HJCI': ('2027-08-20', 8.00, 98.30),
    # CIESA
    'CICA': ('2027-02-15', 8.50, 97.80),
    'CICB': ('2027-02-15', 8.50, 97.80),
    # Edesur
    'EMC1': ('2026-10-15', 9.00, 96.00),
    # Albanesi
    'BYCV': ('2027-05-30', 9.50, 94.80),
    # DESA
    'DEC2': ('2027-08-20', 9.25, 95.20),
    'DEC4': ('2027-08-20', 9.25, 95.20),
    # Havanna
    'HVS1': ('2026-12-05', 8.00, 99.00),
    # SCP
    'LQC1': ('2027-04-10', 8.50, 97.50),
    # Molinos Agro
    'LUC5': ('2027-09-15', 8.00, 98.40),
    # TGLT
    'OZC3': ('2026-11-30', 9.50, 93.50),
    # Raghsa
    'RC1C': ('2028-03-15', 8.50, 97.10),
    'RC2C': ('2031-05-20', 9.00, 92.00),
    # Banco Prov Cordoba
    'RCCR': ('2027-02-28', 8.50, 97.90),
    # Banco Entre Rios
    'RUCD': ('2026-11-15', 7.50, 99.80),
    'RUCE': ('2027-04-15', 8.00, 98.60),
    # RAVA
    'RVS1': ('2026-11-20', 8.00, 99.00),
    # Ternium
    'SIC1': ('2027-04-30', 7.50, 99.20),
    'SIC2': ('2027-04-30', 7.50, 99.20),
    # Werthein
    'WBS3': ('2027-10-15', 8.50, 97.80),
    # Xmarts
    'XMC1': ('2026-11-20', 8.50, 98.20),
    # Pampa
    'ZZC1': ('2028-01-24', 8.25, 97.50),
    # Ausol
    'PZCG': '2027-11-30'
}

def generate_cashflows(maturity_str, coupon_rate, is_amortizable):
    # Base start date for upcoming payments
    # Assuming settlement in late 2026, generate 2-8 future semi-annual dates up to maturity
    mat_year = int(maturity_str.split('-')[0])
    mat_month = maturity_str.split('-')[1]
    mat_day = maturity_str.split('-')[2]
    
    start_year = 2026
    start_month = 12
    
    cfs = []
    current_year = start_year
    current_month = start_month
    
    # Generate dates at 6-month intervals until we reach or pass mat_year
    dates = []
    while current_year < mat_year or (current_year == mat_year and current_month <= int(mat_month)):
        d_str = f"{current_year}-{current_month:02d}-{mat_day}"
        dates.append(d_str)
        current_month += 6
        if current_month > 12:
            current_month -= 12
            current_year += 1
            
    if not dates or dates[-1] != maturity_str:
        dates.append(maturity_str)

    # De-duplicate while preserving order
    unique_dates = []
    for d in dates:
        if d not in unique_dates:
            unique_dates.append(d)
    dates = unique_dates
    
    num_payments = len(dates)
    
    # Calculate cashflows
    residual = 100.0
    half_coupon = coupon_rate / 2.0
    
    for i, d in enumerate(dates):
        is_last = (i == num_payments - 1)
        
        if is_last:
            amort = residual
        elif is_amortizable and i >= max(0, num_payments - 3):
            # Amortize over last 3 payments
            amort = round(100.0 / min(3, num_payments), 2)
        else:
            amort = 0.0
            
        coupon_val = round((residual * half_coupon) / 100.0, 3)
        total_amount = round(amort + coupon_val, 3)
        new_residual = round(max(0.0, residual - amort), 2)
        
        cfs.append(f'{{ date: "{d}", amortization: {amort}, coupon: {half_coupon:.3f}, amount: {total_amount:.3f}, residual: {new_residual} }}')
        residual = new_residual
        
    return "[\n        " + ",\n        ".join(cfs) + "\n      ]"

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# We will parse each bond block and update maturity, couponRate, cleanPrice, cashFlows
def process_bond_block(match):
    block = match.group(0)
    
    # Extract ticker
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if not t_match:
        return block
    ticker = t_match.group(1)
    
    # Find matching spec
    mat_date = "2028-06-30"
    c_rate = 8.50
    c_price = 98.00
    
    for key in sorted(MATURITY_SPEC.keys(), key=len, reverse=True):
        if ticker.startswith(key):
            spec = MATURITY_SPEC[key]
            if isinstance(spec, tuple):
                mat_date, c_rate, c_price = spec
            else:
                mat_date = spec
            break
            
    is_amort = "Amortizable" in block
    
    # Generate new cashflows
    cf_js = generate_cashflows(mat_date, c_rate, is_amort)
    
    # Update block
    block = re.sub(r'maturity:\s*"[^"]+"', f'maturity: "{mat_date}"', block)
    block = re.sub(r'couponRate:\s*[\d\.]+', f'couponRate: {c_rate}', block)
    block = re.sub(r'cleanPrice:\s*[\d\.]+', f'cleanPrice: {c_price}', block)
    block = re.sub(r'cashFlows:\s*\[.*?\]', f'cashFlows: {cf_js}', block, flags=re.DOTALL)
    
    return block

pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content = re.sub(pattern, process_bond_block, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Successfully regenerated all bond maturities, coupon rates, prices, and cash flows.")
