# Code-Documentation Skill Installer
# Copies the Code-Documentation skill to your project

param(
    [Parameter(Mandatory=$true, HelpMessage="Path to your project directory")]
    [string]$ProjectPath
)

# Validate project path exists
if (-not (Test-Path $ProjectPath)) {
    Write-Error "Project path does not exist: $ProjectPath"
    exit 1
}

# Define paths
$skillSource = Join-Path -Path (Join-Path -Path (Join-Path -Path $PSScriptRoot -ChildPath "..") -ChildPath ".claude") -ChildPath "skills"
$skillDest = Join-Path -Path (Join-Path -Path $ProjectPath -ChildPath ".claude") -ChildPath "skills"
$configSource = Join-Path -Path (Join-Path -Path $PSScriptRoot -ChildPath "..") -ChildPath "skill-config.json"
$configDest = Join-Path -Path $ProjectPath -ChildPath "skill-config.json"

# Verify source exists
if (-not (Test-Path $skillSource)) {
    Write-Error "Skill source not found: $skillSource"
    exit 1
}

# Create destination directory
New-Item -ItemType Directory -Path $skillDest -Force | Out-Null
Write-Output "[+] Created .claude/skills directory"

# Copy skill files
Copy-Item -Path "$skillSource\*" -Destination $skillDest -Recurse -Force
Write-Output "[+] Copied skill files"

# Copy config template if it exists
if (Test-Path $configSource) {
    Copy-Item -Path $configSource -Destination $configDest -Force
    Write-Output "[+] Copied skill-config.json template"
} else {
    Write-Output "[*] skill-config.json template not found (optional)"
}

Write-Output ""
Write-Output "[SUCCESS] Installation complete!"
Write-Output "[PATH] Skill installed to: $skillDest"
Write-Output ""
Write-Output "Next steps:"
Write-Output "1. Reload Claude Code to activate the skill"
Write-Output "2. Edit skill-config.json to configure your preferences"
Write-Output "3. Run: /code-documentation"
