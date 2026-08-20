---
name: do-genpt
description: agent_payments_PT.html 형식의 에디토리얼 슬라이드 덱(HTML)을 생성. 스크롤-스냅 풀뷰포트 슬라이드, Pretendard, 종이 질감·inset 프레임, cover·cards3·timeline·compare·revenue·end 등 슬라이드 타입. 모바일에서는 슬라이드 1장이 화면 1페이지에 자동으로 맞춰진다. 발표자료·PT·슬라이드·피치덱 요청 시 사용.
---

# Report-PT — 에디토리얼 슬라이드 덱 생성

기획·전략·리서치 내용을 **기관 발표 수준의 HTML 프레젠테이션**으로 만든다. `agent_payments_PT.html`과 동일한 에디토리얼 덱 형식.

## 트리거

`/do-genpt` 또는 `PT`, `발표자료`, `슬라이드`, `피치덱` 요청

## 언제 쓰나

- 전략·기획·리서치를 슬라이드 덱으로 발표해야 할 때
- (구분) `/do-report` = A4 PDF 기관 리포트 · **`/do-genpt` = 화면 발표용 HTML 슬라이드 덱**

## 형식 (핵심 — 임의 변경 금지)

- **스크롤-스냅 풀뷰포트 덱**: 각 슬라이드 = 100vw×100vh, `scroll-snap-type: y mandatory`. 마우스 스크롤·방향키·PgUp/PgDn·Home/End로 이동.
- **에디토리얼 종이 미학**: 웜 그레이 배경 `#f4f3ef`, 종이색 슬라이드 `#fbfaf7`, 슬라이드마다 inset 얇은 테두리 프레임(`.slide::before`), 블랙 강조.
- **타이포**: Pretendard(CDN). h1 `clamp(52~78px)` 초굵게(840)·음수 자간, `word-break: keep-all`.
- **우측 progress dots** + 좌하단 nav-hint + 키보드 네비 = `<script>`가 자동 생성.
- **모바일 = 슬라이드 1장이 화면 1페이지**(아래 참조) — 스켈레톤이 자동 처리.
- 색·폰트·레이아웃은 `assets/pt-skeleton.html`의 `<style>`·`<script>`에 이미 정의됨 — **그대로 유지한다.**

## 모바일 대응 (스켈레톤이 자동 처리 — 손댈 필요 없음)

`≤980px`에서 각 슬라이드가 **스크롤 없이 화면 한 장에 들어온다.** 데스크톱 렌더링은 영향 없음.

- 모바일 모든 크기는 `.slide`의 base `font-size`에 대한 **`em`으로 정의**되고, `fitMobile()`이 넘치는 슬라이드만 15px → 8px까지 0.25씩 줄여 맞춘 뒤 세로 가운데 정렬한다.
- 높이는 `100dvh` — 모바일 주소창 숨김/표시에 따른 잘림 방지.
- 표(`.plain-table`)는 행 단위 세로 적층, 5·6열 그리드는 2열, 다이어그램(`.flow-area`·`.channel-grid`·`.layer`)은 1열로 전환.

> ⚠️ **새 컴포넌트를 추가하면 절대 px 폰트를 모바일 블록에서 `em`으로 반드시 덮을 것.**
> 안 덮으면 그 서브트리만 축소를 무시해 **autofit이 통째로 실패한다**(폰트를 아무리 줄여도 높이가 안 줄어듦).
> 실제 사고 사례: `.plain-table { font-size: 20px }`를 안 덮어 표 슬라이드가 8px에서도 계속 넘쳤다.

## 슬라이드 타입 (실제 마크업은 `assets/pt-skeleton.html`에 있음 — 복제해서 텍스트만 교체)

| 클래스 | 용도 | 핵심 요소 |
|---|---|---|
| `slide-cover` | 표지 | `.kicker` · `h1` · `.lead` · `.footer` |
| `slide-cards3` | 3분할 카드 | `h2` · `.statement` · `.grid.grid-3` > `.card` ×3 |
| `slide-split_cards` | 대비(좌↔우) | `.split-arrow` > `.panel` · `.bridge` · `.panel` |
| `slide-compare` | 2열 비교 | `.compare-wrap` > `.panel` ×2 |
| `slide-timeline4` | 4단계 로드맵 | `.timeline4` > `.phase` ×4 (`.phase-no`·`.phase-head`·p) |
| `slide-bullets_table` | 항목 표 | `.plain-table` (th 24% 라벨 · td 설명) |
| `slide-steps6` | 6단계 흐름 | 단계 그리드 |
| `slide-*_diagram` | 다이어그램 | `gateway` · `channel` · `monitoring` · `network_stack` |
| `slide-revenue` | 수익·지표 | 강조 수치 |
| `slide-end` | 마무리 | `.kicker` "End" · `h1` "END" · `.lead` |

## 공통 컴포넌트

- `.kicker`(대문자 라벨) · `h1`/`h2`/`h3` · `.lead`(부제) · `.statement`(핵심 문장, 굵게)
- `.grid.grid-3` + `.card`(`.card-title` + p)
- `.panel`(`.panel-label` + ul/li) · `.bridge`(가운데 연결어)
- `.plain-table`(왼쪽 th 라벨 + td 설명)
- `.footer`(좌: 섹션/발표자, 우: `N / total` 페이지) — **모든 슬라이드에 필수**

## 빌드 절차

1. **스켈레톤 복사**: `assets/pt-skeleton.html`을 작업 위치로 복사.
2. **`<style>`·`<script>`·`.deck` 래퍼는 건드리지 않는다.** (형식의 핵심)
3. **`.deck` 안 `<section class="slide ...">` 들을 주제 내용으로 교체.** 위 타입에서 골라, 스켈레톤의 동일 타입 슬라이드를 복제해 텍스트만 바꾼다.
4. 표지(`slide-cover`) → 본문 슬라이드들 → 마무리(`slide-end`) 순. **한 슬라이드 = 한 메시지.**
5. **모든 슬라이드 `.footer` 갱신**: 좌측 = 발표 제목/발표자, 우측 = `01 / N` … `N / N`(총 장수 일치).
6. `<title>`·표지 `h1`·`.kicker`를 주제에 맞게.
7. **저장**: `<주제>_PT.html` (예: `baaam_PT.html`).
8. **열기**: 브라우저로 확인. PDF가 필요하면 브라우저 인쇄(가로·배경 그래픽 켜기).
9. **모바일 확인**: 창을 좁히거나(≤980px) 개발자도구 기기 모드로 **모든 슬라이드가 스크롤 없이 한 화면에 들어오는지** 본다. 넘친다면 그 슬라이드의 내용이 과밀한 것이므로 **문장을 줄인다** — CSS를 손대지 않는다.

## 원칙

- 한글은 `word-break: keep-all`(스켈레톤 CSS가 처리) — 어색한 줄바꿈 방지.
- 정보 밀도: `.statement` 1~2문장, `.card` p 1~2줄, `li` 짧게. 슬라이드당 과밀 금지.
- 색·폰트·간격 임의 변경 금지 — 일관성이 이 형식의 가치.
- 인터넷 필요(Pretendard CDN). 오프라인 배포 시 폰트 로컬 임베드 고려.

## 참고

- 원형: `agent_payments_PT.html` (0023 스킬 통합 전략)
- 자매 스킬: `/do-report`(A4 PDF 기관 리포트)
