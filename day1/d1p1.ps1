cd $PSScriptRoot
$lines = Get-Content "input.txt"
$a1 = @()
$a2 = @()
foreach($line in $lines) {
    $line -match "^(\d+)\s+(\d+)$" | Out-Null
    $a1 += [int]$Matches[1]
    $a2 += [int]$Matches[2]
}

$a1 = $a1 | Sort-Object 
$a2 = $a2 | Sort-Object 

$result = 0
for($i=0; $i -lt $a1.Length; $i++) {
    $result += [Math]::Abs($a1[$i] - $a2[$i])
}

$result

