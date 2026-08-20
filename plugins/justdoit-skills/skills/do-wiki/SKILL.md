---
name: do-wiki
description: 카파시 LLM Wiki 패턴. VAULT_INDEX 기반으로 1 wiki/에 개념 페이지·인덱스·비교 페이지를 자동 생성. 영구노트의 허브 역할.
---

# Wiki — LLM 위키 스킬

> "Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase." — Karpathy

## 개요

카파시의 LLM Wiki 패턴을 옵시디언 제텔카스텐에 접목. `2 Permanent/`의 영구노트들을 종합하여 `1 wiki/`에 개념 페이지를 자동 생성한다. 개별 영구노트를 직접 연결하는 대신, **wiki 페이지가 허브 역할**을 하여 N:N 연결을 자연스럽게 만든다.

## 트리거

`/do-wiki` 또는 `/위키`

## 3가지 모드

| 모드 | 사용법 | 효과 |
|------|--------|------|
| **build** | `/do-wiki build` | 전체 클러스터별 개념 페이지 일괄 생성 |
| **page** | `/do-wiki page 글쓰기` | 특정 주제의 개념 페이지 1개 생성/갱신 |
| **index** | `/do-wiki index` | 전체 위키 목차(index.md) 생성 |

## 폴더 구조

```
1 wiki/
├── index.md           ← 전체 위키 목차
├── 글쓰기.md           ← 개념 페이지 (31개 노트 종합)
├── AI.md              ← 개념 페이지 (60개 노트 종합)
├── 철학.md             ← 개념 페이지
├── ...
└── log.md             ← 생성/갱신 이력 (append-only)
```

## 볼트 경로

```
VAULT_ROOT="/Users/futurewave/Library/CloudStorage/GoogleDrive-futurewave@gmail.com/내 드라이브/03 Resources/옵시디언 볼트/futurewave"
```

---

## ═══ build 모드 ═══

VAULT_INDEX의 클러스터 목록을 읽어서 **노트 5개 이상인 클러스터**에 대해 개념 페이지를 일괄 생성.

### 실행 흐름

1. `_index/VAULT_INDEX.md` Read 1회
2. 노트 5개 이상인 클러스터 추출
3. 각 클러스터에 대해 개념 페이지 생성 (claim 목록만으로, 본문 Read 안 함)
4. `1 wiki/do-index.md` 생성
5. `1 wiki/log.md` 에 이력 append

### 개념 페이지 서식

```markdown
---
type: wiki
topic: "[클러스터명]"
note_count: [N]
generated: "YYYY-MM-DD HH:mm"
---

# [클러스터명]

> [이 주제가 다루는 핵심 질문을 1문장으로]

## 핵심 주장들

이 클러스터의 [N]개 영구노트가 말하는 것:

| 코드 | 주장 |
|------|------|
| [[0030]] | 마음이 편해야 글을 쓴다 |
| [[0030a]] | 부교감 신경과 글쓰기의 관계 |
| ... | ... |

## 주요 흐름

[claim 목록을 분석하여 아이디어의 흐름을 3-5문단으로 서술. 
 각 문단에서 관련 노트를 [[코드]] 위키링크로 인용.
 노트 본문을 읽지 않고 claim만으로 작성.]

## 빈 구멍 (Gap Analysis)

[이 클러스터에서 아직 다뤄지지 않은 질문이나 누락된 관점을 2-3개 제안.
 새 영구노트 후보가 된다.]

## 교차 클러스터 연결

[다른 클러스터와 겹치는 노트가 있으면 표시.
 예: "AI 클러스터의 [[0500]]과 이 클러스터의 [[0530]]은 같은 주제를 다른 각도에서 본다."]

---

> [!info] 자동 생성
> 이 페이지는 `/do-wiki build`로 생성됨. 수동 편집 시 다음 build에서 덮어씌워짐.
```

### 토큰 절약 원칙

- VAULT_INDEX.md 1회 Read만으로 모든 개념 페이지 생성
- 개별 영구노트 본문을 읽지 않는다
- claim 한 줄 + tags로 흐름을 추론

---

## ═══ page 모드 ═══

`/do-wiki page 글쓰기` — 특정 주제의 개념 페이지 1개만 생성/갱신.

1. VAULT_INDEX에서 해당 클러스터(또는 태그 매칭) 노트 추출
2. 개념 페이지 서식대로 생성
3. `1 wiki/log.md`에 이력 append

build와 동일한 서식, 단일 클러스터만 처리.

---

## ═══ index 모드 ═══

`/do-wiki index` — 전체 위키 목차 생성.

```markdown
---
type: wiki-index
generated: "YYYY-MM-DD HH:mm"
---

# Wiki Index

> 383개 영구노트, 79개 클러스터, [N]개 개념 페이지

## 개념 페이지 목록

| 주제 | 노트 수 | 핵심 질문 |
|------|---------|----------|
| [[글쓰기]] | 31 | 어떻게 쓰는 행위 자체가 사고를 촉발하는가? |
| [[AI]] | 60 | AI와 인간의 협업에서 판단의 역할은? |
| ... | ... | ... |

## 미생성 클러스터 (5개 미만)

[노트 수가 적어 개념 페이지를 만들지 않은 클러스터 목록]
```

---

## 핵심 원칙

1. **wiki는 파생물**: 영구노트가 원본, wiki는 그것의 종합. wiki가 삭제되어도 영구노트에서 재생성 가능.
2. **본문 Read 금지**: VAULT_INDEX의 claim+tags만으로 작성. 토큰 절약.
3. **허브 역할**: 영구노트끼리 1:1 연결 대신, wiki 페이지를 통한 N:N 연결.
4. **Gap Analysis**: 빈 구멍을 찾아서 새 영구노트 후보를 제안하는 것이 wiki의 진짜 가치.
5. **덮어쓰기 허용**: `/do-wiki build` 시 기존 페이지를 갱신. 수동 편집 내용은 보존 안 됨.
