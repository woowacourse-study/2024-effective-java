import os
import re


def parse_md_filename(filename):
    """
    파일 이름에서 장, 아이템, 제목, 작성자를 파싱.
    """
    pattern = r'(\d+)장/아이템_(\d+)/([^/]+)_(\w+)\.md'
    match = re.match(pattern, filename)
    if match:
        return match.groups()
    return None


def update_readme():
    md_files, readme_path = find_markdowns()

    # 파일 정보를 읽어 정렬
    entries = {}
    for md_file in md_files:
        chapter, item, title, author = parse_md_filename(md_file)
        key = (int(chapter), int(item), title)
        link = f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}/blob/master/{md_file}"
        if key not in entries:
            entries[key] = []
        entries[key].append((author, link))

    # 장과 아이템 번호로 정렬
    sorted_entries = sorted(entries.items())

    # README.md 업데이트
    with open(readme_path, 'r+', encoding="UTF-8") as readme:
        content = readme.readlines()
        insert_index = content.index('## 글 목록\n') + 2  # '## 글 목록' 섹션을 찾아 그 다음에 삽입

        header = '<table>\n<tr><th>장</th><th>아이템🍳</th><th>주제</th><th>작성자의 글</th></tr>\n'
        if '<table>' not in content:
            content.insert(insert_index, header)
            insert_index += 1

        for entry, authors_links in sorted_entries:
            chapter, item, title = entry
            title = title.replace("_"," ")
            authors_links_str = ', '.join([f'<a href="{link}">{author}의 글</a>' for author, link in authors_links])
            line = f'<tr><td>{chapter}장</td><td>아이템 {item}</td><td>{title}</td><td>{authors_links_str}</td></tr>\n'
            if line not in content:
                content.insert(insert_index, line)
                insert_index += 1

        content.insert(insert_index, '</table>\n')

        readme.seek(0)
        readme.writelines(content)
        readme.truncate()


def find_markdowns():
    base_dir = os.path.dirname(__file__)  # 스크립트 파일의 위치
    readme_path = os.path.join(base_dir, '../../README.md')
    md_files = []
    # 변경된 .md 파일 탐색
    target_dir = os.path.abspath(os.path.join(base_dir, '../../'))
    for root, dirs, files in os.walk(target_dir):
        for file in files:
            if file.endswith('.md') and 'README' not in file:
                rel_path = os.path.relpath(os.path.join(root, file), start=target_dir)  # Get relative path
                md_files.append(rel_path)
    return md_files, readme_path


if __name__ == '__main__':
    update_readme()
