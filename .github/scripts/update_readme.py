import os
import re


def find_markdowns():
    base_dir = os.path.dirname(__file__)  # 스크립트 파일의 위치
    readme_path = os.path.join(base_dir, '../../README.md')
    md_files = []
    md_files_with_absolute_path = {}
    # 변경된 .md 파일 탐색
    target_dir = os.path.abspath(os.path.join(base_dir, '../../'))
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.md') and 'README' not in file:
                rel_path = os.path.relpath(os.path.join(root, file), start=target_dir)  # Get relative path
                md_files.append(rel_path)
                md_files_with_absolute_path[rel_path] = file
    return md_files, readme_path, md_files_with_absolute_path


def parse_md_filename(filename):
    """
    파일 이름에서 장, 아이템, 제목, 작성자를 파싱.
    """
    pattern = r'(\d+)장/아이템_(\d+)/([^/]+)_(\w+)\.md'
    match = re.match(pattern, filename)
    if match:
        return match.groups()
    raise Exception(filename)


def update_readme():
    md_files, readme_path, md_files_with_absolute_path = find_markdowns()
    entries = {}
    chapters = set()
    for md_file in md_files:
        try:
            chapter, item, title, author = parse_md_filename(md_file)
            key = (int(chapter), int(item), title)
            link = f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}/blob/master/{md_file}"
            if key not in entries:
                entries[key] = []
            entries[key].append((author, link))
            chapters.add(int(chapter))
        except Exception as e:
            file_name = str(e)
            print('이거 이상한 파일인데요? -> ' + file_name + " path: " + md_files_with_absolute_path[file_name])

    sorted_entries = sorted(entries.items(),reverse=True)
    sorted_chapters = sorted(chapters,reverse=True)

    with open(readme_path, 'r+', encoding="UTF-8") as readme:
        content = readme.readlines()

        # 각 장의 테이블을 업데이트 또는 생성
        for chapter in sorted_chapters:
            chapter_tables = find_chapter_table_index(content)
            if chapter not in chapter_tables or chapter_tables[chapter]['end'] == chapter_tables[chapter]['start']:
                insert_index = chapter_tables[chapter]['start']
                header = '<table>\n<tr><th>아이템🍳</th><th>주제</th><th>작성자의 글</th></tr>\n'
                content.insert(insert_index, header)
                content.insert(insert_index + 1, '</table>\n')
                chapter_tables[chapter]['start'] += 1
                chapter_tables[chapter]['end'] = insert_index + 1

            table_start = chapter_tables[chapter]['start']
            table_end = chapter_tables[chapter]['end']
            existing_entries = {}
            for line in content[table_start:table_end]:
                if '<tr><td>' in line:
                    item = int(line.split('<td>')[1].split('</td>')[0].strip())
                    existing_entries[item] = line

            insert_index = table_end
            for entry, authors_links in sorted_entries:
                chapter_tables = find_chapter_table_index(content)
                chapter_num, item, title = entry
                if chapter_num != chapter:
                    continue
                title = title.replace("_", " ")
                authors_links_str = ', '.join([f'<a href="{link}">{author}의 글</a>' for author, link in authors_links])
                line = f'<tr><td> {item} </td><td> {title} </td><td> {authors_links_str} </td></tr>\n'
                if item not in existing_entries.keys():
                    current_line = content[insert_index]
                    item_num = -1
                    if '<tr><td>' in current_line:
                        item_num = int(content[insert_index].split('<td>')[1].split('</td>')[0].strip())
                        while insert_index > table_start and item_num > item:
                            insert_index -= 1
                    content.insert(insert_index, line)
                    # chapter_tables[chapter]['end'] += 1  # 중요: 테이블 끝 위치 갱신
                    
                else:
                    existing_index = content.index(existing_entries[item])
                    content[existing_index] = line

        readme.seek(0)
        readme.writelines(content)
        readme.truncate()


def find_chapter_table_index(content):
    list_section_start_index = content.index('## 글 목록\n') + 1
    list_section_end_index = content.index('------\n')
    chapter_tables = {}
    current_chapter = 0
    # 장의 시작 위치와 테이블의 위치를 찾기
    for i in range(list_section_start_index, list_section_end_index):
        if re.search(r'^\s*### (\d+) 장', content[i]):
            current_chapter = int(re.search(r'(\d+)', content[i]).group())
            if current_chapter not in chapter_tables:
                chapter_tables[current_chapter] = {'start': i + 1, 'end': i + 1}

        if current_chapter and '<table>' in content[i]:
            chapter_tables[current_chapter]['start'] = i
        if current_chapter and '</table>' in content[i]:
            chapter_tables[current_chapter]['end'] = i
            current_chapter = 0
    return chapter_tables


if __name__ == '__main__':
    update_readme()
