#!/usr/bin/env python3
"""
제텔카스텐 4-Way Search Engine
키워드 + 링크 탐색 + 유사 노트 + 관계 검색의 조합.
Claude 토큰 0. 결과만 JSON으로 출력.

Usage:
  python3 search.py <vault_root> "<검색어>"
"""

import os, re, sys, json, math
from collections import defaultdict, Counter

def parse_all_notes(vault_root):
    """2 Permanent/ 전체 노트의 frontmatter 파싱"""
    perm_dir = os.path.join(vault_root, '2 Permanent')
    notes = {}

    for f in os.listdir(perm_dir):
        if not f.endswith('.md'):
            continue
        filepath = os.path.join(perm_dir, f)
        with open(filepath, 'r', encoding='utf-8') as fh:
            content = fh.read()

        # frontmatter 파싱
        fm_match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            continue

        fm = fm_match.group(1)
        note_id = re.search(r'^id:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
        claim = re.search(r'^claim:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
        cluster = re.search(r'^cluster:\s*"?(.+?)"?\s*$', fm, re.MULTILINE)
        links_match = re.search(r'links:\s*\[(.*?)\]', fm)
        tags = []
        in_tags = False
        for line in fm.split('\n'):
            if line.strip().startswith('tags:'):
                in_tags = True
                continue
            if in_tags:
                if line.strip().startswith('- '):
                    tags.append(line.strip()[2:].strip())
                elif line.strip() and not line.strip().startswith('-'):
                    break

        note_id_val = note_id.group(1).strip('"') if note_id else ''
        if not note_id_val:
            continue

        links = []
        if links_match:
            links = [x.strip().strip('"') for x in links_match.group(1).split(',') if x.strip()]

        notes[note_id_val] = {
            'id': note_id_val,
            'claim': claim.group(1).strip('"') if claim else f.replace('.md', ''),
            'cluster': cluster.group(1).strip('"') if cluster else '',
            'tags': tags,
            'links': links,
            'filename': f,
        }

    return notes


def search_keyword(notes, query):
    """1. 키워드 검색: claim + tags에서 쿼리 단어 매칭"""
    words = query.lower().split()
    results = []

    for nid, note in notes.items():
        text = f"{note['claim']} {' '.join(note['tags'])} {note['cluster']}".lower()
        score = sum(1 for w in words if w in text)
        if score > 0:
            results.append({'id': nid, 'score': score, 'method': 'keyword'})

    return sorted(results, key=lambda x: -x['score'])[:10]


def search_links(notes, seed_ids):
    """2. 링크 탐색: seed에서 1-2홉 이내 연결된 노트"""
    visited = set(seed_ids)
    hop1 = set()
    hop2 = set()

    # 역방향 링크 맵 구축
    backlinks = defaultdict(set)
    for nid, note in notes.items():
        for link in note['links']:
            backlinks[link].add(nid)

    # 1홉
    for sid in seed_ids:
        if sid in notes:
            for link in notes[sid]['links']:
                if link not in visited:
                    hop1.add(link)
            for bl in backlinks.get(sid, set()):
                if bl not in visited:
                    hop1.add(bl)

    # 2홉
    for h1 in hop1:
        if h1 in notes:
            for link in notes[h1]['links']:
                if link not in visited and link not in hop1:
                    hop2.add(link)
            for bl in backlinks.get(h1, set()):
                if bl not in visited and bl not in hop1:
                    hop2.add(bl)

    results = []
    for nid in hop1:
        if nid in notes:
            results.append({'id': nid, 'score': 2, 'method': 'link_hop1'})
    for nid in hop2:
        if nid in notes:
            results.append({'id': nid, 'score': 1, 'method': 'link_hop2'})

    return results[:10]


def search_similar(notes, seed_ids):
    """3. 유사 노트: 태그 겹침 + 같은 클러스터 기반 추천"""
    if not seed_ids:
        return []

    # seed 노트들의 태그/클러스터 수집
    seed_tags = Counter()
    seed_clusters = set()
    for sid in seed_ids:
        if sid in notes:
            for tag in notes[sid]['tags']:
                seed_tags[tag] += 1
            seed_clusters.add(notes[sid]['cluster'])

    results = []
    for nid, note in notes.items():
        if nid in seed_ids:
            continue
        score = 0
        # 태그 겹침
        for tag in note['tags']:
            if tag in seed_tags:
                score += seed_tags[tag]
        # 클러스터 겹침
        if note['cluster'] in seed_clusters:
            score += 1
        if score > 0:
            results.append({'id': nid, 'score': score, 'method': 'similar'})

    return sorted(results, key=lambda x: -x['score'])[:10]


def search_relationship(notes, seed_ids):
    """4. 관계 검색: 같은 노트에 동시에 연결된 '사촌' 노트 (friends of friends)"""
    if not seed_ids:
        return []

    # seed가 연결된 노트들을 수집
    seed_neighbors = set()
    for sid in seed_ids:
        if sid in notes:
            seed_neighbors.update(notes[sid]['links'])

    # seed_neighbors에 연결된 다른 노트들 = 사촌
    cousins = Counter()
    for neighbor in seed_neighbors:
        if neighbor in notes:
            for link in notes[neighbor]['links']:
                if link not in seed_ids and link not in seed_neighbors:
                    cousins[link] += 1

    # 역방향도
    for nid, note in notes.items():
        if nid in seed_ids or nid in seed_neighbors:
            continue
        shared = len(set(note['links']) & seed_neighbors)
        if shared > 0:
            cousins[nid] += shared

    results = []
    for nid, count in cousins.most_common(10):
        if nid in notes:
            results.append({'id': nid, 'score': count, 'method': 'relationship'})

    return results


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 search.py <vault_root> \"<검색어>\"")
        sys.exit(1)

    vault_root = sys.argv[1]
    query = sys.argv[2]

    notes = parse_all_notes(vault_root)

    # 1. 키워드 검색
    keyword_results = search_keyword(notes, query)
    seed_ids = [r['id'] for r in keyword_results[:3]]

    # 2. 링크 탐색 (키워드 결과를 시드로)
    link_results = search_links(notes, seed_ids) if seed_ids else []

    # 3. 유사 노트
    similar_results = search_similar(notes, seed_ids) if seed_ids else []

    # 4. 관계 검색
    relationship_results = search_relationship(notes, seed_ids) if seed_ids else []

    # 결과 병합 + 중복 제거
    seen = set()
    all_results = []

    for r in keyword_results + link_results + similar_results + relationship_results:
        if r['id'] not in seen:
            seen.add(r['id'])
            note = notes[r['id']]
            all_results.append({
                'id': r['id'],
                'claim': note['claim'],
                'cluster': note['cluster'],
                'tags': note['tags'][:3],
                'method': r['method'],
                'score': r['score'],
            })

    output = {
        'query': query,
        'seed_notes': [{'id': sid, 'claim': notes[sid]['claim']} for sid in seed_ids if sid in notes],
        'results': {
            'keyword': [r for r in all_results if r['method'] == 'keyword'][:5],
            'link_traversal': [r for r in all_results if r['method'].startswith('link')][:5],
            'similar': [r for r in all_results if r['method'] == 'similar'][:5],
            'relationship': [r for r in all_results if r['method'] == 'relationship'][:5],
        },
        'total': len(all_results),
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
