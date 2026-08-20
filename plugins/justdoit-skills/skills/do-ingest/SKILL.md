---
name: do-ingest
description: PDF·URL·이미지·텍스트 클립을 문헌노트(Literature Note)로 일괄 인제스트. /do-literature의 배치 버전 — 출처 파싱·페이지 인용·요약 자동 처리 후 `1 Literature/`에 저장. "ingest", "논문 넣어줘", "URL 정리해줘", "PDF 소화해줘" 등을 언급하면 사용한다.
---

# /do-ingest — 소스 일괄 인제스트

## 트리거
`/do-ingest` 또는 `/ingest`

## 사용법
```
/do-ingest https://...              # URL 단건
/do-ingest ./paper.pdf              # PDF 단건
/do-ingest scan                     # 0 raw/의 미처리 소스 목록 → 일괄 처리
```

## 파이프라인

**Step 1: 소스 타입 판별**
- URL / PDF / 이미지 / 텍스트 클립 자동 감지
- 이미 처리된 소스(URL·파일명 중복)는 건너뜀

**Step 2: 텍스트 추출 + 메타데이터 파싱**
- 저자·제목·발행일·URL·DOI 추출
- PDF: 페이지별 핵심 단락 추출

**Step 3: 자기 말로 요약 + 핵심 개념 추출**
- 3개 이하 핵심 개념에 `/do-permanent` 연결 후보 표시
- 원문 인용은 `>` 블록쿼트로 출처 명시

**Step 4: 문헌노트 저장**
- `/do-literature` 형식으로 `1 Literature/`에 저장
- frontmatter: `type: literature`, `source:`, `processed: true`

## 핵심 원칙
- 원문 복사가 아닌 소화·요약이 목적
- 중복 소스 자동 건너뜀
- 처리 완료 raw 파일에 `processed: true` 플래그
