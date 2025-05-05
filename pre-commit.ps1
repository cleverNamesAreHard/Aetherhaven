$ErrorActionPreference = 'Stop'

Write-Host "Running AutoPep8"

$stagedFiles = git diff --cached --name-only --diff-filter=ACM | Where-Object { $_ -like '*.py' }

foreach ($file in $stagedFiles) {
    $fullPath = Resolve-Path $file | Select-Object -ExpandProperty Path

    if (
        $fullPath -match '\\venv\\' -or
        $fullPath -match 'pycache' -or
        $fullPath -match '\\migrations\\'
    ) {
        continue
    }

    Write-Host "Auto-formatting: $file"
    autopep8 --in-place --aggressive --aggressive $fullPath

    git add $file
}
