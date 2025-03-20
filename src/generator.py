import os
import re
from pathlib import Path

from helpers import markdown_to_html_node


def extract_title(markdown: str) -> str:
    pattern = r"^# (.+)"
    match = re.search(pattern, markdown, re.MULTILINE)
    if not match:
        raise ValueError("H1 tag is not found")
    line = match.group(1)
    return line.strip()


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print((
        f"Generating page from {from_path} to "
        f"{dest_path} using {template_path}"
    ))

    try:
        src_file = open(from_path, "r")
        template_file = open(template_path, "r")

        src_file_content = src_file.read()
        markdown_html = markdown_to_html_node(src_file_content).to_html()
        title = extract_title(src_file_content)

        template_content = template_file.read()
        template_content = template_content.replace("{{ Title }}", title)
        template_content = template_content.replace("{{ Content }}", markdown_html)

        path_dir = os.path.dirname(dest_path)
        if path_dir:
            os.makedirs(path_dir, exist_ok=True)

        dest_file = open(dest_path, "w")
        dest_file.write(template_content)

    except Exception:
        raise
    finally:
        src_file.close()
        template_file.close()
        dest_file.close()


def generate_pages_recursive(
    src_path: str,
    template_path: str,
    dest_path: str
) -> None:
    dir_list = os.listdir(src_path)
    for item in dir_list:
        full_src_path = os.path.join(src_path, item)
        full_dest_path = os.path.join(dest_path, item)
        if os.path.isdir(full_src_path):
            print(f"Creating folder for path: {full_src_path}")
            generate_pages_recursive(
                full_src_path,
                template_path,
                full_dest_path
            )
        else:
            full_dest_path = Path(full_dest_path).with_suffix(".html")
            print(f"Generating html file for path: {full_dest_path}")
            generate_page(full_src_path, template_path, full_dest_path)
