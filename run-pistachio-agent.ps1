param(
  [string]$ProjectRoot = (Split-Path -Parent $PSCommandPath),
  [string]$AgentPromptPath,
  [switch]$DryRun,
  [switch]$SkipGuards
)

$ErrorActionPreference = 'Stop'

if (-not $AgentPromptPath) {
  $AgentPromptPath = Join-Path $ProjectRoot 'agents\pistachio-agent-v2.md'
}

$OutputDir = Join-Path $ProjectRoot 'autonomous-research'
$Date = Get-Date -Format 'yyyy-MM-dd'
$Time = Get-Date -Format 'HH:mm'

if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
  throw "'claude' command not found in PATH."
}

if (-not (Test-Path $AgentPromptPath)) {
  throw "Agent prompt file not found: $AgentPromptPath"
}

function Get-PythonCommand {
  if (Get-Command python -ErrorAction SilentlyContinue) {
    return @('python')
  }
  if (Get-Command py -ErrorAction SilentlyContinue) {
    return @('py', '-3')
  }
  throw "Python not found in PATH."
}

function Invoke-GuardScript {
  param(
    [string]$ScriptPath,
    [string[]]$Arguments
  )

  $py = @(Get-PythonCommand)
  $cmd = $py[0]
  $preArgs = @()
  if ($py.Length -gt 1) {
    $preArgs = $py[1..($py.Length-1)]
  }
  & $cmd @preArgs $ScriptPath @Arguments
  if ($LASTEXITCODE -ne 0) {
    throw "Guard failed: $ScriptPath"
  }
}

New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

if (-not $SkipGuards) {
  Write-Host 'Running Phase 1 guardrails...'
  $toolsDir = Join-Path $ProjectRoot 'tools'
  Invoke-GuardScript -ScriptPath (Join-Path $toolsDir 'lifeos_preflight.py') -Arguments @('--project-root', $ProjectRoot)
  Invoke-GuardScript -ScriptPath (Join-Path $toolsDir 'lifeos_freshness_check.py') -Arguments @('--project-root', $ProjectRoot, '--max-age-days', '7')
  Invoke-GuardScript -ScriptPath (Join-Path $toolsDir 'lifeos_context_budget.py') -Arguments @('--project-root', $ProjectRoot)
}

$agentPrompt = Get-Content -Raw $AgentPromptPath
$runtimeContext = @"

RUNTIME CONTEXT
- project_root: $ProjectRoot
- output_dir: $OutputDir
- today: $Date

Execution requirements:
1. Write final briefing to $OutputDir/briefing-$Date.md.
2. Update memory.md, pending-tasks.md, and predictions.md in $OutputDir.
3. Treat archive/ files as non-authoritative unless explicitly asked.
"@

$finalPrompt = "$agentPrompt`n$runtimeContext"

Write-Host "========================================"
Write-Host "Pistachio Agent - $Date $Time"
Write-Host "========================================"
Write-Host "Project root: $ProjectRoot"
Write-Host "Prompt file: $AgentPromptPath"
Write-Host "Output dir: $OutputDir"

if ($DryRun) {
  Write-Host "DRY RUN enabled. Prompt preview only."
  Write-Host "----------------------------------------"
  Write-Output $finalPrompt
  Write-Host "----------------------------------------"
  exit 0
}

claude -p $finalPrompt

Write-Host "========================================"
Write-Host "Complete"
Write-Host "========================================"
Write-Host "Briefing target: $OutputDir/briefing-$Date.md"
