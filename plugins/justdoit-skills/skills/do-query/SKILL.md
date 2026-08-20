---
name: do-query
description: 제텔카스텐 4-Way Search. 키워드 + 링크 탐색 + 유사 노트 + 관계 검색의 조합. Python이 검색하고 Claude는 해석만.
---

# Query — 4-Way Search

> "검색해서 답을 얻는 시스템"이 아니라 "검색해서 다음 생각으로 넘어가게 하는 시스템"

## 트리거

`/do-query` 또는 `/검색`

## 사용법

`/do-query 글쓰기 루틴`

## 아키텍처

```
/do-query "검색어"
  │
  Bash: python3 search.py "${VAULT_ROOT}" "검색어"    ← 토큰 0
  │
  JSON 결과 (20개 후보 + claim)                        ← ~2K 토큰
  │
  Claude: "이 노트들이 이끄는 다음 생각은?"            ← ~3K 토큰
```

총 ~5K 토큰. 노트 본문 Read 없음.

## 4가지 검색

| 검색 | 역할 | 데이터 |
|------|------|--------|
| **키워드** | 정확히 찾기 | claim + tags 매칭 |
| **링크 탐색** | 맥락 따라가기 | links[] 1-2홉 + 백링크 |
| **유사 노트** | 생각 확장하기 | 태그 겹침 + 같은 클러스터 |
| **관계 검색** | 새 연결 발견 | 공통 이웃의 '사촌' 노트 |

## 실행

1. `search.py` Bash 1회
2. JSON 해석
3. 경로별 상위 3개 + **교차 노트** 강조 + **다음 생각** 2-3개 제안

## 볼트 경로

```
VAULT_ROOT="/Users/futurewave/Library/CloudStorage/GoogleDrive-futurewave@gmail.com/내 드라이브/03 Resources/옵시디언 볼트/futurewave"
```
