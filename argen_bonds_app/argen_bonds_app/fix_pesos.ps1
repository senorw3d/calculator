$file = 'C:\Users\valen\.gemini\antigravity\scratch\argen_bonds_app\js\data.js'
$lines = Get-Content $file -Encoding UTF8

for($i=0; $i -lt $lines.Length; $i++){
    if($lines[$i] -match 'instrumentGroup: "Pesos Fijos"'){
        for($j=$i-15; $j -le $i; $j++){
            if($lines[$j] -match 'ticker: "(\w+)"'){
                $ticker = $Matches[1]
                $lastChar = $ticker[-1]
                if($lastChar -eq 'Z'){
                    $lines[$i] = $lines[$i].Replace('Pesos Fijos', 'Pesos BADLAR')
                    Write-Host "$ticker -> Pesos BADLAR"
                } elseif($lastChar -eq 'Y'){
                    $lines[$i] = $lines[$i].Replace('Pesos Fijos', 'Pesos TAMAR')
                    Write-Host "$ticker -> Pesos TAMAR"
                } else {
                    Write-Host "$ticker -> Pesos Fijos (kept)"
                }
                break
            }
        }
    }
}

Set-Content -Path $file -Value $lines -Encoding UTF8
Write-Host "Done!"
