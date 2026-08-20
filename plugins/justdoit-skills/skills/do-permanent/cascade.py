#!/usr/bin/env python3
"""
Cascade Update Script — /do-permanent Step 5 토큰 절감용
Claude가 직접 Read/Edit하는 대신 이 스크립트가 일괄 처리.

Usage:
  python3 cascade.py <vault_root> <new_note_path> <new_id> <parent_id> <linked_ids...>

Example:
  python3 cascade.py "/path/to/vault" "2 Permanent/0025 제목/0025. 제목.md" "0025" "0024" "0023"

new_note_path: VAULT_ROOT 기준 상대 경로 (폴더 포함 가능)
"""
import sys, os, re, json

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def find_notes_by_id(vault_root, note_id):
    """2 Permanent/ 전체(하위 폴더 포함)에서 ID로 시작하는 .md 파일 목록 반환."""
    perm_root = os.path.join(vault_root, '2 Permanent')
    matches = []
    for dirpath, _, filenames in os.walk(perm_root):
        for f in filenames:
            if not f.endswith('.md'):
                continue
            if f.startswith(f'{note_id}.') or f.startswith(f'{note_id} '):
                matches.append(os.path.join(dirpath, f))
    return matches

def find_topic_folder(vault_root, top_id):
    """최상위 ID에 해당하는 폴더 찾기. 예: '0025' → '2 Permanent/0025 제목/'."""
    perm_root = os.path.join(vault_root, '2 Permanent')
    for entry in os.listdir(perm_root):
        full = os.path.join(perm_root, entry)
        if os.path.isdir(full) and (entry.startswith(f'{top_id} ') or entry == top_id):
            return full
    return None

def add_id_to_links(content, new_id):
    """frontmatter의 links[] 배열에 new_id 추가 (이미 있으면 스킵)."""
    pattern = r'(links:\s*\[)(.*?)(\])'
    match = re.search(pattern, content)
    if not match:
        return content, False
    existing = match.group(2)
    if f'"{new_id}"' in existing:
        return content, False
    new_links = f'{existing}, "{new_id}"' if existing.strip() else f'"{new_id}"'
    return content[:match.start()] + match.group(1) + new_links + match.group(3) + content[match.end():], True

def is_table_row(line):
    """VAULT_INDEX 표의 데이터 행인지 (헤더·구분선 제외)."""
    return line.startswith('|') and not line.startswith('| ID') and not line.startswith('|--')

def append_to_vault_index(vault_root, new_id, claim, tags, links, cluster):
    """VAULT_INDEX.md에 1줄 추가.

    두 형식을 모두 지원한다:
      ① 클러스터 헤딩(`## 클러스터: X`)으로 나뉜 인덱스 → 해당 섹션 표 끝에
      ② 헤딩 없는 단일 평면 표 인덱스        → 파일의 마지막 표 행 뒤에
    """
    idx_path = os.path.join(vault_root, '_index', 'VAULT_INDEX.md')
    if not os.path.exists(idx_path):
        return False
    content = read_file(idx_path)
    if f'| {new_id} |' in content:      # 이미 등재됨 — 중복 추가 금지
        return True
    tags_str = ', '.join(tags) if tags else ''
    links_str = ', '.join(links) if links else ''
    claim_esc = claim.replace('|', '\\|')   # claim 안의 파이프가 표를 깨뜨리지 않도록
    new_row = f'| {new_id} | {claim_esc} | {tags_str} | {links_str} |'
    lines = content.split('\n')

    # ① 클러스터 섹션이 있으면 그 섹션 표 끝에
    cluster_header = f'## 클러스터: {cluster}' if cluster else None
    if cluster_header and cluster_header in content:
        insert_idx = None
        for i, line in enumerate(lines):
            if cluster_header in line:
                for j in range(i + 1, len(lines)):
                    if lines[j].startswith('## ') or lines[j].startswith('---'):
                        insert_idx = j
                        break
                    if is_table_row(lines[j]):
                        insert_idx = j + 1
                if insert_idx is None:
                    insert_idx = len(lines)
                break
        if insert_idx is not None:
            lines.insert(insert_idx, new_row)
            write_file(idx_path, '\n'.join(lines))
            return True

    # ② 단일 평면 표: 마지막 데이터 행 뒤에
    last_row = None
    for i, line in enumerate(lines):
        if is_table_row(line):
            last_row = i
    if last_row is not None:
        lines.insert(last_row + 1, new_row)
        write_file(idx_path, '\n'.join(lines))
        return True
    return False

