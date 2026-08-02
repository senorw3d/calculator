# PowerShell script to fix issuer names in data.js
# Uses full ticker matching since issuer strings contain the full ticker

$file = 'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
$content = Get-Content $file -Raw -Encoding UTF8

# Full ticker -> (issuer, shortIssuer) mapping
$tickerMap = @{}

# Helper to add all tickers with a given prefix
function AddPrefix($prefix, $fullName, $shortName, $suffixes) {
    foreach ($s in $suffixes) {
        $ticker = $prefix + $s
        $tickerMap[$ticker] = @($fullName, $shortName)
    }
}

# YPF S.A.
$ypfTickers = @('YFCGD','YFCID','YFCIO','YFCJC','YFCJD','YFCJO','YFCKD','YFCKO','YFCLD','YFCLO','YFCMD','YFCND','YFCOC','YFCOD',
    'YM34C','YM34D','YM34O','YM35D','YM35O','YM37D','YM37O','YM38D','YM38O','YM39C','YM39D','YM39O','YM40D','YM41D','YM41O','YM42C','YM42D','YM42O','YM43D',
    'YMCIC','YMCID','YMCIO','YMCJC','YMCJD','YMCJO','YMCXC','YMCXD','YMCXO','YMCYD','YMCYO','YMCZC')
foreach ($t in $ypfTickers) { $tickerMap[$t] = @('YPF S.A.','YPF') }

# Telecom Argentina
$tlcTickers = @('TLCMD','TLCMO','TLCMZ','TLCOD','TLCOO','TLCPC','TLCPD','TLCPO','TLCTC','TLCTD','TLCTO','TLCUD','TLCUO','TLCVD','TLCWD','T662O','T672D','LCMZ')
foreach ($t in $tlcTickers) { $tickerMap[$t] = @('Telecom Argentina S.A.','Telecom') }

# IRSA
$irsaTickers = @('IRCFD','IRCFO','IRCND','IRCOC','IRCOD','IRCOO')
foreach ($t in $irsaTickers) { $tickerMap[$t] = @('IRSA Inversiones y Representaciones S.A.','IRSA') }
$irsaPropTickers = @('IRCPC','IRCPD','IRCPO')
foreach ($t in $irsaPropTickers) { $tickerMap[$t] = @('IRSA Propiedades Comerciales S.A.','IRSA Prop. Com.') }

# Pan American Energy
$paeTickers = @('PN35D','PN35O','PN36C','PN36D','PN36O','PN38D','PN41D','PN41O','PN42D','PN42O','PN43D','PN43O','PNXCC','PNXCO','PECMO','PECND','PECNO')
foreach ($t in $paeTickers) { $tickerMap[$t] = @('Pan American Energy Group S.L.','Pan American') }

# Arcor
foreach ($t in @('ARC1C','ARC1D')) { $tickerMap[$t] = @('Arcor S.A.I.C.','Arcor') }

# Aeropuertos Argentina 2000
$tickerMap['AERBD'] = @('Aeropuertos Argentina 2000 S.A.','AA2000')

# Banco Galicia
foreach ($t in @('BACGC','BACGD')) { $tickerMap[$t] = @('Banco de Galicia y Buenos Aires S.A.U.','Bco. Galicia') }
$tickerMap['BACHC'] = @('Banco Hipotecario S.A.','Bco. Hipotecario')

# Central Puerto
foreach ($t in @('CP37D','CP37O','CP38C','CP38D','CP38O','CP40D')) { $tickerMap[$t] = @('Central Puerto S.A.','Central Puerto') }

# Cresud
foreach ($t in @('CS45O','CS47C','CS47D','CS48D','CS48O','CS49D','CS49O','CS50D','CS50O','CS51D','CS51O','CS52D','CS52O')) { $tickerMap[$t] = @('Cresud S.A.C.I.F. y A.','Cresud') }

# Edenor
foreach ($t in @('DNC3C','DNC3D','DNC3O','DNC3Y','DNC5D','DNC5O','DNC7C','DNC7D','DNC7O','DNC9O','DNCAD','DNCAO','DNCBD','DNCBO')) { $tickerMap[$t] = @('Edenor S.A.','Edenor') }

