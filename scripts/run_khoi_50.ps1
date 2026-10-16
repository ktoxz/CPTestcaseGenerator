[CmdletBinding()]
param(
    [int]$Iterations = 3,
    [int]$CasesPerRound = 10,
    [int]$OracleLimit = 20,
    [string]$Model = "ollama",
    [string]$OllamaModel = "nemotron-3-nano:30b-cloud",
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$ExtraArgs
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$python = Get-Command py -ErrorAction SilentlyContinue
if ($null -eq $python) {
    throw "Python launcher 'py' was not found. Install Python 3.12 first."
}

$problems = @(
    "cf1000a", "cf1000b", "cf1003a", "cf1003b", "cf1003c",
    "cf1004a", "cf1004b", "cf1004c", "cf1005a", "cf1005b",
    "cf1005c", "cf1005d", "cf1006a", "cf1006b", "cf1006c",
    "cf1006d", "cf1007a", "cf1008a", "cf1008b", "cf1009a",
    "cf1009b", "cf1009c", "cf1010a", "cf1010c", "cf1011a",
    "p02548", "p02554", "p02555", "p02574", "p02580",
    "p02584", "p02585", "p02586", "p02596", "p02598",
    "p02599", "p02614", "p02623", "p02629", "p02642",
    "p02661", "p02678", "p02685", "p02691", "p02839",
    "p02986", "p03044", "p03274", "p03575", "p03862"
)

Push-Location $root
try {
    & py -3.12 main.py --problems @problems --oracle `
        --oracle-limit $OracleLimit --iterations $Iterations `
        --cases-per-round $CasesPerRound --model $Model `
        --ollama-model $OllamaModel --judge local @ExtraArgs
    exit $LASTEXITCODE
}
finally {
    Pop-Location
}
