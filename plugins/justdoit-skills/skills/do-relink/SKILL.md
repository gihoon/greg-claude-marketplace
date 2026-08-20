---
name: do-relink
description: 볼트의 frontmatter links[]를 유일한 진실로 삼아 양방향 링크와 VAULT_INDEX를 재정합. 노트 추가·이동·수정 후 링크가 깨졌거나 단방향인 경우 사용. "relink", "링크 고쳐줘", "인덱스 망가졌어", "양방향 링크" 등을 언급하면 사용한다.
---

# /do-relink — 링크·인덱스 재정합

## 트리거
`/do-relink` 또는 `/relink`

## 파이프라인

**Step 1: 전체 frontmatter 스캔**
- `2 Permanent/`·`1 Literature/` 모든 노트의 `links[]` 수집
- `_index/VAULT_INDEX.md` 로드

**Step 2: 양방향 정합 검사**
- A→B 링크 존재 시 B의 `links[]`에 A 없으면 → 추가 후보 목록
- 끊긴 링크(노트 없음) → 삭제 후보 목록

**Step 3: VAULT_INDEX 드리프트 탐지**
- 노트 존재 but 인덱스 누락 → 추가 필요
- 인덱스 존재 but 노트 삭제 → 제거 필요

**Step 4: 변경 사항 확인 + 적용**
- AskUserQuestion으로 추가·삭제 목록 확인
- 확인된 항목만 frontmatter 수정
- `/do-index` 호출 → VAULT_INDEX 재생성

## 핵심 원칙
- frontmatter `links[]`가 유일한 진실 (본문 위키링크는 참고용)
- 자동 삭제 금지 — 반드시 사용자 확인
- cascade.py 없이 frontmatter에서 직접 derive
