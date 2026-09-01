---
name: do-brain
description: 제텔카스텐 클러스터 폴더(허브+하위노트)를 알프레도 방식의 엔티티-관계 YAML(brain.yml)로 압축하고, 그 폴더에 brain.yml을 우선 참고하라는 CLAUDE.md를 만든다. "brain.yml 만들어줘", "지식그래프로 압축해줘", "do-brain", "brain 스킬" 등을 언급하면 사용한다.
---

# do-brain — 클러스터 폴더를 brain.yml로 압축

> 원리 출처: [[0035]]·[[0035a]]·[[0035c]] (알프레도 SSOT 봇 아키텍처). 산문 요약 대신 엔티티-관계 모델을 쓰는 이유, 무효화 규칙의 필요성은 그 노트들에 있다. 이 스킬은 그 패턴을 **임의의 클러스터 폴더**에 일반화한다.

## 트리거

`/do-brain <폴더 경로>` 또는 "brain.yml 만들어줘", "지식그래프로 압축해줘"

폴더를 지정하지 않으면 사용자에게 대상 폴더를 확인한다 (AskUserQuestion 또는 일반 질문).

## 언제 쓰나

- `2 Permanent/` 안의 특정 클러스터(허브 노트 + 하위 노트들, 예: `0035 알프레도 지식그래프 봇/`)가 문서·가이드·로드맵까지 여러 파일로 불어나서, 매번 폴더 전체를 읽지 않고도 사실 조회에 답할 수 있는 단일 참조 파일이 필요할 때
- 이미 `brain.yml`이 있는 폴더인데 노트가 추가/수정되어 갱신이 필요할 때 (기존 파일을 감지해 재생성)

## 하지 않는 것

- 원본 노트를 대체하지 않는다. 깊은 추론·서사·연결분석이 필요한 질문에는 여전히 원본 `.md`를 읽어야 한다.
- 자동 실시간 동기화가 아니다. 이 스킬을 실행한 시점의 스냅샷이다. 갱신은 Step 5(CLAUDE.md 규칙)와 `/do-permanent` 연동으로 유도하지만, 최종 실행은 여전히 대화 안에서 스킬을 호출해야 일어난다.

---

## Step 1: 대상 폴더 확정

사용자가 폴더를 지정하지 않았으면 확인한다. 폴더는 보통 `2 Permanent/<클러스터>/` 형태이며 허브 노트(`type: permanent`, `parent: ""`)와 그 자식들을 포함한다.

## Step 2: 폴더 스캔 — 개별 노트를 깊이 읽지 않는다

**원칙(do-permanent와 동일):** 가능한 한 frontmatter만으로 그래프를 구성한다. 본문을 여는 것은 frontmatter의 `claim`만으로 description이 불충분할 때(예: 구현 가이드처럼 `claim` 필드가 없는 `type: plan` 문서)로 제한한다.

1. 대상 폴더의 모든 `.md` 파일 frontmatter를 읽는다 (`type`, `id`, `status`, `parent`, `claim`, `links`, `cluster`, `tags`).
2. `type: permanent` 문서 → Note 엔티티. `type: plan`(가이드·로드맵 등) → Doc 엔티티.
3. 하위 폴더(예: `원본자료/`)의 원천 자료는 개별 엔티티로 만들지 않는다 — 이미 permanent 노트들이 그 내용을 소화했다고 간주하고, 필요 시 각 Note 엔티티의 `attributes.source`에 파일명만 남긴다.
4. 이 세션에서 이미 만든 학습 정리 md/PT 같은 파생물이 있으면 `type: derived_summary` 하나로 뭉뚱그려 넣는다 (개별 슬라이드까지 엔티티화하지 않는다).

## Step 3: 엔티티 변환 규칙

**Note 엔티티 (permanent):**
```yaml
Note_<ID>:
  status: active                      # frontmatter status 이모지는 attributes.status_marker로 보존, 여기는 active/deprecated만
  type: permanent_note
  description: "<claim을 그대로 또는 다듬어서. 이미 압축된 한 문장이므로 대개 재가공 불요>"
  attributes:
    zettel_id: "<id>"
    cluster: "<cluster>"
    tags: "<tags 상위 5개 정도>"
  relations:
    - type: PART_OF
      target: Cluster_<허브ID>        # 허브 자신이 아니면
    - type: RELATES_TO               # links[] 각 항목마다. 대상이 이 폴더 안이면 그대로, 밖이면 Ext_ 스텁으로
      target: <Note_ID 또는 Ext_ID>
```

