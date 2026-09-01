#!/usr/bin/env bash
# do-hotpdf — HTML → PDF 렌더
#
#   bash build.sh <input.html> [out.pdf]
#
# 입력 HTML을 보고 두 모드 중 하나로 렌더한다.
#   문서 모드: `.sheet`(A4 210×297mm)  → 시트 1장 = 세로 1페이지. 원본 그대로 인쇄.
#   덱   모드: `.canvas`(960×540 고정) → 슬라이드 1장 = 가로 1페이지. 스크롤·스케일을
#              푸는 인쇄 CSS를 임시 사본에 주입한다(원본 HTML은 건드리지 않는다).
set -euo pipefail

IN="${1:?usage: build.sh <input.html> [out.pdf]}"
OUT="${2:-${IN%.html}.pdf}"
CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
[ -x "$CHROME" ] || { echo "Chrome 없음: $CHROME (CHROME=... 로 지정)" >&2; exit 1; }

SRC="$(cd "$(dirname "$IN")" && pwd)/$(basename "$IN")"
TMP=""

if grep -q 'class="canvas' "$SRC"; then
  echo "· 덱 모드 (960×540 → 가로 페이지)"
  TMP="${SRC%.html}.__print__.html"
  # </head> 앞에 인쇄 CSS 주입. 960×540px @96dpi = 254 × 142.875mm
  awk '/<\/head>/ && !done {
    print "<style>@media print{"
    print "  @page{size:254mm 142.875mm;margin:0}"
    print "  html,body{background:#fff;height:auto;overflow:visible;scroll-snap-type:none}"
    print "  .slide{height:auto;min-height:0;display:block;overflow:visible;page-break-after:always;scroll-snap-align:none}"
    print "  .slide:last-child{page-break-after:auto}"
    print "  .canvas{transform:none!important;box-shadow:none;margin:0 auto}"
    print "  .dots,.nav,.progress{display:none!important}"
    print "}</style>"
    done=1
  } {print}' "$SRC" > "$TMP"
  SRC="$TMP"
else
  echo "· 문서 모드 (A4 세로)"
fi

"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=10000 --print-to-pdf="$OUT" "file://$SRC" 2>/dev/null

[ -n "$TMP" ] && rm -f "$TMP"

PAGES=$(python3 - "$OUT" <<'PY'
import sys
d = open(sys.argv[1], 'rb').read()
print(d.count(b'/Type /Page') - d.count(b'/Type /Pages'))
PY
)
echo "→ $OUT ($PAGES 페이지)"
