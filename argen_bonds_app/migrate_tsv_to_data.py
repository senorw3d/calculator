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
                
            rating = row[17].strip() if len(row) > 17 else ""
            
            bond = {
                "id": f"bond_{ticker}",
                "ticker": ticker,
                "isin": isin,
                "issuer": emisor,
                "shortIssuer": emisor[:20], # truncated for now
                "rating": rating,
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
        
    print(f"Migrated {len(bonds)} bonds to {output_file}")

if __name__ == '__main__':
    migrate()
