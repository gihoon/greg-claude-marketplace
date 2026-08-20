---
name: do-lint
description: 볼트 상태 점검. 고아 노트, 끊긴 링크, 약한 연결, 프론트매터 누락을 탐지하고 수정 제안.
---

# Lint — 볼트 상태 점검

> "위키를 점진적으로 정리하고 전반적인 데이터 무결성을 강화한다." — Karpathy

## 트리거

`/do-lint` 또는 `/점검`

## 점검 대상

```
0 raw/          ← 미처리 자료 확인 (processed 플래그)
1 wiki/         ← 개념 페이지 정합성
2 Permanent/    ← 구조/메타데이터/연결 점검
_index/         ← 인덱스 동기화 상태
```

## 점검 항목

### 1. 구조 (Structure)

- **고아 노트**: `2 Permanent/`에서 어디에서도 참조되지 않는 노트
- **끊긴 링크**: `links[]`에 존재하지 않는 ID 포함
- **Folgezettel 정합성**: `parent` 필드가 실제 존재하는 노트를 가리키는지

### 2. 프론트매터 (Metadata)

- **필수 필드 누락**: `2 Permanent/`에 `claim`, `links`, `cluster` 필드 있는지
- **links-본문 불일치**: links[]에 있지만 본문에 없거나 그 반대

### 3. 연결 (Connections)

- **약한 연결**: 연결이 1개뿐인 영구노트
- **클러스터 고립**: 같은 클러스터 내에서만 연결, 교차 연결 없음
- **미처리 raw**: `0 raw/`에 `processed: false`인 자료

### 4. 발견 (Discovery)

- **숨겨진 연결**: claim+tags가 유사하지만 아직 연결 안 된 노트 쌍 제안
- **wiki 갭**: wiki 개념 페이지의 "빈 구멍" 섹션 기반

## 실행

### Step 1: VAULT_INDEX + GRAPH 읽기

`_index/VAULT_INDEX.md`와 `_index/GRAPH.md`만 읽어서 대부분의 점검 수행. 개별 노트 본문 Read 최소화.

### Step 2: 점검 실행 + 리포트

```
## 볼트 상태 점검

📊 통계: 영구노트 383개, wiki 21개, raw 미처리 N개

### 🔴 즉시 수정
- 끊긴 링크: [[없는ID]] in 0030a.md
- 프론트매터 누락: 0540.md에 cluster 없음

### 🟡 개선 권장
- 고아 노트: 0070.md — 아무 데서도 참조 안 됨
- 약한 연결: 0210.md — 연결 0개
- 미처리 raw: 3개

### 🟢 연결 기회
- [[0630]]과 [[0030a1]]: "루틴"과 "인지적 방파제" — 연결 제안
```

### Step 3: 수정 (사용자 확인 후)

**자동 수정 안 함.** 리포트 보여주고 사용자가 선택.

## 핵심 원칙

1. **비파괴적**: 리포트만, 자동 수정 없음
2. **VAULT_INDEX 우선**: 개별 노트 Read 최소화
3. **발견 지향**: 오류 수정 + 새 연결 기회 발굴

## 볼트 경로

```
VAULT_ROOT="/Users/futurewave/Library/CloudStorage/GoogleDrive-futurewave@gmail.com/내 드라이브/03 Resources/옵시디언 볼트/futurewave"
```

점검 대상: `${VAULT_ROOT}/0 raw/`, `${VAULT_ROOT}/1 wiki/`, `${VAULT_ROOT}/2 Permanent/`, `${VAULT_ROOT}/_index/`
