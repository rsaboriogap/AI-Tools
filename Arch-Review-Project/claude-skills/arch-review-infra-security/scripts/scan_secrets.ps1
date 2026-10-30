param([Parameter(Mandatory=$true)][string]$Target)
# Read-only secret scan. Prints file:line [type]; matched values are masked.
if (-not (Test-Path $Target)) { throw "Path not found: $Target" }
$q = "[`"']"
$patterns = [ordered]@{
    "password"    = "password\s*[:=]\s*$q[^`"']{4,}"
    "api_key"     = "api[_-]?key\s*[:=]\s*$q[^`"']{8,}"
    "aws_key"     = 'AKIA[0-9A-Z]{16}'
    "pem_key"     = '-----BEGIN (RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'
    "conn_string" = "(Password|Pwd)=[^;`"' ]{4,};"
}
$exclude = @("node_modules", ".git", "dist", "build", "vendor", "bin", "obj", ".venv", "venv", ".vs")
$skipFiles = @("package-lock.json", "yarn.lock")
Write-Host "# Secret scan: $Target"
Get-ChildItem -Path $Target -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object {
        $p = $_.FullName
        $skipFiles -notcontains $_.Name -and
        -not ($exclude | Where-Object { $p -match ("[\\/]" + [regex]::Escape($_) + "[\\/]") })
    } |
    ForEach-Object {
        foreach ($name in $patterns.Keys) {
            Select-String -Path $_.FullName -Pattern $patterns[$name] -ErrorAction SilentlyContinue |
                ForEach-Object { Write-Host "$($_.Path):$($_.LineNumber) [$name] <masked>" }
        }
    }
