#!/bin/bash
# ETHConf 2026 New York 리포트 PDF 빌드
# 사용법: bash report/build.sh
set -e

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -x "$CHROME" ]; then
  echo "오류: Google Chrome을 찾을 수 없습니다 ($CHROME)"
  exit 1
fi

"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
  --virtual-time-budget=10000 \
  --print-to-pdf="$DIR/report.pdf" \
  "file://$DIR/report.html" 2>&1 | tail -1

echo "빌드 완료: $DIR/report.pdf"
