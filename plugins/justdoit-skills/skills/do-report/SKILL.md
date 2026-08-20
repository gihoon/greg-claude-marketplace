---
name: do-report
description: >-
  Create an institutional research report as an A4 PDF (JP Morgan / 미래에셋 급 기관 리서치 수준).
  Use this whenever the user asks to write/build a research report, market report, 리포트, 보고서, or 참관/현장 리포트.
  Structure: cover, Table of Contents, Executive Summary (take-aways), chapters with "View" insight boxes,
  comparison tables, pullquotes, disclaimer boxes; Pretendard for Korean and Source Serif 4 (serif body) +
  Inter (sans headings, Wall-Street style) for English; auto-injected header/footer; rendered to PDF via
  Chrome headless with locally embedded woff2 fonts.
---

# 기관 리서치 리포트 디자인

이 스킬은 기관용 리서치 리포트(A4 PDF)를 생성한다. 완성된 디자인 자산
(`design-system.css`, 폰트 woff2, 로고, `build.sh`, HTML 골격)이 이 스킬의 `assets/`에 번들돼 있다.

- 스킬 자산 경로: `~/.claude/skills/do-report/assets/`
- 레퍼런스 구현: `~/git/jk-report/20260608 ETHConf NewYork - Report/` (있다면 실제 완성본 참고)

---

## 1. 빠른 시작 (새 리포트 생성)

리포트는 **자신의 폴더 하나**에 들어간다. 아래로 디자인 자산을 복제하고 골격에서 시작한다.

```bash
SK=~/.claude/skills/do-report/assets
DEST="<리포트 폴더>"                       # 예: "20260608 ETHConf NewYork - Report"
mkdir -p "$DEST/report/assets/fonts" "$DEST/images" "$DEST/docs"
cp "$SK/design-system.css" "$SK/build.sh"      "$DEST/report/"
cp "$SK/fonts/"*.woff2                          "$DEST/report/assets/fonts/"
cp "$SK/images/"*.png                           "$DEST/images/"
cp "$SK/report-skeleton.html"                   "$DEST/report/report.html"   # 골격에서 시작
```

그다음 `report/report.html`의 `[플레이스홀더]`를 실제 내용으로 채운다(구성은 4절). 빌드는 5절.

## 2. 디자인 시스템 (`design-system.css` — 그대로 사용)
- **색**: `--blue-primary:#1C60EF`(강조·제목), `--blue-deep:#1B4FD6`(표 행 헤더), `--blue-tint:#EAF1FE`(표 셀), `--blue-tint-2:#F5F8FF`(View 박스), `--ink:#141414`(본문), `--gray-footer:#9AA0A6`.
- **페이지 모델 (핵심)**: `@page A4 margin0`; `.page`는 `210×297mm + overflow:hidden + page-break-after:always` → **1 섹션 = 정확히 1 PDF 페이지**. `.page-body`는 `top26/left·right22/bottom24mm` 절대배치. 표지는 별도 `.cover`.
- **머리말·꼬리말**: HTML 하단 `<script>`가 각 `.page`에 자동 주입 — 좌상단 로고 + 우상단 페이지번호(#555), 하단 카피라이트(우측정렬) + 로고. **표지 제외, Writers=2부터** 번호.
- **타이포**: `h1.chapter` 21pt/800/blue · `h2.section` 13.5pt/800 · `p` 10.5pt/lh1.78/justify.

## 3. 폰트 (가변 woff2 **로컬 임베딩** — 오프라인 빌드, CDN 금지)
- **한국어판**: Pretendard (design-system.css의 `@font-face`가 `assets/fonts/PretendardVariable.woff2` 사용 — 자동).
- **영문판**: 본문 **Source Serif 4**(세리프) + 제목·표·UI **Inter**(산세리프) = 월스트리트 리서치 톤.
  `report_english.html`의 `<head>`에 골격 주석의 `<style>` 블록을 넣으면 적용된다(`@font-face` 3개 + body 세리프/제목 Inter 오버라이드 + 이름 고정폭).
- ⚠️ **표지 글자에 `text-shadow` 금지** — Chrome print-to-pdf가 그림자를 글자 배경처럼 칠해 **검정 박스**로 보인다. 가독성은 표지 배경 네이비 오버레이로 확보.

## 4. 표준 구성 (페이지 순서 — 골격 `report-skeleton.html`에 모두 포함)
1. **표지(cover)** — 다크블루 그라데이션 또는 배경 사진(+네이비 오버레이). 제목/부제/발행월/`dsrv.com`.
2. **Writers** — 제목 + 작성자(이름+직책) + 면책 박스(`.disclaimer`).
3. **목차(Table of Contents)** — dotted leader + 페이지번호.
4. **Executive Summary** — 5개 take-away(`.takeaway`: 번호+제목+본문).
5. **본문 챕터** — `h1.chapter`/`h2.section`. 컴포넌트: 비교표(`table.compare`), 그림(`.figure`+img+`.caption`), 풀쿼트(`.pullquote`), 주석(`.note`), 그리고 **각 챕터·세션 끝에 `.view-box` 박스**(해석·시사점).
6. **Business Contact** — 제목/이메일/로고/URL/면책 박스(본문 폭 `left:0;right:0`, 하단에 붙임).

## 5. 빌드 & 필수 점검
```bash
cd "<리포트 폴더>/report" && bash build.sh        # → report.pdf
# 다른 파일명(영문판 등):
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=10000 \
  --print-to-pdf="<원하는 파일명>.pdf" "file://$PWD/<html파일>"
```
빌드 직후 **반드시**:
1. **overflow 점검** — `.page`는 넘치면 잘린다. 넘치는 섹션은 `…</div></section>` + `<section class="page"><div class="page-body">…`로 **분리**.
2. **목차 페이지번호 동기화** — 섹션=1페이지이므로 각 제목의 섹션 순번(+표지)으로 `.pno`를 맞춘다. (제목 텍스트 기준 목차 자동 재생성 스크립트 권장)
3. PDF 페이지를 이미지로 읽어 표지·목차·표·View 박스가 깨지지 않았는지 시각 확인.

## 6. 사진·캡션
- 사진은 사용자 제공(HEIC 등). `sips -s format jpeg in.heic --out out.jpg && sips -Z 2400 out.jpg` 로 변환·리사이즈 후 `images/`에 두고 `<img>`로 삽입.
- 인물 캡션: **"세션명 — (우측:) 이름 at 회사 (직책)"** (이름·소속·직책 3요소).

## 7. 집필 원칙
- 절제된 분석체. 미검증·상충 수치는 "발표자 주장/사례"로 귀속하고 `.note`로 균형. AI 티 단어(관통/렌즈/날것/함의) 회피.
- 면책은 "자유 공유·인용 가능, 단 출처 표기"로 통일.
- 영문판은 직역이 아닌 **기관 리서치 영문체**; 인명 로마자는 사용자 확인; 영어는 길어 페이지가 밀리므로 overflow·목차 재점검.

## 8. 번들 자산 목록 (`assets/`)
- `design-system.css` — 디자인 시스템 전체
- `build.sh` — Chrome headless PDF 빌드
- `report-skeleton.html` — 표준 구성 + 모든 컴포넌트 예시 + 영문 폰트 `<style>` 주석 + 머리말/꼬리말 JS
- `fonts/` — PretendardVariable / Inter / SourceSerif4 / SourceSerif4-Italic (woff2)
- `images/` — 로고 이미지 (favicon dark·light, master dark·light) — 실제 사용할 로고 파일로 교체
