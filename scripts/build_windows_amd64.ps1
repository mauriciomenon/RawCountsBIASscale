$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")

if (-not $IsWindows) {
    throw "Run this script on Windows 11 amd64."
}

if ($env:PROCESSOR_ARCHITECTURE -notin @("AMD64", "x86_64")) {
    throw "Run this script on Windows 11 amd64."
}

uv run --extra build python -m nuitka `
  --standalone `
  --assume-yes-for-downloads `
  --enable-plugin=tk-inter `
  --windows-console-mode=disable `
  --product-name="SCADA Analog Scaling Calculator" `
  --file-version=1.1 `
  --product-version=1.1 `
  --output-dir=dist/nuitka/windows-amd64 `
  --remove-output `
  indicador.py