def update_graph(vault_root, new_id, links):
    """GRAPH.md에 1줄 추가."""
    graph_path = os.path.join(vault_root, '_index', 'GRAPH.md')
    if not os.path.exists(graph_path):
        return False
    content = read_file(graph_path)
    links_str = ', '.join(links) if links else ''
    new_line = f'{new_id} → {links_str}'
    if new_line in content:
        return True
    stats_idx = content.find('## 통계')
    if stats_idx > 0:
        content = content[:stats_idx] + new_line + '\n' + content[stats_idx:]
    else:
        content += '\n' + new_line
    write_file(graph_path, content)
    return True

def update_wiki_page(vault_root, cluster, new_id, claim):
    """해당 클러스터의 wiki 개념 페이지에 새 노트 1줄 추가."""
    if not cluster:
        return False
    wiki_path = os.path.join(vault_root, '1 wiki', f'{cluster}.md')
    if not os.path.exists(wiki_path):
        return False
    content = read_file(wiki_path)
    if f'[[{new_id}]]' in content:
        return True
    new_row = f'| [[{new_id}]] | {claim} |'
    for marker in ['## 교차 태그', '## 주요 흐름']:
        if marker in content:
            content = content.replace(marker, f'{new_row}\n\n{marker}')
            break
    count_match = re.search(r'note_count:\s*(\d+)', content)
    if count_match:
        old = int(count_match.group(1))
        content = content.replace(f'note_count: {old}', f'note_count: {old + 1}')
    body_count = re.search(r'(\d+)개 영구노트', content)
    if body_count:
        old = int(body_count.group(1))
        content = content.replace(f'{old}개 영구노트', f'{old + 1}개 영구노트')
    write_file(wiki_path, content)
    return True

def extract_frontmatter_field(content, field):
    match = re.search(rf'^{field}:\s*"?(.+?)"?\s*$', content, re.MULTILINE)
    return match.group(1).strip('"') if match else ''

def extract_links_array(content):
    match = re.search(r'links:\s*\[(.*?)\]', content)
    if match:
        return [x.strip().strip('"') for x in match.group(1).split(',') if x.strip()]
    return []

def extract_tags_array(content):
    tags, in_tags = [], False
    for line in content.split('\n'):
        if line.strip().startswith('tags:'):
            in_tags = True
            continue
        if in_tags:
            if line.strip().startswith('- '):
                tags.append(line.strip()[2:].strip())
            elif line.strip() and not line.strip().startswith('-'):
                break
    return tags

def get_top_id(note_id):
    """하위 ID에서 최상위 숫자 ID 추출. '0025a1' → '0025'."""
    match = re.match(r'^(\d+)', note_id)
    return match.group(1) if match else note_id

def main():
    if len(sys.argv) < 5:
        print("Usage: cascade.py <vault_root> <new_note_path> <new_id> <parent_id> [linked_ids...]")
        sys.exit(1)

    vault_root = sys.argv[1]
    new_note_relpath = sys.argv[2]
    new_id = sys.argv[3]
    parent_id = sys.argv[4]
    linked_ids = sys.argv[5:] if len(sys.argv) > 5 else []

    new_note_path = os.path.join(vault_root, new_note_relpath)
    if not os.path.exists(new_note_path):
        print(f"ERROR: {new_note_path} not found")
        sys.exit(1)

    new_content = read_file(new_note_path)
    claim = extract_frontmatter_field(new_content, 'claim')
    cluster = extract_frontmatter_field(new_content, 'cluster')
    all_links = extract_links_array(new_content)
    tags = extract_tags_array(new_content)

    results = {"cascade": [], "index": {}, "warnings": []}

    # 1. 부모 노트: 하위 폴더까지 재귀 탐색 후 child link 추가
    if parent_id:
        parent_files = find_notes_by_id(vault_root, parent_id)
        if not parent_files:
            results["warnings"].append(f"parent {parent_id} not found")
        for ppath in parent_files:
            pcontent = read_file(ppath)
            pcontent, changed = add_id_to_links(pcontent, new_id)
            if changed:
                write_file(ppath, pcontent)
                rel = os.path.relpath(ppath, vault_root)
                results["cascade"].append({"path": rel, "change": "structural"})

    # 2. 연결 노트: 역방향 links[] 추가 (재귀 탐색)
    for lid in linked_ids:
        if lid == parent_id:
            continue
        for mpath in find_notes_by_id(vault_root, lid):
            mcontent = read_file(mpath)
            mcontent, changed = add_id_to_links(mcontent, new_id)
            if changed:
                write_file(mpath, mcontent)
                rel = os.path.relpath(mpath, vault_root)
                results["cascade"].append({"path": rel, "change": "semantic"})

    # 3. VAULT_INDEX & GRAPH 갱신
    results["index"]["vault_index"] = append_to_vault_index(vault_root, new_id, claim, tags, all_links, cluster)
    results["index"]["graph"] = update_graph(vault_root, new_id, all_links)

    # 4. Wiki 개념 페이지 갱신
    results["index"]["wiki"] = update_wiki_page(vault_root, cluster, new_id, claim)

    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
