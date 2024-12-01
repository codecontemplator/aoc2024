cd $PSScriptRoot
$lines = Get-Content "input.txt"
$a1 = @()
$a2 = @()
foreach($line in $lines) {
    $line -match "^(\d+)\s+(\d+)$" | Out-Null
    $a1 += [int]$Matches[1]
    $a2 += [int]$Matches[2]
}

$result = 0
foreach($e in $a1) {
    $c = $a2 | Where-Object { $_ -eq $e} | Measure-Object | Select-Object -ExpandProperty Count
    $result += $e * $c
}

$result