# Generacion Mediterranea
foreach ($t in @('MGCED','MGCEO','MGCMO','MGCND','MGCNO','MGCOC','MGCOD','MGCOO','MGCOZ','MGCQD','MGCQO','MGCRD','MGCRO','MGCRZ','MGCTD')) { $tickerMap[$t] = @('Generacion Mediterranea S.A.','Gen. Mediterranea') }

# Vista Energy
foreach ($t in @('VSCPC','VSCPD','VSCPO','VSCQD','VSCRC','VSCRD','VSCRO','VSCUC','VSCUD','VSCUO','VSCVD','VSCVO','VSCXD','VSCXO','VSCZC','VSCZO')) { $tickerMap[$t] = @('Vista Energy Argentina S.A.U.','Vista Energy') }

# Tecpetrol
foreach ($t in @('TTC8D','TTC8O','TTC9D','TTCAC','TTCAD','TTCBD','TTCBO','TTCDO','TTCED','TTCEO')) { $tickerMap[$t] = @('Tecpetrol S.A.','Tecpetrol') }

# TGS
foreach ($t in @('TSC3C','TSC4D','TSC4O','TSC4Z')) { $tickerMap[$t] = @('Transportadora de Gas del Sur S.A.','TGS') }

# Loma Negra
foreach ($t in @('LOC5C','LOC5D','LOC5O','LOC6C','LOC6D','LOC6O','LMS7C','LMS7D','LMS7O','LMS8C')) { $tickerMap[$t] = @('Loma Negra C.I.A.S.A.','Loma Negra') }

# Mastellone
foreach ($t in @('MCC1C','MCC2D','MCC3C','MCC3D','MCC3O','MTC2D','MTC2O')) { $tickerMap[$t] = @('Mastellone Hnos. S.A.','Mastellone') }

# Mirgor
foreach ($t in @('MR43D','MR43O','MR44D','MR44O','MR46D','MR46O','MR47D')) { $tickerMap[$t] = @('Mirgor S.A.C.I.F.I.A.','Mirgor') }

# Pluspetrol
foreach ($t in @('PLC1O','PLC2C','PLC2D','PLC2O','PLC3D','PLC3O','PLC4C','PLC4D','PLC4O','PLC5D','PLC5O','PLC6O','PLC7C','PLC7D','PLC7O')) { $tickerMap[$t] = @('Pluspetrol S.A.','Pluspetrol') }

# Banco Supervielle
foreach ($t in @('SBC1D','SBC1O','SBC2D','SBC2O','SBC3D','SBC3O')) { $tickerMap[$t] = @('Banco Supervielle S.A.','Bco. Supervielle') }

# PCR
foreach ($t in @('PQCRD','PQCRO','PQCSD','PQCSO')) { $tickerMap[$t] = @('Petroquimica Comodoro Rivadavia S.A.','PCR') }

# Rizobacter
$tickerMap['RZBCD'] = @('Rizobacter Argentina S.A.','Rizobacter')

# San Miguel
foreach ($t in @('SNEBD','SNSBD','SNSDD')) { $tickerMap[$t] = @('S.A. San Miguel A.G.I.C.I. y F.','San Miguel') }

# 360 Energy
foreach ($t in @('GYC4O','GYC5D')) { $tickerMap[$t] = @('360 Energy Solar S.A.','360 Energy') }

# MSU Energy
foreach ($t in @('EAC4D','EAC4O','MSSFD','MSSGD')) { $tickerMap[$t] = @('MSU Energy S.A.','MSU Energy') }

# Genneia
foreach ($t in @('GN49D','GN49O')) { $tickerMap[$t] = @('Genneia S.A.','Genneia') }

# Oiltanking
foreach ($t in @('OT41D','OT42D','OT42O','OTS2D','OTS2O','OTS5O')) { $tickerMap[$t] = @('Oiltanking Ebytem S.A.','Oiltanking') }

# Capex
foreach ($t in @('CAC5D','CACBD','CACDO')) { $tickerMap[$t] = @('Capex S.A.','Capex') }

# Oldelval
foreach ($t in @('OLC5D','OLC5O','OLC6D','OLC7D','OLC7O')) { $tickerMap[$t] = @('Oleoductos del Valle S.A.','Oldelval') }

# Ledesma
$tickerMap['LDCGO'] = @('Ledesma S.A.A.I.','Ledesma')

