#!/usr/bin/env bash
# ============================================================
# Render any HTML → PDF using headless Chromium (16:9, 1280x720).
#
# Usage:
#   ./render.sh <input.html> [output.pdf]
#
# Looks for the HTML file in slides/<week>/, computes the absolute
# file:// URL, and writes the PDF next to the HTML.
# ============================================================
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <input.html> [output.pdf]" >&2
  exit 1
fi

INPUT="$1"
OUTPUT="${2:-${INPUT%.html}.pdf}"

# Resolve absolute path (no symlink resolution, so file:// works)
ABS_INPUT="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"

# Make the PDF path absolute too, anchored next to the HTML
ABS_OUTPUT="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$OUTPUT")"

echo "→ Rendering: file://$ABS_INPUT"
echo "→ Output:    $ABS_OUTPUT"

chromium \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --hide-scrollbars \
  --no-pdf-header-footer \
  --print-to-pdf="$ABS_OUTPUT" \
  --virtual-time-budget=10000 \
  "file://$ABS_INPUT" 2>&1 | tail -5

if [[ -s "$ABS_OUTPUT" ]]; then
  echo "✓ OK: $(ls -lh "$ABS_OUTPUT" | awk '{print $5}')"
else
  echo "✗ Failed to produce PDF" >&2
  exit 1
fi