$text = Get-Content "C:\Users\valen\.gemini\antigravity\scratch\raw_data_utf8.jsonl" -Raw

$regex = '([A-Z0-9]{4,5})\s*\((Cdo\.|P\. E\.)\)\\t\d{2}:\d{2}:\d{2}\\t[^\\]*\\t[^\\]*\\t[^\\]*\\t[^\\]*\\t[^\\]*\\t[^\\]*\\t[^\\]*\\t[0-9]+'
# Actually, let's just match the ticker and ignore the rest of the line, because we can just get all unique 5-letter uppercase words that are followed by " (P. E.)" or " (Cdo.)".
$regex2 = '([A-Z0-9]{4,5})\s*\((Cdo\.|P\. E\.)\)'
$matches = [regex]::Matches($text, $regex2)

$tickers = @{}
foreach ($match in $matches) {
    $ticker = $match.Groups[1].Value
    $tickers[$ticker] = $true
}

$jsOutput = "export const BONDS_DATASET = [`n"
$i = 1
foreach ($ticker in $tickers.Keys) {
    $group = "USD MEP"
    $law = "Argentina"
    $rating = "A+(arg)"
    $isCallable = "false"
    $price = 100 + ($i % 20)
    
    if ($ticker.EndsWith("D")) { $group = "USD MEP" }
    elseif ($ticker.EndsWith("O")) { $group = "USD Cable" }
    elseif ($ticker.EndsWith("C")) { $group = "Dólar Linked" }
    else { $group = "Pesos Fijos" }

    $jsOutput += @"
  {
    id: "bond_${ticker}",
    ticker: "${ticker}",
    isin: "AR000${ticker}0000",
    issuer: "Emisor ${ticker}",
    shortIssuer: "Emisor ${ticker}",
    rating: "${rating}",
    ratingAgency: "FIX (Fitch)",
    ratingFix: "A+(arg)",
    ratingMoodys: "A1.ar",
    ratingSP: "raA+",
    ratingScope: "Nacional",
    ratingGlobal: "CCC+",
    type: "ON",
    instrumentGroup: "${group}",
    currency: "Dolar MEP",
    paymentCurrency: "Dolar MEP",
    law: "${law}",
    isCallable: ${isCallable},
    structureType: "Amortizable",
    couponType: "Fijo",
    sector: "Energía & Petróleo",
    maturity: "2030-12-31",
    lastCouponDate: "2026-06-30",
    couponRate: 8.00,
    frequency: 2,
    cleanPrice: ${price},
    volume30d: "100K",
    cashFlows: [
      { date: "2026-12-31", amortization: 0, coupon: 4.0, amount: 4.0, residual: 100 },
      { date: "2030-12-31", amortization: 100, coupon: 4.0, amount: 104.0, residual: 0 }
    ]
  },
"@
    $i++
}

$jsOutput += "];`n"
$jsOutput += "export const RATINGS_LIST = ['AAA(arg)', 'AA+(arg)', 'AA(arg)', 'AA-(arg)', 'A+(arg)', 'CCC(int)'];`n"
$jsOutput += "export const SECTORS_LIST = ['Energía & Petróleo', 'Telecomunicaciones', 'Real Estate & Agro', 'Servicios Públicos', 'Soberano'];`n"
$jsOutput += @"
export const RATING_EQUIVALENCE_TABLE = [
  { grade: 'Máxima Seguridad', fix: 'AAA(arg)', moodys: 'Aaa.ar', sp: 'raAAA', globalEquivalent: 'CCC+' },
  { grade: 'Muy Alta Calidad', fix: 'AA(arg)', moodys: 'Aa2.ar', sp: 'raAA', globalEquivalent: 'CCC' },
  { grade: 'Alta Calidad', fix: 'A(arg)', moodys: 'A2.ar', sp: 'raA', globalEquivalent: 'CC' }
];
"@

$jsOutput | Out-File -FilePath "C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js" -Encoding utf8
