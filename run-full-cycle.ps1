param(
  [string]$ProjectRoot = (Split-Path -Parent $PSCommandPath),
  [string]$AgentPrompt = "agents/pistachio-agent-v3.md",
  [string]$GeneratedDir = "",
  [string]$ReferenceDir = "",
  [string]$LoraVersion = "v3",
  [string]$RunId = "",
  [string]$Notes = "",
  [double]$MaxAgeDays = 7.0,
  [switch]$SkipCostTracking,
  [string]$CostActivity = "autonomous_loop",
  [string]$CompareWithRunId = "",
  [string]$TrainingDatasetDir = "",
  [string]$TrainingOutputDir = "",
  [string]$DatasetManifestOut = "",
  [switch]$RunProduction,
  [string]$ProductionWorkflow = "",
  [string]$ProductionPrompts = "",
  [int]$ProductionCount = 5,
  [string]$ProductionOutputDir = "",
  [string]$ProductionReferenceDir = "",
  [string]$ProductionLora = "",
  [switch]$SkipCommit,
  [switch]$DryRun
)

$ErrorActionPreference = "Stop"

function Get-PythonCmd {
  if (Get-Command python -ErrorAction SilentlyContinue) {
    return @("python")
  }
  if (Get-Command py -ErrorAction SilentlyContinue) {
    return @("py", "-3")
  }
  throw "Python not found in PATH."
}

$py = @(Get-PythonCmd)
$cmd = @()
$cmd += $py
$cmd += (Join-Path $ProjectRoot "tools\run_full_cycle.py")
$cmd += @(
  "--project-root", $ProjectRoot,
  "--agent-prompt", $AgentPrompt,
  "--lora-version", $LoraVersion,
  "--max-age-days", "$MaxAgeDays"
)

if ($GeneratedDir) {
  $cmd += @("--generated-dir", $GeneratedDir)
}
if ($ReferenceDir) {
  $cmd += @("--reference-dir", $ReferenceDir)
}
if ($RunId) {
  $cmd += @("--run-id", $RunId)
}
if ($Notes) {
  $cmd += @("--notes", $Notes)
}
if ($SkipCostTracking) {
  $cmd += "--skip-cost-tracking"
}
if ($CostActivity) {
  $cmd += @("--cost-activity", $CostActivity)
}
if ($CompareWithRunId) {
  $cmd += @("--compare-with-run-id", $CompareWithRunId)
}
if ($TrainingDatasetDir) {
  $cmd += @("--training-dataset-dir", $TrainingDatasetDir)
}
if ($TrainingOutputDir) {
  $cmd += @("--training-output-dir", $TrainingOutputDir)
}
if ($DatasetManifestOut) {
  $cmd += @("--dataset-manifest-out", $DatasetManifestOut)
}
if ($RunProduction) {
  $cmd += "--run-production"
  if ($ProductionWorkflow) {
    $cmd += @("--production-workflow", $ProductionWorkflow)
  }
  if ($ProductionPrompts) {
    $cmd += @("--production-prompts", $ProductionPrompts)
  }
  if ($ProductionCount -gt 0) {
    $cmd += @("--production-count", "$ProductionCount")
  }
  if ($ProductionOutputDir) {
    $cmd += @("--production-output-dir", $ProductionOutputDir)
  }
  if ($ProductionReferenceDir) {
    $cmd += @("--production-reference-dir", $ProductionReferenceDir)
  }
  if ($ProductionLora) {
    $cmd += @("--production-lora", $ProductionLora)
  }
}
if ($SkipCommit) {
  $cmd += "--skip-commit"
}
if ($DryRun) {
  $cmd += "--dry-run"
}

Write-Host "Running full cycle:"
Write-Host ("  " + ($cmd -join " "))

if ($cmd.Length -gt 1) {
  & $cmd[0] $cmd[1..($cmd.Length - 1)]
} else {
  & $cmd[0]
}
exit $LASTEXITCODE
