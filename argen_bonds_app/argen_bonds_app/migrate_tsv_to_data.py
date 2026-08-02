import csv
import json
import re

def migrate():
    input_file = "ons_list.tsv"
    output_file = "js/data.js"
    
    bonds = []
    
    with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        
        for row in reader:
            if not row or len(row) < 12:
                continue
                
            estado = row[0].strip()
            if estado != "Normal":
                pass # maybe skip? let's keep all for now if ticker exists
            
            titulo = row[1].strip()
            emisor = row[2].strip()
            ticker = row[3].strip()
            
            if not ticker:
                continue
                
            fecha_alta = row[4].strip()
            vencimiento_raw = row[5].strip()
            moneda = row[6].strip()
            ley = row[7].strip()
            jurisdiccion = row[8].strip()
            isin = row[10].strip()
            serie = row[11].strip()
            
            # Format maturity to YYYY-MM-DD
            maturity = ""
            if vencimiento_raw and '/' in vencimiento_raw:
                parts = vencimiento_raw.split('/')
                if len(parts) == 3:
                    # DD/MM/YYYY
                    maturity = f"{parts[2]}-{parts[1]}-{parts[0]}"
            
            # Currency mapping
            currency_code = "ARS"
            instrument_group = "Pesos"
            if "Dólares" in moneda:
                currency_code = "USD"
                instrument_group = "USD MEP"
            elif "UVA" in moneda:
                currency_code = "UVA"
                instrument_group = "UVA"
            elif "Dólar Linked" in moneda:
                currency_code = "USD"
                instrument_group = "Dolar Linked"
            
            tasa = row[19].strip() if len(row) > 19 else "0"
            coupon_rate = 0.0
            try:
                tasa = tasa.replace(',', '.')
                match = re.search(r"[-+]?\d*\.\d+|\d+", tasa)
                if match:
                    coupon_rate = float(match.group())
            except:
                pass
                
            raw_rating = row[17].strip() if len(row) > 17 else ""
            
            clean_rating = "S/C"
            r_up = raw_rating.upper()
            if "AAA" in r_up:
                clean_rating = "AAA(arg)"
            elif "AA-" in r_up or "AA -" in r_up:
                clean_rating = "AA-(arg)"
            elif "AA+" in r_up or "AA +" in r_up:
                clean_rating = "AA+(arg)"
            elif "AA" in r_up:
                clean_rating = "AA(arg)"
            elif "A-" in r_up or "A -" in r_up:
                clean_rating = "A-(arg)"
            elif "A+" in r_up or "A +" in r_up or "A1+" in r_up:
                clean_rating = "A+(arg)"
            elif "A" in r_up:
                clean_rating = "A(arg)"
            elif "BBB+" in r_up or "BBB +" in r_up:
                clean_rating = "BBB+(arg)"
            elif "BBB" in r_up or "BBB-" in r_up:
                clean_rating = "BBB(arg)"
            
            bond = {
                "id": f"bond_{ticker}",
                "ticker": ticker,
                "isin": isin,
                "issuer": emisor,
                "shortIssuer": emisor[:20], # truncated for now
                "rating": clean_rating,
                "type": "ON",
                "instrumentGroup": instrument_group,
                "currency": currency_code,
                "paymentCurrency": currency_code,
                "law": ley if ley else "Argentina",
                "isCallable": False,
                "structureType": "Bullet", # default for now
                "couponType": "Fijo",
                "sector": "Corporativo",
                "maturity": maturity,
                "couponRate": coupon_rate,
                "frequency": 2,
                "cleanPrice": 100.0,
                "volume30d": "-",
                "cashFlows": []
            }
            
            # Add a dummy cashflow for the maturity so the app doesn't break
            if maturity:
                bond["cashFlows"].append({
                    "date": maturity,
                    "amortization": 100.0,
                    "coupon": coupon_rate / 2, # assuming semiannual
                    "amount": 100.0 + (coupon_rate / 2),
                    "residual": 0.0
                })
            
            bonds.append(bond)

    # Write the output file
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write("export const BONDS_DATASET = ")
        json.dump(bonds, out, indent=2, ensure_ascii=False)
        out.write(";\n")
        out.write("""
export const RATINGS_LIST = ['Todos', 'AAA(arg)', 'AA+(arg)', 'AA(arg)', 'AA-(arg)', 'A+(arg)', 'A(arg)', 'A-(arg)', 'BBB+(arg)', 'BBB(arg)'];
export const SECTORS_LIST = ['Todos', 'Energía & Petróleo', 'Bancos & Servicios Financieros', 'Telecomunicaciones', 'Real Estate', 'Consumo y Retail', 'Agropecuario', 'Industrial', 'Corporativo'];
export const RATING_EQUIVALENCE_TABLE = [
  { rating: "AAA", syp: "raAAA", fix: "AAA(arg)", moodys: "Aaa.ar", description: "Máxima calidad crediticia, riesgo mínimo." },
  { rating: "AA", syp: "raAA", fix: "AA(arg)", moodys: "Aa.ar", description: "Muy alta calidad crediticia, muy bajo riesgo." },
  { rating: "A", syp: "raA", fix: "A(arg)", moodys: "A.ar", description: "Alta calidad crediticia, bajo riesgo." },
  { rating: "BBB", syp: "raBBB", fix: "BBB(arg)", moodys: "Baa.ar", description: "Calidad crediticia adecuada, riesgo moderado." }
];
""")
        
    print(f"Migrated {len(bonds)} bonds to {output_file}")

if __name__ == '__main__':
    migrate()
