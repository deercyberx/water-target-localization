# 实验运行脚本（模板）
# 使用前请根据实际项目修改路径和参数

$ErrorActionPreference = "Stop"

$PROJECT_ROOT = Split-Path -Parent $PSScriptRoot
$CODE_DIR = Join-Path $PROJECT_ROOT "code"
$RESULTS_DIR = Join-Path $PROJECT_ROOT "results"
$LOGS_DIR = Join-Path $PROJECT_ROOT "logs"

$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"

Write-Host "=== 开始实验 ===" -ForegroundColor Cyan
Write-Host "时间: $TIMESTAMP"

# 激活虚拟环境
$venvActivate = Join-Path $CODE_DIR ".venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) { & $venvActivate }

# 运行训练
Write-Host "--- 训练中 ---" -ForegroundColor Yellow
python (Join-Path $CODE_DIR "train.py") 2>&1 | Tee-Object -FilePath (Join-Path $LOGS_DIR "train_$TIMESTAMP.log")

Write-Host "=== 实验完成 ===" -ForegroundColor Green
Write-Host "日志: $LOGS_DIR\train_$TIMESTAMP.log"
