---
name: do-hot-pt
description: HOTPLX IR 형식의 네이비·러스트 IR 덱(HTML)을 생성. 960×540 고정 캔버스를 뷰포트에 맞춰 스케일하고 모바일에서는 리플로우+autofit, Pretendard, 네이비(#1B2A4A)·패널(#22335A) 다크 ↔ 화이트 라이트 교차 배경, 러스트(#9C4A34) 액센트. cover·profile·cards3·flow·duo·bm·metrics·table·divider 슬라이드 타입. 투자유치·IR·기업설명·사업계획 발표 요청 시 사용.
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

| 클래스 | 용도 | 배경 | 핵심 요소 |
|---|---|---|---|
| `t-cover` | 표지 | 다크 | `.brand`·`.cover-meta`·`.display`·`.grid-3`>`.card`×3·`.lead`·`.statement-bar` |
| `t-profile` | 팀·연혁 | 다크 | `.people`>`.person`(이름·역할·경력) + `.milestones`>`.ms`(연도·내용) |
| `t-cards3` | 3축 요약 | 양쪽 | `.grid-3` > `.card`(`.num` ①②③ + `.hairline` + `.accent` 정량근거) |
| `t-flow` | 4단계 흐름 | 다크 | `.flow` > `.step`×4 + `.arw`(자동 →/↓), 강조 단계에 `.on`·`.badge` |
| `t-duo` | 2축 대비·순환 | 양쪽 | `.duo-wrap` > `.pane`×2, 순환은 `.loop`(`.mark`로 ↓↺) |
| `t-bm` | 수익모델 | 라이트 | `.bm` > `.bm-col`(`.bm-head` 네이비 바 + `.bm-claim` + `.bm-row` 라벨·값, `.hot`으로 과금 강조) |
| `t-metrics` | 단가·시나리오 | 라이트 | `.metrics` 4열 그리드 (`.colhead`·`.rowlabel`·`.cell`, 합계행은 `.cell.total`) |
| `t-table` | 다년 추정 | 라이트 | `.tbl` (합계행 `.accent`, 가정은 `<caption>`) |
| `t-divider` | 섹션 구분 | 양쪽 | `.kicker`만 (APPENDIX 등) |

## 공통 컴포넌트

- `.kicker`(러스트 대문자 레터스페이스) · `h1` · `.display`(표지 전용) · `.lead`(한 문장 요약) · `.hairline`
- `.num`(①②③④, 러스트) · `.card`(`.card-title` + p + `.accent`) · `.badge`(러스트 알약)
- `.statement-bar` — 한 장에 하나. 안에서 `.hl`로 한 구절만 더 밝게
- `.fine` — 가정·각주(이탤릭 중앙)
- `.footer` 3분할(좌 로고 · 중앙 캡션 · 우 페이지번호) — **모든 슬라이드에 필수**

## 빌드 절차

1. **스켈레톤 복사**: `assets/pt3-skeleton.html`을 작업 위치로 복사.
2. **`<style>`·`<script>`·`.deck`·`.canvas`는 건드리지 않는다.** (형식의 핵심)
3. `.deck` 안 `<section>`을 주제에 맞는 타입으로 재구성. 스켈레톤의 동일 타입을 복제해 텍스트만 교체.
4. 표지 → 팀·시장 → 제품 → 경쟁우위 → 수익모델 → 수치 → `t-divider` → 부록 순. **한 슬라이드 = 한 메시지.**
5. `.is-dark`/`.is-light`를 교차 배치. 각 `<div class="canvas">`의 `data-title`은 우측 dots 툴팁이 된다.
6. `.footer` 페이지번호를 `01`…`N`으로, `<title>`·표지 텍스트를 주제에 맞게.
7. **저장**: `<주제>_IR.html`.
8. **렌더 검증** — 눈으로 본다. 오라클 없이 "잘 나왔다"고 하지 않는다:
   ```bash
   CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   "$CHROME" --headless --disable-gpu --window-size=1120,700 \
     --screenshot=out.png "file://$PWD/<주제>_IR.html"
   ```
9. **모바일 확인**: headless Chrome은 `--window-size`에 **최소 너비 500px을 강제**한다. 390px을 재려면 `<iframe width=390 height=844>`로 감싼 페이지를 렌더한다. 넘치면 **문장을 줄인다** — CSS를 손대지 않는다.

## 원칙

- 정보 밀도: `.lead` 1문장, `.card p` 2줄 이내, `li` 짧게. 고정 캔버스라 넘치면 잘린다 — **글자 수를 줄이지, 폰트를 줄이지 않는다.**
- 제목은 `<br>`로 의미 단위 2줄까지. 한글 줄바꿈은 `word-break: keep-all`이 처리.
- 수치 슬라이드에는 반드시 `.fine`으로 가정을 밝힌다. IR에서 가정 없는 숫자는 신뢰를 깎는다.
- 다크는 구조·권위(표지·팀·제품·경쟁우위), 라이트는 계산·검증(수익모델·추정·부록)에 쓴다.
- 인터넷 필요(Pretendard CDN). 오프라인 배포 시 woff2 로컬 임베드.

## 함정 (실제로 겪은 것)

- **`transform: rotate()`를 모바일 화살표에 쓰지 않는다.** 트랜스폼은 scrollable overflow 영역에 잡혀, 안 넘치는 슬라이드를 autofit이 8px까지 끝없이 줄인다. 화살표 글자는 `::before { content }`로 바꾼다.
- **`.body`의 flex-shrink를 0으로 유지한다**(`flex: 1 0 auto`). `flex: 1`(=`1 1 0`)이면 내용이 넘칠 때 body가 찌그러지고 내용이 헤더·푸터 **위에 겹쳐 그려질 뿐** 캔버스 `scrollHeight`가 커지지 않는다. autofit이 넘침을 못 보고 그냥 통과시킨다.
- **`scrollHeight`만으로 판정하지 않는다.** 위 두 경우 모두 `scrollHeight`는 정상이라고 답했고, 실제로 렌더해 보고서야 h1이 잘린 것이 드러났다. 반환값이 아니라 결과물을 본다.

## 참고

- 원형: `HOTPLX_IR_short_최종.html` (0016 HOTPL AI Store DNA / 자료/HOTPLX)
- 자매 스킬: `/do-genpt`(에디토리얼) · `/do-report`(A4 PDF)
