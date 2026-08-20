---
name: do-fleeting
description: 임시노트를 0 raw/에 포착하고, scan 모드로 미처리 자료를 영구노트로 전환한다.
---

# Raw — 임시노트 + Raw 스캔

> "생각은 떠오르는 순간 잡지 않으면 사라진다." — 니클라스 루만

## 트리거

`/do-fleeting` 또는 `/임시노트`

## 2가지 모드

| 모드 | 사용법 | 효과 |
|------|--------|------|
| **기본** | `/do-fleeting 메모` | `0 raw/` 에 즉시 저장 |
| **scan** | `/do-fleeting scan` | `0 raw/` 미처리 자료 → 영구노트 전환 |

## 폴더 구조

```
0 raw/              ← 불변 소스 (이 스킬의 저장 위치)
  ├── articles/     ← 웹 기사, 클리핑
  ├── papers/       ← 논문
  ├── books/        ← 독서 노트
  ├── videos/       ← 영상 요약
  ├── podcasts/     ← 팟캐스트
  └── assets/       ← 이미지, 첨부
```

---

## ═══ 기본 모드 ═══

### Step 1: 내용 확인

- 내용 있으면 → Step 2
- 없으면 → AskUserQuestion

### Step 2: 즉시 저장

`0 raw/` 에 저장. 도구 1회. 분류/탐색/분석 안 함.

**파일명**: `YYYYMMDD 제목.md`

```markdown
---
type: fleeting
created: "YYYY-MM-DD"
processed: false
tags:
  - 태그1
---

[사용자 메모 원문 그대로]
```

### Step 3: 1줄 보고

```
0 raw/20260416 아이디어.md 에 저장했습니다.
```

---

## ═══ scan 모드 ═══

> `0 raw/` 미처리 자료를 찾아서 영구노트로 전환

### Scan Step 1: 미처리 자료 찾기

`0 raw/` 하위 전체에서 frontmatter `processed: false` 또는 `processed` 필드 없는 `.md` 파일 목록 추출.

**방법**: python 스크립트 또는 Grep으로 frontmatter 스캔 (본문 Read 안 함).

### Scan Step 2: 분류 + 확인

미처리 파일 목록을 사용자에게 보여주고 어떤 것을 영구노트로 만들지 AskUserQuestion으로 확인.

### Scan Step 3: 영구노트 생성

선택된 자료에 대해:
1. 해당 raw 파일을 **이때만 Read** (필요한 파일만, 전체 아님)
2. `/do-permanent` 스킬의 파이프라인 실행 (VAULT_INDEX 매칭 → 노트 생성 → cascade.py)

### Scan Step 4: 처리 완료 표시

생성 완료된 raw 파일의 frontmatter에 `processed: true` 추가.
raw 파일 자체는 삭제하지 않음 (불변 원칙).

### Scan Step 5: 보고

```
📊 scan 완료
미처리: 5개 발견
처리: 3개 → 영구노트 생성
스킵: 2개
```

---

## 핵심 원칙

1. **즉시 저장**: 기본 모드는 도구 1회. 탐색 안 함.
2. **원문 보존**: raw 파일은 수정/삭제 안 함. `processed` 플래그만 추가.
3. **최소 서식**: frontmatter + 본문. 구조화 안 함.
4. **필요한 것만 Read**: scan 시 사용자가 선택한 파일만 Read. 전체 스캔 안 함.

## 볼트 경로

```
VAULT_ROOT="/Users/futurewave/Library/CloudStorage/GoogleDrive-futurewave@gmail.com/내 드라이브/03 Resources/옵시디언 볼트/futurewave"
```

저장 위치: `${VAULT_ROOT}/0 raw/`
