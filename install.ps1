<#
.SYNOPSIS
  Cài OCR-TB trên Windows (PowerShell 5.1 / PowerShell 7).

.DESCRIPTION
  Tạo virtualenv riêng, cài dependency, tải model ONNX vào cache và tạo lệnh
  `ocr-tb` trong thư mục bin của gói (hoặc thư mục người dùng chỉ định).

.EXAMPLE
  .\install.ps1
  .\install.ps1 -InstallDir C:\ocr-tb
  .\install.ps1 -NoServer
#>
[CmdletBinding()]
param(
  [string] $InstallDir = "$env:LOCALAPPDATA\Programs\ocr-tb",
  [string] $Python = "python",
  [switch] $NoServer,
  [switch] $Force
)

$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Write-Step($message) { Write-Host "==> $message" -ForegroundColor Cyan }

Write-Step "Kiểm tra Python"
$cmd = Get-Command $Python -ErrorAction SilentlyContinue
if (-not $cmd) {
  Write-Error "Không tìm thấy '$Python'. Cài Python 3.10-3.13 từ https://www.python.org/downloads/ và chạy lại."
}
& $Python --version

$versionOk = & $Python -c "import sys; print(1 if (3,10) <= sys.version_info[:2] <= (3,13) else 0)"
if ($versionOk -ne "1") {
  Write-Error "Cần Python 3.10 - 3.13."
}

if (Test-Path $InstallDir) {
  if ($Force) {
    Write-Step "Xóa thư mục cài cũ: $InstallDir"
    Remove-Item -Recurse -Force $InstallDir
  } else {
    Write-Step "Thư mục đã tồn tại: $InstallDir (dùng -Force để cài lại)"
  }
}

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
$VenvPy = Join-Path $InstallDir "venv\Scripts\python.exe"

Write-Step "Tạo virtualenv"
& $Python -m venv (Join-Path $InstallDir "venv")

Write-Step "Nâng pip và cài OCR-TB"
& $VenvPy -m pip install --upgrade pip setuptools wheel | Out-Null
$spec = if ($NoServer) { $scriptDir } else { "$scriptDir[server]" }
& $VenvPy -m pip install $spec

$env:OCR_TB_HOME = $InstallDir
$env:OCR_TB_CACHE = Join-Path $InstallDir "models"

Write-Step "Ghi thông tin cài đặt (để ocr-tb update biết cập nhật thế nào)"
& $VenvPy -m ocr_tb record-install --method script --repo-dir $scriptDir --prefix $InstallDir | Out-Null

Write-Step "Tải model ONNX vào cache"
& $VenvPy -m ocr_tb models pull

$binDir = Join-Path $InstallDir "bin"
New-Item -ItemType Directory -Force -Path $binDir | Out-Null
$shim = Join-Path $binDir "ocr-tb.cmd"
@"
@echo off
"$VenvPy" -m ocr_tb %*
"@ | Set-Content -Path $shim -Encoding ASCII
Write-Step "Đã tạo lệnh: $shim"

Write-Host ""
Write-Host "Cài xong." -ForegroundColor Green
Write-Host "  Thêm vào PATH (cho phiên hiện tại):"
Write-Host "    `$env:Path += ';$binDir'"
Write-Host "  Thêm vĩnh viễn cho user:"
Write-Host "    [Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path','User') + ';$binDir', 'User')"
Write-Host ""
Write-Host "Kiểm tra nhanh:"
Write-Host "  & `"$shim`" info"
Write-Host "  & `"$shim`" solve .\samples"
Write-Host ""
Write-Host "Tesseract (tuỳ chọn, chỉ cho benchmark): winget install --id UB-Mannheim.TesseractOCR"