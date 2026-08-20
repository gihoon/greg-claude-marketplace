# greg-claude-marketplace

Greg의 Claude Code 스킬 패키지. 지식을 쌓고 → 아이디어로 다듬고 → 결과물로 만들고 → 검증·자동화하는 20개 스킬.

> **출처**: [kimyoon21/brown-claude-marketplace](https://github.com/kimyoon21/brown-claude-marketplace) · [vibelabs.kr/shared/8](https://vibelabs.kr/shared/8)

---

## 설치

```bash
/plugin marketplace add https://github.com/gihoon/greg-claude-marketplace
/plugin install justdoit-skills@greg-claude-marketplace
```

업데이트: `/plugin update justdoit-skills@greg-claude-marketplace`

---

## 전체 흐름

```
아이디어 떠오름
  │
  ├─ 메모로 남기기 ──→ /do-fleeting → /do-literature → /do-permanent → /do-wiki   (지식 축적)
  │                                  └→ /do-index /do-query /do-lint  (탐색·점검)
  │
  ├─ 지식을 제품으로 ─→ /do-sharpen → /do-productify              (실행 계획)
  │
  ├─ 발표·리포트로 ────→ /do-genpt · /do-report         (슬라이드 · PDF)
  │
  └─ 검증·자동화 ──────→ /do-critique · /do-research · /do-decide
                          /do-ingest · /do-relink · /do-refactor
                          /do-breakdown · /do-compile
```

---

## 볼트 준비 (지식관리 스킬 전제조건)

지식관리 스킬(`/do-fleeting` `/do-permanent` 등)을 쓰려면 옵시디언 볼트가 아래 구조여야 한다.

```
볼트 루트/
├── 0 raw/            ← /do-fleeting 저장 위치
├── 1 wiki/           ← /do-wiki 생성 위치
├── 2 Permanent/      ← /do-permanent 저장 위치
├── 3 Archive/        ← 처리 완료 raw 보관
├── _index/
│   ├── VAULT_INDEX.md
│   └── GRAPH.md
└── CLAUDE.md
```

**스타터킷** (권장): [Google Drive에서 zettel-connect-starter.zip 다운로드](https://drive.google.com/file/d/1KCm_BE93x8vh5gg_-fx0YjDkSsIzToFs/view?usp=drive_link) 후 Claude Code에 붙여넣기:

```
zettel-connect-starter.zip을 사용해서 옵시디언 제텔카스텐 볼트를 설치해줘.
zip 파일 경로와 새 볼트 경로를 물어봐서 진행해줘.
설치 후 SKILL.md 파일들의 VAULT_ROOT 경로를 내 볼트 경로로 치환해줘.
```

**수동 설치** 시 VAULT_ROOT 경로 치환 여부 확인:

```bash
grep -r "futurewave" ~/.claude/skills/ 2>/dev/null || echo "✅ clean"
```

---

## 지식관리 파이프라인

### /do-fleeting — 생각을 즉시 포착

**언제**: 지금 정리할 시간은 없지만 잃고 싶지 않을 때.

```
/do-fleeting 오늘 미팅에서 나온 아이디어: 팀 대시보드를 Mattermost로 옮기면 어떨까
```

→ `0 raw/YYYYMMDD 제목.md`에 즉시 저장. 분류나 분석 없이 1번의 도구 호출로 끝.

**쌓인 메모 정리**:

```
/do-fleeting scan
```

→ `0 raw/`의 미처리 목록을 보여주고, 선택한 항목을 `/do-permanent`으로 전환해준다.

---

### /do-literature — 읽은 자료를 문헌노트로

**언제**: 책·논문·아티클을 읽고 자기 말로 소화해 남기고 싶을 때. `/do-fleeting`(내 생각)와 달리 **출처가 있는 자료** 전용.

```
/do-literature 루만 「Communicating with Slip Boxes」 — 제텔카스텐의 핵심은 대화 상대로서의 메모다
```

→ `1 Literature/`에 저장. 영구노트 후보 개념을 표시해 `/do-permanent`으로 연결.

---

### /do-permanent — 영구노트 생성

**언제**: 생각이 충분히 익었고 제텔카스텐에 정식으로 기록하고 싶을 때.

```
/do-permanent LLM은 검색을 대체하는 게 아니라 검색 결과를 해석하는 레이어다
```

Claude가 자동으로:
1. `VAULT_INDEX.md`를 읽어 연결 후보 3개 이하 제안
2. Folgezettel ID 배정
3. 노트 생성 + `cascade.py`로 링크 자동 업데이트

---

### /do-wiki — 클러스터 허브 페이지

**언제**: 특정 주제의 노트가 쌓여 한눈에 보이는 인덱스 페이지가 필요할 때.

```
/do-wiki AI에이전트
```

→ `1 wiki/AI에이전트.md` 생성. 관련 영구노트 자동 연결.

---

### /do-index — VAULT_INDEX 갱신

**언제**: 노트를 여러 개 추가·수정한 뒤 인덱스를 최신 상태로 맞출 때. `/do-permanent`·`/do-query`·`/do-lint`가 이 인덱스를 읽으므로 **지식관리의 토대**.

```
/do-index
```

→ `2 Permanent/`·`1 Literature/`의 프론트매터를 `_index/VAULT_INDEX.md`로 압축. 노트 추가 후 실행.

---

### /do-query — 볼트 검색

**언제**: "이 주제로 예전에 뭔가 적었는데" 싶을 때.

```
/do-query LLM 검색
```

키워드·태그·클러스터·링크 관계 4가지 방식으로 동시 검색.

---

### /do-lint — 볼트 건강 점검

**언제**: 월 1회 볼트 상태를 정리할 때.

```
/do-lint
```

고아 노트·깨진 위키링크·미처리 raw·frontmatter 누락 탐지 후 수정 제안.

---

## 아이디어 파이프라인

### /do-sharpen — 아이디어를 명세서로

**언제**: 막연한 아이디어를 제품화 가능한 명세서로 만들고 싶을 때. 개발 착수 전 필수.

```
/do-sharpen 팀원들이 매일 업무를 정리해서 공유할 수 있는 툴이 있으면 좋겠어
```

Notion 페이지도 입력 가능:

```
/do-sharpen https://notion.so/xxx
```

소크라테스 질문 최대 10라운드 → 명확성 80점 이상 → 명세서 자동 생성.  
**판정 축**: Who(15) · Why(20) · What(20) · Scope(15) · Measure(15) · Risk(15)  
**결과물**: 한 줄 요약 / 대상 / 배경 / 결과물 / 범위 / 성공기준 / 리스크

---

### /do-productify — 명세서를 로드맵으로

**언제**: 명세서가 준비됐고 "어떤 형태의 제품으로 어떻게 만들지" 설계할 때. `/do-sharpen` 다음 단계.

```
/do-productify ./spec-daily-summary.md
```

**경량화 우선**: `claude-skill → 스크립트 → local HTML → ... → 풀스택 웹서비스`

**보안 판정**:
- 🔴 STOP: 프로덕션 DB 직접 접근, 개인정보 유출 경로
- 🟡 REVIEW: 테스트 환경 불명확, 민감성 불확실
- 🟢 SAFE: 공개 API, 익명화 데이터

**결과물**: 제품 형태 근거 + 의존성 + Phase별 목표/기준/보안 체크 로드맵 문서

---

## 리포트·발표

### /do-report — A4 PDF 기관 리포트

**언제**: 정리된 내용을 기관급 리서치 리포트로 내보낼 때.

```
/do-report ETHConf 2026 참관 리포트 만들어줘
```

기관 리포트 스타일 (표지·목차·Executive Summary·"View" 인사이트 박스·디스클레이머). Pretendard+Source Serif 4 폰트 임베드, Chrome headless PDF 렌더.

---

### /do-genpt — HTML 슬라이드 덱

**언제**: 전략·기획을 발표용 슬라이드로 만들 때.

```
/do-genpt 둘레값 사업 피치덱 만들어줘
```

에디토리얼 풀뷰포트 HTML. 스크롤·방향키 탐색. `<주제>_PT.html`로 저장 후 브라우저에서 발표.

### /do-genpt-hotplx — 네이비 러스트 IR 덱

**언제**: 투자자·심사역에게 보내는 IR·기업설명·사업계획.

```
/do-genpt-hotplx AInexus 시리즈A IR 덱 만들어줘
```

네이비(`#1B2A4A`) 다크 ↔ 화이트 라이트 교차에 러스트(`#9C4A34`) 액센트. 960×540 고정 캔버스,
모바일에서는 리플로우 + autofit으로 슬라이드 1장이 화면 1페이지에 들어온다.
수익모델·재무추정·팀 슬라이드 타입 포함.

---

## 검증·자동화

### /do-critique — 적대적 검증

**언제**: 명세·기획을 외부에 내보내기 전 스스로 약점을 찾고 싶을 때.

```
/do-critique ./spec.md
```

미검증 가정·경쟁 누락·논리 구멍을 탐지. 🔴 치명 / 🟡 주의 / 🟢 통과 판정.

---

### /do-ingest — 외부 자료 일괄 인제스트

**언제**: PDF·URL·이미지·텍스트를 문헌노트로 빠르게 변환하고 싶을 때.

```
/do-ingest ./report.pdf
/do-ingest https://example.com/article
```

소스 판별 → 텍스트 추출 → 요약 + 개념 추출 → `1 Literature/` 저장.

---

### /do-relink — 링크 정합 복구

**언제**: 노트를 여러 개 추가·수정한 뒤 frontmatter `links[]`와 VAULT_INDEX가 어긋났을 때.

```
/do-relink
```

양방향 링크 정합 검사 → 드리프트 탐지 → 확인 후 일괄 수정 → `/do-index` 자동 호출.

---

### /do-refactor — 노트 구조 변경

**언제**: 노트를 이동·병합·분할할 때 링크가 깨지지 않게 하고 싶을 때.

```
/do-refactor move 0024 "2 Permanent/AI에이전트/"
/do-refactor merge 0024 0025
/do-refactor split 0024
```

이동·이름변경·병합·분할 4가지 서브커맨드. `links[]`와 VAULT_INDEX를 함께 갱신.

---

### /do-breakdown — 큰 노트 분해

**언제**: 하나의 노트가 너무 많은 아이디어를 담고 있어 원자적 노트로 쪼개고 싶을 때.

```
/do-breakdown 0024
```

분해 후보 개념 제안 → 확인 → 하위 영구노트 생성 + 원본 노트 갱신.

---

### /do-compile — 노트 → 발표·리포트 자동 생성

**언제**: 이미 쌓인 볼트 노트들을 모아 슬라이드나 리포트로 만들고 싶을 때.

```
/do-compile pt AI에이전트          # 클러스터 → 슬라이드 덱
/do-compile report AI에이전트      # 클러스터 → PDF 리포트
```

클러스터·태그 기준으로 노트 수집 → 스토리라인 구성 → `/do-genpt` 또는 `/do-report` 실행.

---

### /do-research — 웹 근거 수집

**언제**: 주장·명세에 외부 데이터·시장 조사가 필요할 때. `/do-critique`의 🔴 항목 보강에 특히 유용.

```
/do-research "국내 협업 툴 시장 규모 2025"
/do-research --critique ./spec.md
```

---

### /do-decide — 결정 기록 (ADR)

**언제**: 제품·아키텍처 결정을 나중에 추적 가능하게 남기고 싶을 때.

```
/do-decide Redis 캐시 레이어 도입
```

맥락·검토 대안·근거를 ADR 형식으로 `2 Permanent/`에 저장. `status: superseded`로 번복 추적.

---

## 실전 시나리오

### 1. 지식 축적 (기본 흐름)

```
/do-fleeting 팀 대시보드를 Mattermost로 옮기면 알림 피로가 줄 것 같다

# 며칠 후
/do-fleeting scan           # 미처리 목록 확인
/do-permanent               # 영구노트로 전환

# 노트가 쌓이면
/do-index              # VAULT_INDEX 갱신
/do-wiki 협업도구       # 허브 페이지 생성
```

### 2. 지식을 제품으로

```
/do-sharpen 팀 일일 업무요약 봇을 만들고 싶어
/do-productify ./spec.md
```

### 3. 발표·리포트

```
/do-genpt 프로젝트 피치덱 만들어줘
/do-report 월간 리서치 리포트 만들어줘
```

### 4. 볼트 정기 점검 (월 1회)

```
/do-lint               # 문제 탐지
/do-fleeting scan           # 미처리 메모 정리
/do-index              # VAULT_INDEX 갱신
/do-wiki 클러스터명     # 허브 페이지 갱신
```

### 5. 명세 검증 + 시장 조사

```
/do-sharpen 팀 일일 업무요약 봇
/do-critique ./spec.md           # 약점 탐지
/do-research --critique ./spec.md  # 🔴 항목 근거 보강
/do-decide "Slack API 사용 vs 자체 웹훅"  # 결정 기록
/do-productify ./spec.md
```

### 6. 외부 자료 → 볼트 통합

```
/do-ingest ./paper.pdf           # 문헌노트 생성
/do-relink                       # 링크 정합 복구
/do-compile pt 클러스터명         # 노트 → 발표 자료
```

---

## 요구사항

- [Claude Code](https://claude.ai/code) (CLI 또는 데스크탑 앱)
- Claude Pro 이상
- Python 3.9+ (`cascade.py`, `search.py` 실행용)
- Obsidian (볼트 뷰어, 지식관리 스킬 전용)
