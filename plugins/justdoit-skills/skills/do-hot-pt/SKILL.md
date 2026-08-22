---
name: do-hot-pt
description: HOTPLX IR 형식의 네이비·러스트 IR 덱(HTML)을 생성. 960×540 고정 캔버스를 뷰포트에 맞춰 스케일하고 모바일에서는 리플로우+autofit, Pretendard, 네이비(#1B2A4A)·패널(#22335A) 다크 ↔ 화이트 라이트 교차 배경, 러스트(#9C4A34) 액센트. 표지·팀연혁(원형사진+타임라인)·통계패널·4단계 흐름·원형번호 카드·경쟁대비 패널·순환루프·수익모델·단가표·로드맵Gate·누적막대차트·다년추정표 14종 레이아웃. 투자유치·IR·기업설명·사업계획 발표 요청 시 사용.
---

# do-hot-pt — 네이비 러스트 IR 덱 생성

투자유치·기업설명을 **IR 덱 수준의 HTML 프레젠테이션**으로 만든다. `HOTPLX_IR_short_최종.html`에서 추출한 디자인 시스템.

## 트리거

`/do-hot-pt` 또는 IR·투자유치·기업설명·사업계획 발표 요청

## 언제 쓰나

- 투자자·심사역에게 보내는 덱 — 수익모델·재무추정·팀·시장 구조가 들어갈 때
- (구분) `/do-genpt` = 흑백 에디토리얼 세로 흐름 · **`/do-hot-pt` = 네이비 러스트 IR** · `/do-report` = A4 PDF 리포트

## 형식 (핵심 — 임의 변경 금지)

- **고정 960×540 캔버스**: 모든 수치는 디자인 px 기준. `.canvas`를 `transform: scale(--k)`로 뷰포트에 맞춘다(JS 계산). 16:9가 어디서나 유지된다.
- **다크 ↔ 라이트 교차가 이 형식의 리듬**: 네이비 `#1B2A4A`(표지·팀·제품·구조·경쟁우위) ↔ 화이트(수익모델·수치·부록). `.is-dark`/`.is-light`가 토큰을 통째로 뒤집는다. **연속 3장 같은 배경 금지.**
- **러스트 규칙**: `#9C4A34`는 양쪽 배경에서 그대로 액센트. 키커·번호·강조 수치·강조바에 쓴다.
- **강조바는 한 슬라이드에 하나**: `.statement-bar`. 다크에서는 러스트, 라이트에서는 네이비 배경. 남발하면 위계가 죽는다.
- **타이포**: Pretendard(CDN). 표지 2em / 제목 1.5em / 리드 .875em / 카드 .9375em / 본문 .75em / 키커 .6875em.
- 색·타입스케일·좌표는 `assets/pt3-skeleton.html`의 `<style>`에 정의됨 — **그대로 유지한다.**

## 모바일 (스켈레톤이 자동 처리 — 손댈 필요 없음)

`≤980px`에서 고정 캔버스를 풀고 세로 리플로우 + autofit. 슬라이드 1장이 화면 1페이지에 들어온다.

**이 스켈레톤의 모든 치수는 `.canvas`의 base font-size에 대한 `em`이다.** `fitMobile()`이 넘치는 캔버스의 base를 15px → 8px까지 0.25씩 줄이면 전체가 따라 줄어든다. 그래서 "px를 em으로 덮어야 하는" 작업이 아예 없다.

> ⚠️ **새 컴포넌트를 추가할 때도 `em`만 쓴다.** 절대 px 크기를 하나라도 넣으면 그 서브트리만 축소를 무시해 autofit이 통째로 실패한다(폰트를 줄여도 높이가 안 줄어듦). 테두리 `1px`만 예외.

## 슬라이드 타입 (마크업은 `assets/pt3-skeleton.html` — 복제해서 텍스트만 교체)

스켈레톤은 **HOTPLX TIPS IR 14장 전체**다. 만들 슬라이드와 같은 성격의 장을 통째로 복제해 텍스트만 갈아끼운다.

| 스켈레톤 장 | 용도 | 배경 | 핵심 요소 |
|---|---|---|---|
| 01 | 표지 | 다크 | `.wm.cover` 워드마크 · `.kicker` · `h1` · `.grid3`>`.card`×3 · `.lead` · `.statement-bar` |
| 02 | 팀·연혁 | 라이트 | `.pcard`(`.ph` 원형 사진 + `.nm`/`.rl`/`ul`/`.tagline`) + `.tl`>`.it`(`.hot`으로 러스트 점) + `.softbar` |
| 03 | 자산·확산 | 라이트 | `.statpanel`(대형 수치) + `.chain`>`.lnk`(`.on` 강조) + `.dn` 화살표 |
| 04 | 4단계 흐름 | 다크 | `.flow`>`.step`×4 + `.arw`, 강조 단계에 `.on` |
| 05 | 3축 요약 | 라이트 | `.grid3`>`.card` + `.nc`(원형 번호) + `.tintbox`(`.hot`) |
| 06 | 경쟁 대비 | 라이트 | `.grid2`>`.panelbox`(`.navy`) + `.stack`>`.bx`(`.on`) |
| 07 | 순환 루프 | 다크 | `.grid2`>`.panelbox` + `.pill`(`.soft`) + ↓↺ 리스트 |
| 08 | 수익모델 | 라이트 | `.bm`>`.bm-col`(`.bm-head`·`.bm-claim`·`.bm-row.hot`) |
| 09 | 단가·시나리오 | 다크 | `.metrics` 4열 그리드 (`.colhead`·`.rowlabel`·`.cell.total`) |
| 10 | 로드맵·Gate | 라이트 | `.grid3.r`>`.panelbox` + `.pill`(`.navy`) + `.tintbox` |
| 11 | 섹션 구분 | 라이트 | `.kicker`만 (APPENDIX) |
| 12 | 누적 막대 차트 | 다크 | `.chart`>`.col`>`.seg`(`.s1`~`.s4`) + `.legend` + `.sidecard` |
| 13 | 다년 추정 표 | 라이트 | `.otbl`(`tr.tot` 네이비 합계 · `tr.tot2` 러스트 합계 · `tr.thin` 가정행) |
| 14 | 경쟁 비교 표 | 라이트 | `.otbl` + `td.hl`(자사 열 틴트) + `td.sub`(이탤릭 보조행) |

## 공통 컴포넌트

- `.kicker`(러스트 대문자) · `h1` · `.lead` · `.fine`(가정·각주, 이탤릭 중앙)
- `.nc` 원형 번호 배지 — **안에는 원문자(①)가 아니라 숫자(1)를 넣는다.** `.nc.rust`로 러스트
- `.pill` 알약 라벨 — `.navy` / `.soft` 변형
- `.tintbox` 카드 안 연파랑 강조 박스 · `.softbar` 얇은 보조 바
- `.statement-bar` — **한 장에 하나.** 안에서 `.hl`로 한 구절만 더 밝게
- `.wm` 워드마크 — `.cover`(표지) · `.br`(좌하단, 라이트 슬라이드) · `.tr`(우상단, 다크 슬라이드).
  스켈레톤은 `.wmtext` 텍스트 자리표시이며, 실제 덱에서는 `<img src="data:image/png;base64,…">`로 교체한다
- `.ph` 인물 사진 자리표시 — 실제 덱에서는 base64 `<img>`로 교체 (원형·러스트 링)
- `.footer` 3분할(좌 로고/캡션 · 중앙 캡션 · 우 페이지번호) — **모든 슬라이드에 필수**
## 빌드 절차

1. **스켈레톤 복사**: `assets/pt3-skeleton.html`을 작업 위치로 복사.
2. **`<style>`·`<script>`·`.deck`·`.canvas`는 건드리지 않는다.** (형식의 핵심)
3. `.deck` 안 `<section>`을 재구성한다. 성격이 같은 장을 **통째로 복제해 텍스트만 교체**한다.
   슬라이드는 `<div class="canvas is-dark|is-light" data-title="…">` 하나로 시작하며, 레이아웃은 안쪽 컴포넌트가 결정한다.
4. 표지 → 팀·연혁 → 자산 → 제품 → 경쟁 → 수익모델 → 수치 → APPENDIX 구분 → 부록 순. **한 슬라이드 = 한 메시지.**
5. `.is-dark`/`.is-light`를 교차 배치. 각 `<div class="canvas">`의 `data-title`은 우측 dots 툴팁이 된다.
6. `.footer` 페이지번호를 `01`…`N`으로, `<title>`·표지 텍스트를 주제에 맞게.
7. **저장**: `<주제>_IR.html`.
8. **렌더 검증** — 눈으로 본다. 오라클 없이 "잘 나왔다"고 하지 않는다:
   ```bash
   CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   "$CHROME" --headless --disable-gpu --window-size=1120,700 \
     --screenshot=out.png "file://$PWD/<주제>_IR.html"
   ```
9. **넘침 측정** — 위 「함정」의 두 식(`body 내부 넘침`·`푸터 침범`)을 14장 전부에 돌린다. 눈으로만 보면 놓친다.
10. **모바일 확인**: headless Chrome은 `--window-size`에 **최소 너비 500px을 강제**한다. 390px을 재려면 `<iframe width=390 height=844>`로 감싼 페이지를 렌더한다. 넘치면 **문장을 줄인다** — 폰트를 줄이지 않는다.

## 원칙

- 정보 밀도: `.lead` 1문장, `.card p` 2줄 이내, `li` 짧게. 고정 캔버스라 넘치면 잘린다 — **글자 수를 줄이지, 폰트를 줄이지 않는다.**
- 제목은 `<br>`로 의미 단위 2줄까지. 한글 줄바꿈은 `word-break: keep-all`이 처리.
- 수치 슬라이드에는 반드시 `.fine`으로 가정을 밝힌다. IR에서 가정 없는 숫자는 신뢰를 깎는다.
- 다크는 구조·권위(표지·팀·제품·경쟁우위), 라이트는 계산·검증(수익모델·추정·부록)에 쓴다.
- 인터넷 필요(Pretendard CDN). 오프라인 배포 시 woff2 로컬 임베드.

## 함정 (실제로 겪은 것)

- **`scrollHeight` 로 넘침을 판정하지 않는다.** `.body`는 데스크톱에서 `flex:1`(=`1 1 0`)이라 내용이 넘치면
  body가 찌그러지고 내용이 **푸터 위에 겹쳐 그려질 뿐** `scrollHeight`는 정상이라고 답한다.
  반드시 아래 두 가지를 함께 재고, 하나라도 걸리면 **문장을 줄인다**:
  ```js
  const over = body.scrollHeight - body.clientHeight;          // ① body 내부 넘침
  const collide = contentBottom - footer.getBoundingClientRect().top;  // ② 푸터 침범
  ```
- **새로 만든 그리드는 모바일에서 저절로 접히지 않는다.** `.grid2`/`.grid3` 같은 컴포넌트를 추가하면
  `@media (max-width:980px)`에 `grid-template-columns:1fr !important`를 반드시 같이 넣는다.
  안 넣으면 우측 열이 화면 밖으로 잘려나가는데 세로 autofit은 이를 못 잡는다.
- **`.wm` 절대배치 워드마크도 모바일에서 `position:static`으로 풀어준다.**
- **원형 번호 배지 안에는 숫자를 넣는다.** `①`을 넣으면 원 안에 작은 원이 하나 더 그려진다.
- **`transform: rotate()`를 모바일 화살표에 쓰지 않는다.** 트랜스폼이 scrollable overflow에 잡혀
  안 넘치는 슬라이드를 autofit이 8px까지 끝없이 줄인다. 화살표는 `::before { content }`로 넣는다.

## 참고

- 원형: `HOTPLX_TIPS_IR_tech_business_v3.pdf` — 스켈레톤은 이 PDF 14장을 HTML로 재현한 것이다
  (0016 HOTPL AI Store DNA / 0016p. TIPS IR 개발 실행)
- 자매 스킬: `/do-genpt`(에디토리얼) · `/do-hot-report`(A4 1p) · `/do-hot-pdf`(PDF 렌더)
