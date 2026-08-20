---
name: do-breakdown
description: 큰 노트나 허브 노트를 원자적 하위 영구노트들로 분해. 1 노트 = 1 아이디어 원칙 복구. "breakdown", "쪼개줘", "분해해줘", "하위 노트 만들어줘" 등을 언급하면 사용한다.
---

# /do-breakdown — 노트 분해

## 트리거
`/do-breakdown <노트ID 또는 경로>` 또는 `/breakdown`

## 파이프라인

**Step 1: 대상 노트 분석**
- 노트 Read + VAULT_INDEX에서 연결 컨텍스트 로드
- 원자적 아이디어 단위 추출 (각각이 독립 영구노트가 될 수 있는 단위)

**Step 2: 분해 계획 확인**
- 분해될 노트 목록 + 각 노트의 예상 claim 제안
- AskUserQuestion으로 사용자 확인·조정

**Step 3: 하위 영구노트 생성**
- 각 아이디어를 `/do-permanent` 파이프라인으로 처리
- Folgezettel ID 자동 배정 (부모 ID 기반 하위 ID)

**Step 4: 허브 노트 전환**
- 원본 노트의 본문을 하위 노트 links[] 목록으로 대체
- 원본은 허브 노트로 유지 (삭제 안 함)

**Step 5: 인덱스 갱신**
- `/do-index` 호출 → VAULT_INDEX 갱신

## 핵심 원칙
- 1 노트 = 1 아이디어 원칙 준수
- 원본 허브 노트는 절대 삭제하지 않음
- 분해 단위는 사용자가 최종 결정
