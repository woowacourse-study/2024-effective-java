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
    entries = []
    for md_file in md_files:
        chapter, item, title, author = parse_md_filename(md_file)
        link = f"https://github.com/{os.getenv('GITHUB_REPOSITORY')}/blob/master/{md_file}"
        entries.append((int(chapter), int(item), title, author, link))

    # 장과 아이템 번호로 정렬
    entries.sort()

    # README.md 업데이트
    with open(readme_path, 'r+', encoding="UTF-8") as readme:
        content = readme.readlines()
        insert_index = content.index('## 글 목록\n') + 2  # '## 글 목록' 섹션을 찾아 그 다음에 삽입


        header = '| 장 | 아이템 | 주제(작성글 링크) | 작성자 |\n'
        divider = '|:---:|:---:|:--------:|:-----:|\n'  # 열 구분자 추가
        if header not in content:
            content.insert(insert_index, header)
            insert_index += 1
        if divider not in content:
            content.insert(insert_index, divider)
            insert_index += 1

        for entry in entries:
            chapter, item, title, author, link = entry
            title = title.replace("_",  " ")
            line = f'| {chapter}장 | 아이템 {item} | [{title}]({link}) | {author} |\n'
            if line not in content:
                content.insert(insert_index, line)
                insert_index += 1

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