**Doc 엔티티 (plan/가이드/로드맵 등 claim이 없는 문서):**
- description은 문서 제목 + 첫 요약 문단에서 1~2문장만 추출 (본문 전체를 옮기지 않는다)
- `attributes`에는 그 문서의 핵심 절차·수치·표만 압축해 넣는다 (원문 표현을 문장으로 풀어쓰지 말고 `key: value` 형태로)
- relations: `DERIVED_FROM` → 근거가 된 Note 엔티티들, `PART_OF` → Cluster

**Cluster 엔티티 (허브 노트 자신):**
- 허브 노트(`parent: ""`)를 `Cluster_<ID>`로 승격
- `HAS_CHILD` relations로 하위 노트 전부 연결

**Ext_ 스텁 (폴더 밖 링크):**
- `_index/VAULT_INDEX.md`를 Read해서 해당 ID의 `Claim` 컬럼 값을 그대로 `description`으로 쓴다 (개별 노트를 열지 않는다)
- VAULT_INDEX에 없으면 `description: "전체 내용은 <ID> 노트 참조"`만

## Step 4: 헤더 주석 + 저장

파일 상단에 다음 블록을 **항상** 포함한다 (내용은 대상 클러스터에 맞게 치환):

```yaml
# =========================================================
# brain.yml — "<폴더명>" 폴더의 지식그래프
#
# 이 파일은 폴더 안 노트/문서의 핵심 사실을 엔티티-관계 모델로 압축한 것이다.
# 원본 문서를 대체하지 않는다 — 빠른 질의응답을 위한 단일 참조 파일이다.
#
# [허용 relation type]
#   HAS_CHILD · PART_OF · DERIVED_FROM · RELATES_TO · CONTRASTS_WITH
#   REQUIRES · GOVERNS · VALIDATES · IMPLEMENTS · MEASURED_BY
#
# [작성 금지]
#   description·attributes 안에 다른 엔티티 이름을 산문으로 결합해 쓰지 말 것.
#   결합은 relations로만 표현한다. (근거: 0035a)
#
# [무효화 규칙]
#   폴더 안 .md 파일이 추가/수정되면 이 파일도 갱신해야 한다.
#   자동 동기화 장치는 없다 — 같은 폴더의 CLAUDE.md가 그 책임을 사람/에이전트에게 위임한다.
#   최종 갱신 기준: <YYYY-MM-DD>
# =========================================================
```

- **저장 위치·파일명:** 대상 폴더 안에 `brain.yml`. 이미 `*-brain.yml`(예: `alfred-brain.yml`)처럼 다른 이름의 파일이 존재하면 새로 만들지 말고 **그 파일을 갱신**한다.
- relation type 어휘집은 클러스터 성격에 따라 늘려도 되지만 20개를 넘기지 않는다.

## Step 5: 폴더 CLAUDE.md 생성/갱신

같은 폴더에 `CLAUDE.md`가 없으면 새로 만들고, 있으면 아래 블록이 없을 때만 추가한다 (기존 내용 유지, surgical하게 append).

```markdown
# CLAUDE.md — <폴더명>

이 폴더에서 작업할 때는 <brain.yml 파일명>을 먼저 참고한다.

- **사실 조회**(수치·정의·구조 확인)는 <brain.yml 파일명>만 읽고 답한다. 폴더 전체를 다시 읽지 않는다.
- **깊은 추론·서사·연결분석**이 필요한 질문은 원본 노트(.md)를 연다. <brain.yml 파일명>은 원본을 대체하지 않는다.
- **이 폴더에 새 영구노트가 생기거나 기존 노트의 claim/links/status가 바뀌면, 그 작업을 끝내기 전에 `/do-brain`으로 <brain.yml 파일명>을 갱신한다.** 갱신을 건너뛰면 이 파일이 낡은 채로 답변에 쓰이게 된다 — 이게 정확히 [[0035c]]가 경고한 실패 모드다.
```

## Step 6: 완료 보고

1~3줄로: 생성/갱신된 엔티티 수, 파일 경로, CLAUDE.md 생성 여부만 보고한다. 전체 YAML을 채팅에 다시 붙여넣지 않는다 (사용자가 원하면 별도 요청 시).

---

## `/do-permanent`와의 연동

`/do-permanent`로 새 영구노트가 그 폴더에 저장되면, cascade.py 실행 직후 그 폴더에 `brain.yml`(또는 `*-brain.yml`)이 이미 존재하는지 확인한다. 존재하면 이 스킬(Step 2~4)을 이어서 실행해 갱신한다. 이 연동 스텝은 `do-permanent/SKILL.md`의 Step 6에 등록되어 있다.
