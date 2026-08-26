param(
  [string]$Target = 'C:\0\_Infinite\_AI\01\_Projects\pptx-beautify-lock-Skil',
  [string]$CatalogTarget = 'C:\0\_Infinite\_AI\01\_Projects\pptx-beautify-lock-Skil\_catalog\Claude-code-ChatGPT-Codex---SKILL'
)

$ErrorActionPreference = 'Stop'
$SkillRepo = 'https://github.com/Space653000/pptx-beautify-lock-Skill.git'
$CatalogRepo = 'https://github.com/Space653000/Claude-code-ChatGPT-Codex---SKILL.git'

function Sync-Repo([string]$RepoUrl, [string]$Path) {
  $parent = Split-Path -Parent $Path
  if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Force -Path $parent | Out-Null }

  if (Test-Path (Join-Path $Path '.git')) {
    Write-Host "Updating $Path" -ForegroundColor Cyan
    $dirty = git -C $Path status --porcelain
    if ($dirty) {
      throw "Local changes exist in $Path. Backup script refuses to overwrite them. Commit/stash them first."
    }
    git -C $Path fetch origin main
    git -C $Path merge --ff-only origin/main
  }
  elseif (Test-Path $Path) {
    throw "$Path exists but is not a Git checkout. Rename/remove it before running backup."
  }
  else {
    Write-Host "Cloning $RepoUrl -> $Path" -ForegroundColor Cyan
    git clone $RepoUrl $Path
  }
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  throw 'Git for Windows is required but git.exe was not found in PATH.'
}

Sync-Repo $SkillRepo $Target
Sync-Repo $CatalogRepo $CatalogTarget

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$manifest = Join-Path $Target 'BACKUP_MANIFEST.txt'
$skillSha = (git -C $Target rev-parse HEAD).Trim()
$catalogSha = (git -C $CatalogTarget rev-parse HEAD).Trim()
@
"Backup time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss K')"
"pptx-beautify-lock-Skill: $skillSha"
"Claude-code-ChatGPT-Codex---SKILL: $catalogSha"
"Target: $Target"
"Catalog target: $CatalogTarget"
"Policy: fast-forward only; local modifications are never overwritten."
@ | Set-Content -Encoding UTF8 $manifest

Write-Host ''
Write-Host 'BACKUP_PASS=true' -ForegroundColor Green
Write-Host "Skill backup: $Target"
Write-Host "Catalog backup: $CatalogTarget"
Write-Host "Manifest: $manifest"
