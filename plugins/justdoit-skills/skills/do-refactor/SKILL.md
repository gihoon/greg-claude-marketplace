---
name: do-refactor
description: 노트 이동·ID 재배치·병합·분할 시 links[]와 VAULT_INDEX 정합을 유지. 볼트 구조 재정비 작업의 안전망. "refactor", "노트 옮겨줘", "ID 바꿔줘", "노트 합쳐줘", "쪼개줘" 등을 언급하면 사용한다.
---

# /do-refactor — 노트 구조 리팩터

## 트리거
`/do-refactor` 또는 `/refactor`

## 서브커맨드
| 커맨드 | 효과 |
|--------|------|
| `/do-refactor move <ID> <새폴더>` | 노트 이동 + links[] 경로 갱신 |
| `/do-refactor rename <ID> <새ID>` | ID 재배치 + 부모·자식 links[] 갱신 |
| `/do-refactor merge <ID1> <ID2>` | 두 노트 병합 → 새 노트, 양쪽 링크 리디렉트 |
| `/do-refactor split <ID>` | 노트 분할 → 원자적 노트 2개, 부모 links[] 갱신 |

## 파이프라인

**Step 1: 영향 범위 산출**
- 대상 노트를 links[]로 참조하는 모든 노트 목록

**Step 2: 변경 미리보기**
- 파일명·ID·links[] 변경 전/후 대조 출력
- AskUserQuestion으로 확인

**Step 3: 실행**
- 파일 조작 실행
- 원본은 `3 Archive/`에 백업 후 삭제

**Step 4: 정합 검증**
- `/do-relink` 호출 → 링크 일관성 확인
- `/do-index` 호출 → VAULT_INDEX 갱신

## 핵심 원칙
- 실행 전 반드시 미리보기 확인
- 원본 노트는 Archive 백업 후 삭제