# BBVA Argentina
foreach ($t in @('BF37D','BF39D')) { $tickerMap[$t] = @('BBVA Argentina S.A.','BBVA Argentina') }

# Grupo Supervielle
$tickerMap['GPS1M'] = @('Grupo Supervielle S.A.','Grupo Supervielle')

# Holcim
foreach ($t in @('HJCFD','HJCIO')) { $tickerMap[$t] = @('Holcim Argentina S.A.','Holcim') }

# CGC (Compania General de Combustibles)
foreach ($t in @('NPCCC','NPCCD','NPCCO','NPCDD','NPCDO','NPCED','NPCEO')) { $tickerMap[$t] = @('Compania Gral. de Combustibles S.A.','CGC') }

# Clisa
foreach ($t in @('CLI1D','CLSIO')) { $tickerMap[$t] = @('Clisa - Cia. Latinoamericana de Infraestructura','Clisa') }

# CIESA
foreach ($t in @('CICAD','CICAO','CICBD')) { $tickerMap[$t] = @('Cia. de Inversiones de Energia S.A.','CIESA') }

# Edesur
foreach ($t in @('EMC1D','EMC1O')) { $tickerMap[$t] = @('Empresa Distribuidora Sur S.A.','Edesur') }

# Albanesi
foreach ($t in @('BYCVD','BYCVO','BYCVX','BYCVY')) { $tickerMap[$t] = @('Albanesi Energia S.A.','Albanesi') }

# DESA
foreach ($t in @('DEC2D','DEC4D')) { $tickerMap[$t] = @('DESA Desarrollos S.A.','DESA') }

# Havanna
$tickerMap['HVS1D'] = @('Havanna S.A.','Havanna')

# SCP
foreach ($t in @('LQC1C','LQC1O')) { $tickerMap[$t] = @('Sociedad Comercial del Plata S.A.','SCP') }

# Molinos Agro
$tickerMap['LUC5D'] = @('Molinos Agro S.A.','Molinos Agro')

# TGLT
foreach ($t in @('OZC3D','OZC3O')) { $tickerMap[$t] = @('TGLT S.A.','TGLT') }

# Raghsa
foreach ($t in @('RC1CD','RC2CD','RC2CO')) { $tickerMap[$t] = @('Raghsa S.A.','Raghsa') }

# Banco Prov Cordoba
foreach ($t in @('RCCRD','RCCRO')) { $tickerMap[$t] = @('Banco de la Prov. de Cordoba S.A.','Bco. Prov. Cordoba') }

# Banco Entre Rios
foreach ($t in @('RUCDC','RUCDD','RUCDO','RUCED','RUCEO')) { $tickerMap[$t] = @('Banco de Entre Rios S.A.','Bco. Entre Rios') }

# RAVA
$tickerMap['RVS1O'] = @('Rava Bursatil S.A.','RAVA')

# Ternium
foreach ($t in @('SIC1D','SIC2D')) { $tickerMap[$t] = @('Ternium Argentina S.A.','Ternium') }

# VBC = Vista Energy (additional series)
foreach ($t in @('VBC1D','VBC2C','VBC2D','VBC2O')) { $tickerMap[$t] = @('Vista Energy Argentina S.A.U.','Vista Energy') }

# Werthein
$tickerMap['WBS3D'] = @('Werthein S.A.','Werthein')

# XMC
foreach ($t in @('XMC1C','XMC1O')) { $tickerMap[$t] = @('Xmarts S.A.','Xmarts') }

# ZZC = Pampa Energia
foreach ($t in @('ZZC1D','ZZC1O')) { $tickerMap[$t] = @('Pampa Energia S.A.','Pampa Energia') }

# PZCG
$tickerMap['PZCGO'] = @('Autopistas del Sol S.A.','Ausol')

# Now replace each specific ticker
foreach ($ticker in $tickerMap.Keys) {
    $fullName = $tickerMap[$ticker][0]
    $shortName = $tickerMap[$ticker][1]
    
    $content = $content.Replace("issuer: `"Emisor $ticker`"", "issuer: `"$fullName`"")
    $content = $content.Replace("shortIssuer: `"Emisor $ticker`"", "shortIssuer: `"$shortName`"")
}

[System.IO.File]::WriteAllText($file, $content, [System.Text.Encoding]::UTF8)
Write-Host "Done! Updated all issuer names."
