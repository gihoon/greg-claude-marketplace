---
name: do-compile
description: 볼트의 노트들을 선택해 /do-genpt(슬라이드) 또는 /do-report(PDF)로 컴파일. "노트 기반 발표·리포트 자동 생성"의 핵심. "compile", "노트로 발표 만들어줘", "노트 모아서 리포트 써줘", "클러스터로 PT" 등을 언급하면 사용한다.
---

# /do-compile — 노트 → 결과물 컴파일

## 트리거
`/do-compile` 또는 `/compile`

## 사용법
```
/do-compile pt 클러스터명           # 클러스터 노트들 → 슬라이드 덱
/do-compile report 클러스터명       # 클러스터 노트들 → PDF 리포트
/do-compile pt --tag 태그명         # 태그 필터 노트들 → 슬라이드
/do-compile pt ID1 ID2 ID3          # 명시적 노트 목록 → 슬라이드
```

## 파이프라인

**Step 1: 소스 노트 수집**
- 클러스터 / 태그 / 명시적 ID 목록 기준으로 VAULT_INDEX 검색
- 관련 노트 claim·tags·links 로드

**Step 2: 스토리라인 구성**
- 노트 claim들을 논리 흐름으로 정렬
- 슬라이드/챕터 구조 초안 → AskUserQuestion으로 확인

**Step 3: 결과물 생성**
- `pt` → `/do-genpt` 스킬 실행 (노트 claim을 슬라이드 bullet으로 매핑)
- `report` → `/do-report` 스킬 실행 (노트 claim을 챕터로 매핑)

**Step 4: 소스 기록**
- 결과물 파일에 소스 노트 ID 목록 명시 (재현 가능하도록)

## 핵심 원칙
- 소스 노트는 항상 명시 — 어떤 노트에서 왔는지 추적 가능해야 함
- 노트 원문 인용 시 ID + claim 출처 표기
