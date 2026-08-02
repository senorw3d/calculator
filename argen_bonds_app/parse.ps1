$json = Get-Content C:\Users\valen\.gemini\antigravity\scratch\raw_data_utf8.jsonl -Raw | ConvertFrom-Json
$lines = $json.content -split '\r?\n'
$bonds = @()
foreach ($line in $lines) {
    if ($line -match '^([A-Z0-9]+)\s*\((Cdo\.|P\. E\.)\)\t.*?\t([\d,]+)\t') {
        $bonds += [PSCustomObject]@{
            Ticker = $matches[1]
            Type = $matches[2]
            Price = $matches[3]
        }
    }
}
$bonds | Group-Object Ticker | ForEach-Object {
    $_.Group | Sort-Object Type -Descending | Select-Object -First 1
} | ConvertTo-Json -Depth 2 | Out-File C:\Users\valen\.gemini\antigravity\scratch\parsed_bonds.json -Encoding utf8
