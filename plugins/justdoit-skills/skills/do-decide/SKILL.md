---
name: do-decide
description: 제품·아키텍처·전략 결정을 ADR(Architecture Decision Record) 형식으로 볼트에 기록. 결정의 맥락·대안·근거를 남겨 나중에 추적 가능하게. "decide", "결정 기록", "ADR", "왜 이걸 선택했는지 남겨줘" 등을 언급하면 사용한다.
---

# /do-decide — 결정 기록 (ADR)

## 트리거
`/do-decide <결정 제목>` 또는 `/decide`

## ADR 노트 형식

```markdown
---
type: decision
id: "ADR-YYYYMMDD-NNN"
status: accepted
date: "YYYY-MM-DD"
links: ["관련 노트 ID"]
cluster: "프로젝트명"
tags:
  - decision
  - adr
---

## 결정
[한 줄 결정문]

## 맥락
[왜 이 결정이 필요했는가]

## 검토한 대안
| 대안 | 장점 | 단점 |
|------|------|------|

## 근거
[왜 이 옵션을 선택했는가]

## 결과
[이 결정이 가져올 영향·트레이드오프]
```

## 파이프라인

**Step 1: 결정 맥락 수집**
- AskUserQuestion: 무엇을 / 왜 / 어떤 대안을 검토했는지

**Step 2: ADR 초안 생성**
- 수집된 답변으로 ADR 형식 작성

**Step 3: 저장 + 인덱스 갱신**
- `2 Permanent/` 저장 (파일명: `ADR-YYYYMMDD 결정제목.md`)
- `/do-index` 갱신

## 핵심 원칙
- 결정은 번복 가능 — `status: superseded`로 추적
- 대안을 반드시 1개 이상 기록 (왜 선택하지 않았는지)
- 결정 없이 진행한 것도 나중에 기록 가능
