---
name: do-permanent
description: 제텔카스텐 영구노트 생성. VAULT_INDEX claim+tags로 3개 이하 연결 후보 선별 → 노트 생성 → cascade.py 일괄 후처리. 최상위 ID는 전용 폴더(2 Permanent/0025 제목/)를 생성하고 하위 노트는 부모 폴더에 저장한다.
---

# Permanent Note — 영구노트 스킬

> "하나의 노트에는 하나의 아이디어만." — 니클라스 루만

## 개요

영구노트는 제텔카스텐의 **최종 결과물**. `/do-permanent 아이디어`로 실행.

**연결 원칙:** `_index/VAULT_INDEX.md`의 claim+tags만으로 연결 후보 3개 이하를 선별. 개별 노트 본문을 읽지 않는다.

## 트리거

`/do-permanent` 또는 `/영구노트`

---

## 사용자 질문 프로토콜 (필수)

사용자에게 **어떤 질문이든 묻거나, 확인을 요청하거나, 선택지를 제시할 때** 반드시 **`AskUserQuestion` 툴**을 사용한다. 일반 텍스트로 질문하고 답을 기다리는 방식은 금지.

---

## 볼트 경로 (자동 감지)

**VAULT_ROOT 결정 순서:**

**Step A.** config 파일 확인:
```bash
cat ~/.claude/skills/justdoit-skills/vault.conf 2>/dev/null
```
출력이 있으면 그 경로를 VAULT_ROOT로 사용. 아래 Step B/C 생략.

**Step B.** 현재 작업 디렉토리에서 `.obsidian` 폴더 탐색:
```bash
find . -name ".obsidian" -maxdepth 4 -type d 2>/dev/null | head -1
```
찾으면 그 부모 디렉토리를 VAULT_ROOT로 사용. Step C 생략.

**Step C.** 감지 실패 시 `AskUserQuestion`으로 경로 입력 받기 → 입력값을 config에 저장:
```bash
mkdir -p ~/.claude/skills/justdoit-skills
echo "<사용자 입력 경로>" > ~/.claude/skills/justdoit-skills/vault.conf
```

---

## 폴더 구조

```
VAULT_ROOT/
├── 0 raw/          ← 불변 소스
├── 1 wiki/         ← LLM 자동 생성 (개념·요약·인덱스)
├── 2 Permanent/    ← 영구노트 저장 위치
│   ├── 0023 스킬 통합 전략/
│   │   ├── 0023. 두 스킬 패키지 통합 분석.md   ← 최상위 노트
│   │   └── 0023a. good-skills 개선·확장 분석.md  ← 하위 노트
│   ├── 0024 HiVibeLabs/
│   │   ├── 0024. Main Subject.md
│   │   ├── 0024a. Project.m
│   │   └── ...
│   └── ...
└── _index/
    ├── VAULT_INDEX.md
    └── GRAPH.md
```

**ID 타입 규칙:**

| ID 패턴 | 예시 | 타입 | 저장 위치 |
|---------|------|------|-----------|
| 숫자 4자리 | `0025` | 최상위 노트 | `2 Permanent/0025 [제목]/0025. [제목].md` (폴더 신규 생성) |
| 숫자+소문자 | `0025a` | 1단계 하위 | `2 Permanent/0025 [제목]/0025a. [제목].md` |
| 숫자+소문자+숫자 | `0025a1` | 2단계 하위 | `2 Permanent/0025 [제목]/0025a1. [제목].md` |
| 부모 폴더 없음 | — | fallback | `2 Permanent/[ID]. [제목].md` |

---

## 파이프라인 (5 Step)

```
/do-permanent "아이디어"
  │
  Step 0: VAULT_ROOT 감지
  │
  Step 1: 아이디어 수집 (없으면 AskUserQuestion)
  │
  Step 2: 원자성 검증
  │
  Step 3: VAULT_INDEX Read 1회 → claim+tags 매칭 → 후보 3개 이하 → ID 배정
  │
  Step 4: 폴더 생성 (최상위 ID일 때) + 노트 생성 (Write 1회)
  │
  Step 5: cascade.py (Bash 1회)
```

---

## Step 0: VAULT_ROOT 감지

위 "볼트 경로" 섹션의 Step A → B → C 순서로 실행. VAULT_ROOT 확정 후 진행.

## Step 1: 아이디어 수집

- 아이디어가 함께 제공되면 → Step 2로
- 없으면 → AskUserQuestion으로 질문

## Step 2: 원자성 검증

1. 하나의 아이디어인가? 여러 개 섞이면 분리 제안
2. 명확한 주장/명제 형태인가? 모호하면 정제 제안

## Step 3: VAULT_INDEX 경량 검색 & 연결 & ID 배정

**절대 개별 노트 파일을 Read하지 않는다.**

**3-1.** `_index/VAULT_INDEX.md` Read 1회.

**3-2. 연결 후보 선별 (3개 이하):**
- claim의 주장 방향·전제·귀결이 겹치는 노트
- 같은 태그를 공유하는 노트
- 각 후보에 연결 유형 1줄: 지지 / 반박 / 확장 / 구체화 / 유비

