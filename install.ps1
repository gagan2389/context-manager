# ============================================================
#  Context Manager for Claude Code — Windows Installer
#  Run in PowerShell: .\install.ps1
# ============================================================

$ErrorActionPreference = "Stop"

$SkillName = "context-manager"
$InstallDir = "$env:USERPROFILE\.claude\skills\$SkillName"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SourceDir = Join-Path $ScriptDir ".claude\skills\$SkillName"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗"
Write-Host "║   Context Manager — Claude Code Skill Installer  ║"
Write-Host "╚══════════════════════════════════════════════════╝"
Write-Host ""

# Check Python 3
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion"
} catch {
    Write-Host "⚠️  Python not found."
    Write-Host "   Install it from https://python.org and re-run this script."
    exit 1
}

# Check if Claude Code config dir exists
$claudeDir = "$env:USERPROFILE\.claude"
if (-not (Test-Path $claudeDir)) {
    Write-Host ""
    Write-Host "⚠️  ~/.claude directory not found."
    Write-Host "   Make sure Claude Code is installed first:"
    Write-Host "   npm install -g @anthropic-ai/claude-code"
    Write-Host ""
    $ans = Read-Host "   Create ~/.claude anyway? [y/N]"
    if ($ans -match "^[Yy]$") {
        New-Item -ItemType Directory -Path "$claudeDir\skills" -Force | Out-Null
    } else {
        Write-Host "Cancelled."
        exit 1
    }
}

# Create skills directory if needed
New-Item -ItemType Directory -Path "$env:USERPROFILE\.claude\skills" -Force | Out-Null

# Backup existing install if present
if (Test-Path $InstallDir) {
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backup = "$InstallDir.backup.$timestamp"
    Write-Host ""
    Write-Host "ℹ️  Existing install found. Backing up to:"
    Write-Host "   $backup"
    Move-Item $InstallDir $backup
}

# Copy skill files
Write-Host ""
Write-Host "📦 Installing to: $InstallDir"
Copy-Item -Recurse -Path $SourceDir -Destination $InstallDir

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗"
Write-Host "║   ✅  Installation complete!                      ║"
Write-Host "╚══════════════════════════════════════════════════╝"
Write-Host ""
Write-Host "The skill is now available in ALL your Claude Code projects."
Write-Host ""
Write-Host "Quick start:"
Write-Host "  1. Open Claude Code in any project"
Write-Host "  2. Type: /ignore init          <- set up ignore list"
Write-Host "  3. Type: /tokenstatus          <- see current token usage"
Write-Host "  4. Type: /topiccontext create Project-1-Name   <- create topic scope"
Write-Host "  5. Type: /usetopiccontext Project-1-Name <- activate topic scope"
Write-Host ""
