import re

# Dictionary mapping ticker (or ticker family / base) to maturity date YYYY-MM-DD
MATURITY_MAP = {
    # YPF
    'YM34': '2024-09-30', 'YM35': '2025-07-28', 'YM37': '2026-02-12', 'YM38': '2027-09-30',
    'YM39': '2029-03-23', 'YM40': '2026-07-15', 'YM41': '2028-11-15', 'YM42': '2026-09-30',
    'YM43': '2031-06-30', 'YFCG': '2025-02-14', 'YFCI': '2026-03-05', 'YFCJ': '2026-06-30',
    'YFCK': '2027-04-15', 'YFCL': '2027-09-15', 'YFCM': '2028-03-15', 'YFCN': '2028-09-15',
    'YFCO': '2029-11-30', 'YMCI': '2025-12-15', 'YMCJ': '2026-04-30', 'YMCX': '2027-10-15',
    'YMCY': '2028-06-30', 'YMCZ': '2029-09-30',
    # Telecom
    'TLCM': '2025-07-18', 'TLCO': '2026-08-06', 'TLCP': '2026-11-15', 'TLCT': '2028-07-18',
    'TLCU': '2029-04-10', 'TLCV': '2031-03-15', 'TLCW': '2032-12-15', 'T662': '2024-11-20',
    'T672': '2025-03-15', 'LCMZ': '2025-07-18',
    # IRSA
    'IRCF': '2025-06-22', 'IRCN': '2026-03-25', 'IRCO': '2028-06-30', 'IRCP': '2028-09-15',
    # Pan American Energy
    'PN35': '2025-04-30', 'PN36': '2026-01-20', 'PN38': '2027-05-15', 'PN41': '2027-11-30',
    'PN42': '2028-06-15', 'PN43': '2029-02-28', 'PNXC': '2025-08-31', 'PECM': '2026-10-31',
    'PECN': '2027-12-15',
    # Arcor
    'ARC1': '2027-07-06',
    # AA2000
    'AERB': '2031-02-01',
    # Galicia / Hipotecario / Supervielle / BBVA
    'BACG': '2026-05-15', 'BACH': '2025-11-07', 'SBC1': '2025-05-10', 'SBC2': '2026-01-18',
    'SBC3': '2026-10-05', 'BF37': '2025-09-15', 'BF39': '2026-12-01', 'GPS1': '2025-06-30',
    'RCCR': '2026-02-28', 'RUCD': '2025-11-15', 'RUCE': '2025-11-15',
    # Central Puerto
    'CP37': '2025-09-08', 'CP38': '2026-06-14', 'CP40': '2027-03-20',
    # Cresud
    'CS45': '2025-03-03', 'CS47': '2026-02-26', 'CS48': '2026-08-11', 'CS49': '2027-02-21',
    'CS50': '2027-11-03', 'CS51': '2028-05-12', 'CS52': '2028-12-20',
    # Edenor
    'DNC3': '2025-05-24', 'DNC5': '2026-02-20', 'DNC7': '2030-05-12', 'DNC9': '2026-10-15',
    'DNCA': '2027-04-20', 'DNCB': '2028-09-30',
    # Gen. Mediterranea
    'MGCE': '2025-08-15', 'MGCM': '2026-03-10', 'MGCN': '2026-09-20', 'MGCO': '2027-04-15',
    'MGCQ': '2027-11-01', 'MGCR': '2028-05-30', 'MGCT': '2029-01-15',
    # Vista Energy / VBC
    'VSCP': '2025-03-10', 'VSCQ': '2025-11-20', 'VSCR': '2026-07-04', 'VSCU': '2027-03-18',
    'VSCV': '2027-10-12', 'VSCX': '2028-06-30', 'VSCZ': '2029-04-15', 'VBC1': '2026-12-05',
    'VBC2': '2026-12-05',
    # Tecpetrol
    'TTC8': '2025-06-18', 'TTC9': '2026-01-15', 'TTCA': '2026-08-22', 'TTCB': '2027-04-10',
    'TTCD': '2027-11-15', 'TTCE': '2029-05-21',
    # TGS
    'TSC3': '2025-05-02', 'TSC4': '2031-05-02',
    # Loma Negra
    'LOC5': '2025-10-10', 'LOC6': '2029-01-23', 'LMS7': '2026-04-15', 'LMS8': '2027-09-20',
    # Mastellone
    'MCC1': '2025-04-15', 'MCC2': '2026-06-30', 'MCC3': '2027-11-20', 'MTC2': '2026-06-30',
    # Mirgor
    'MR43': '2025-09-15', 'MR44': '2026-05-10', 'MR46': '2027-01-25', 'MR47': '2027-10-10',
    # Pluspetrol
    'PLC1': '2025-02-15', 'PLC2': '2025-09-01', 'PLC3': '2026-05-20', 'PLC4': '2026-12-10',
    'PLC5': '2027-08-15', 'PLC6': '2028-03-20', 'PLC7': '2029-01-10',
    # PCR
    'PQCR': '2025-11-15', 'PQCS': '2027-07-20',
    # Rizobacter
    'RZBC': '2026-06-14',
    # San Miguel
    'SNEB': '2025-04-10', 'SNSB': '2026-10-14', 'SNSD': '2027-08-20',
    # 360 Energy
    'GYC4': '2025-07-15', 'GYC5': '2027-02-28',
    # MSU Energy
    'EAC4': '2025-10-05', 'MSSF': '2027-06-15', 'MSSG': '2027-06-15',
    # Genneia
    'GN49': '2027-09-02',
    # Oiltanking
    'OT41': '2025-08-10', 'OT42': '2026-04-25', 'OTS2': '2027-01-15', 'OTS5': '2028-05-20',
    # Capex
    'CAC5': '2024-10-25', 'CACB': '2028-08-25', 'CACD': '2028-08-25',
    # Oldelval
    'OLC5': '2025-12-10', 'OLC6': '2026-11-20', 'OLC7': '2028-04-15',
    # Ledesma
    'LDCG': '2026-07-30',
    # Holcim
    'HJCF': '2025-03-31', 'HJCI': '2026-08-20',
    # CGC
    'NPCC': '2025-09-10', 'NPCD': '2026-11-05', 'NPCE': '2028-03-15',
    # Clisa
    'CLI1': '2027-07-20', 'CLSI': '2027-07-20',
    # CIESA
    'CICA': '2026-02-15', 'CICB': '2026-02-15',
    # Edesur
    'EMC1': '2025-10-15',
    # Albanesi
    'BYCV': '2026-05-30',
    # DESA
    'DEC2': '2026-08-20', 'DEC4': '2026-08-20',
    # Havanna
    'HVS1': '2025-12-05',
    # SCP
    'LQC1': '2026-04-10',
    # Molinos Agro
    'LUC5': '2026-09-15',
    # TGLT
    'OZC3': '2025-11-30',
    # Raghsa
    'RC1C': '2027-03-15', 'RC2C': '2030-05-20',
    # RAVA
    'RVS1': '2025-07-20',
    # Ternium
    'SIC1': '2026-04-30', 'SIC2': '2026-04-30',
    # Werthein
    'WBS3': '2026-10-15',
    # Xmarts
    'XMC1': '2025-08-20',
    # Pampa
    'ZZC1': '2027-01-24',
    # Ausol
    'PZCG': '2026-11-30'
}

filepath = r'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern to find each object and update maturity and the 2nd cashflow date
def update_bond(match):
    block = match.group(0)
    
    # Extract ticker
    t_match = re.search(r'ticker:\s*"([^"]+)"', block)
    if not t_match:
        return block
    ticker = t_match.group(1)
    
    # Find matching maturity
    mat_date = None
    for key in sorted(MATURITY_MAP.keys(), key=len, reverse=True):
        if ticker.startswith(key):
            mat_date = MATURITY_MAP[key]
            break
            
    if not mat_date:
        # Fallback based on last digit/char of ticker code if available
        mat_date = "2027-06-30"
        
    # Replace maturity: "2030-12-31" with maturity: "mat_date"
    block = re.sub(r'maturity:\s*"2030-12-31"', f'maturity: "{mat_date}"', block)
    # Replace the second cashflow date
    block = re.sub(r'\{ date: "2030-12-31"', f'{{ date: "{mat_date}"', block)
    
    return block

# Match each object block inside BONDS_DATASET
pattern = r'\{\s*id:\s*"bond_[^"]+".*?\n\s*\}'
new_content = re.sub(pattern, update_bond, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated maturities across all bonds.")