**3-3. Folgezettel ID 배정:**
- 가장 관련 깊은 노트를 부모로 결정
- 발전/심화 → 하위 ID (예: `0025` → `0025a`)
- 병렬/대안 → 형제 ID (예: `0025a` 옆에 `0025b`)
- 새 주제 → 새 최상위 ID (현재 최대 숫자 + 1)
- 사용자에게 후보 + ID 제안 → AskUserQuestion으로 확인

## Step 4: 폴더 생성 + 노트 생성

**4-1. 저장 경로 결정:**

```bash
# 최상위 ID (예: 0025) → 폴더 신규 생성
mkdir -p "${VAULT_ROOT}/2 Permanent/0025 [제목]"
# 저장 경로: 2 Permanent/0025 [제목]/0025. [제목].md

# 하위 ID (예: 0025a) → 부모 폴더 탐색
ls "${VAULT_ROOT}/2 Permanent/" | grep "^0025 "
# 찾은 폴더 안에 저장: 2 Permanent/0025 [제목]/0025a. [제목].md
# 부모 폴더 없으면: 2 Permanent/0025a. [제목].md
```

**4-2. 노트 파일 생성 (Write 1회):**

**문체:** 번역투 배제, 훅으로 시작, 문장 밀도 높게, 짧은/긴 문장 교차.

```markdown
---
type: permanent
id: "[ID]"
created: "YYYY-MM-DD HH:mm"
status: 🌱
parent: "[부모 ID]"
claim: "[핵심 주장 한 줄]"
links: ["부모ID", "연결1", "연결2"]
cluster: "[클러스터명]"
tags:
  - 태그1
  - 태그2
---

## 🗂 Zettelkasten Code

**`[현재 ID]`** — *[앞 ID]([앞 노트 제목])* 와 *[뒤 ID]([뒤 노트 제목])* 사이에 삽입

> 🔗 **연결 전략:** [전략명] — [시드 노트]를 '[클러스터]' 클러스터의 맥락 속으로 끌어들인다.

---

## 💡 핵심 아이디어

**"[훅 문장]"**

[2-3문단. 기존 노트를 [[위키링크]]로 인용.]

> **"[핵심 주장 인용구]"**

---

## 🔗 노트 연결 분석

### 연결 1: 타겟 심층 분석
[핵심 솔루션과 메커니즘. bullet 3-4개.]

### 연결 2: Serendipity
> ✨ **놀라운 접점:** [두 노트의 예상 밖 만남]
[인과 사슬 또는 구조적 유사성.]

### 연결 3: Synthesis
> 🛡️ **"[새 개념/프레임]"** — [한 줄 정의]
[구체적 실천 bullet 3-4개.]

---

## 🎯 실행 체크리스트
- [ ] **[액션]** — [구체 산출물]
- [ ] **[액션]** — [...]
- [ ] **[액션]** — [...]

---

## 📊 기대 효과
[before/after 2-3문단.]
> **[잠언]**

---

## 📎 참조 노트
**Seed Note:**
- [노트 제목](URL) ← *출처*

**관련 노트:**
- [노트 제목] ← *코드*
```

## Step 5: cascade.py 일괄 실행

`new_note_relpath`는 VAULT_ROOT 기준 상대 경로. 폴더가 있으면 폴더 포함.

```bash
python3 "${VAULT_ROOT}/.claude/skills/do-permanent/cascade.py" \
  "${VAULT_ROOT}" \
  "2 Permanent/0025 제목/0025. 제목.md" \
  "0025" "0024" "0023" "0022"
```

cascade.py가 처리하는 것:
1. 부모 노트 links[] 추가 (재귀 탐색으로 하위 폴더도 검색)
2. 연결 노트 역방향 links[] 추가
3. VAULT_INDEX.md 1줄 append
4. GRAPH.md 1줄 append
5. 해당 클러스터 wiki 페이지에 1줄 추가

결과: JSON 출력 → 1-3줄 요약 보고.

---

## 초안 입력 모드

raw에서 이미 완성된 초안이 들어오면 (frontmatter + `## 💡` 섹션 포함):
1. Step 0~2 스킵
2. Step 3에서 초안의 ID를 우선 사용 (충돌 시 조정)
3. Step 4~5 정상 수행

---

## 심층 분석

`/do-permanent`는 claim 기반 경량 연결만 수행.
깊은 분석이 필요하면 사용자가 직접 관련 노트를 지정하여 대화로 진행.

## 핵심 원칙

1. **원자성**: 1 노트 = 1 아이디어
2. **VAULT_INDEX만 읽기**: 개별 노트 본문 Read 금지
3. **후보 3개 이하**: 연결 후보를 3개 넘게 제안하지 않는다
4. **폴더 계층**: 최상위 ID는 전용 폴더, 하위 노트는 부모 폴더 안
5. **cascade.py로 후처리**: 다른 스킬 호출 금지, cascade.py Bash 1회로 끝
6. **Folgezettel 충실**: 코드 계층으로 계보 추적 가능
