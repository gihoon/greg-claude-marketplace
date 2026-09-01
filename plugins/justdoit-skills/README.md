# justdoit-skills

지식관리 파이프라인과 아이디어 파이프라인을 하나로 묶은 Claude Code 스킬 패키지.

> **출처**
> - 원본 저장소: [kimyoon21/brown-claude-marketplace](https://github.com/kimyoon21/brown-claude-marketplace)
> - 참고 자료: [vibelabs.kr/shared/8](https://vibelabs.kr/shared/8)

## 스킬 목록

### 지식관리 파이프라인 (Zettelkasten)

```
/do-fleeting → /do-literature → /do-permanent → /do-wiki
                        ↓
              /do-index  /do-query  /do-lint  /do-brain
```

| 스킬 | 설명 |
|------|------|
| `/do-fleeting` | 임시노트 즉시 저장. `/do-fleeting scan`으로 미처리 목록 확인 후 영구노트 전환 |
| `/do-literature` | 문헌노트 생성. 읽은 자료를 자기 말로 소화해 `1 Literature/`에 저장 |
| `/do-permanent` | 원자적 영구노트 생성. VAULT_INDEX 연결 + cascade.py 후처리 |
| `/do-wiki` | 클러스터 개념 허브 페이지 생성 |
| `/do-index` | 프론트매터 기반 VAULT_INDEX 자동 생성·갱신 (perm·query·lint의 토대) |
| `/do-query` | 볼트 4-Way 검색 (키워드·태그·클러스터·연결 기준) |
| `/do-lint` | 볼트 건강 점검 (고아 노트, 깨진 링크, 미처리 raw) |
| `/do-brain` | 클러스터 폴더를 엔티티-관계 brain.yml로 압축 + 참조용 CLAUDE.md 생성. `/do-permanent`가 새 노트 저장 시 자동 갱신 연동 |

### 아이디어 파이프라인

```
/do-sharpen → /do-productify
```

| 스킬 | 설명 |
|------|------|
| `/do-sharpen` | 모호한 아이디어·요청을 구체적인 명세서로 다듬기 |
| `/do-productify` | 명세서를 받아 최적 제품 형태 결정 + 페이즈별 로드맵 설계 |

### 리포트·발표

| 스킬 | 설명 |
|------|------|
| `/do-report` | 기관 리서치 리포트를 A4 PDF로 생성 (Chrome headless 렌더) |
| `/do-genpt` | 에디토리얼 슬라이드 덱(HTML) — 흑백 종이 질감, 세로 스크롤 |
| `/do-hotpt` | 네이비 러스트 IR 덱(HTML) — 다크↔라이트 교차 16:9, 투자유치 |
| `/do-hotreport` | 네이비 러스트 A4 1p 요약서(HTML) — 초고밀도 한 장 브리프 |
| `/do-hotpdf` | 완성된 HTML을 PDF로 렌더 — 문서(A4 세로)·덱(16:9 가로) 자동 판별 |

### 검증·자동화

| 스킬 | 설명 |
|------|------|
| `/do-critique` | 명세·기획 노트 적대적 검증 — 미검증 가정·경쟁 누락·논리 구멍 탐지 |
| `/do-ingest` | PDF·URL·이미지를 문헌노트로 일괄 인제스트 |
| `/do-relink` | frontmatter links[] 기반 양방향 링크·VAULT_INDEX 재정합 |
| `/do-refactor` | 노트 이동·ID 재배치·병합·분할 시 링크 정합 유지 |
| `/do-breakdown` | 큰 노트를 원자적 하위 영구노트들로 분해 |
| `/do-compile` | 볼트 노트들을 슬라이드·리포트로 컴파일 |
| `/do-research` | 웹 검색으로 시장·경쟁·기술 근거 수집·보강 |
| `/do-decide` | 제품·아키텍처 결정을 ADR 형식으로 기록 |

## 사용 예시

```
/do-fleeting 오늘 미팅에서 나온 아이디어 메모
/do-permanent 새로운 인사이트 정리
/do-query 지식관리 관련 노트 찾아줘
/do-sharpen 이 아이디어를 제품 명세로 만들어줘
/do-critique ./spec.md
/do-productify
/do-compile pt AI에이전트
```
