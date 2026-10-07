param([Parameter(Mandatory=$true)][string]$Target)
if (-not (Test-Path $Target)) { throw "Path not found: $Target" }
$patterns = @{
    "password" = 'password\s*=\s*["'][^"']{4,}'
    "api_key"  = 'api[_-]?key\s*[:=]\s*["'][^"']{8,}'
    "aws_key"  = 'AKIA[0-9A-Z]{16}'
    "pem_key"  = '-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----'
}
$exclude = @("node_modules", ".git", "dist", "build", "vendor", "bin", "obj", ".venv", "venv")
Write-Host "# Secret scan: $Target"
Get-ChildItem -Path $Target -Recurse -File -ErrorAction SilentlyContinue |
    Where-Object { $p = $_.FullName; -not ($exclude | Where-Object { $p -match [regex]::Escape($_) }) } |
    ForEach-Object {
        foreach ($name in $patterns.Keys) {
            Select-String -Path $_.FullName -Pattern $patterns[$name] -ErrorAction SilentlyContinue |
                ForEach-Object { Write-Host "$($_.Path):$($_.LineNumber) [$name] $($_.Line.Trim())" }
        }
    }
