#!/usr/bin/env bash
# Local development only: bind explicitly to this computer's loopback address.
set -euo pipefail

preview_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$preview_root"

if command -v quarto >/dev/null 2>&1; then
  preview_quarto="$(command -v quarto)"
elif [[ -x /private/tmp/yanxu-quarto/bin/quarto ]]; then
  preview_quarto=/private/tmp/yanxu-quarto/bin/quarto
else
  printf '%s\n' 'Install Quarto first: https://quarto.org/docs/get-started/' >&2
  exit 1
fi

python3 scripts/render_profile.py
exec "$preview_quarto" preview --render all --host 127.0.0.1 --port 4321 --no-browser
