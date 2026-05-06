#!/usr/bin/env bash
set -euo pipefail

target="${1:-}"
cd "$(dirname "$0")/.."

case "$target" in
  macos-arm64)
    check_system="Darwin"
    check_machines="arm64"
    output_dir="dist/nuitka/macos-arm64"
    bundle_args=(--macos-create-app-bundle)
    ;;
  debian-trixie-amd64)
    check_system="Linux"
    check_machines="x86_64 AMD64"
    output_dir="dist/nuitka/debian-trixie-amd64"
    bundle_args=()
    ;;
  debian-trixie-arm64)
    check_system="Linux"
    check_machines="aarch64 arm64"
    output_dir="dist/nuitka/debian-trixie-arm64"
    bundle_args=()
    ;;
  *)
    echo "Usage: $0 {macos-arm64|debian-trixie-amd64|debian-trixie-arm64}" >&2
    exit 2
    ;;
esac

python - "$check_system" "$check_machines" "$target" <<'PY'
import platform
import sys

expected_system = sys.argv[1]
expected_machines = set(sys.argv[2].split())
target = sys.argv[3]

if platform.system() != expected_system or platform.machine() not in expected_machines:
    raise SystemExit(f"Run this script on {target}.")
PY

uv run --extra build python -m nuitka \
  --standalone \
  --assume-yes-for-downloads \
  --enable-plugin=tk-inter \
  --product-name="SCADA Analog Scaling Calculator" \
  --file-version=1.1 \
  --product-version=1.1 \
  --output-dir="$output_dir" \
  --remove-output \
  "${bundle_args[@]}" \
  indicador.py
