import os
import re
from html_generator import markdown_to_html_node


def extract_title(markdown):
    splitted = re.split(r"^#\s+", markdown.lstrip())
    if len(splitted) > 1:
        return splitted[1]
    else:
        raise Exception("string does not start with one '# '")


def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    with open(from_path, "r") as f:
        markdown_content = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        print(source_path, dest_path)

        if os.path.isfile(source_path) and source_path.endswith(".md"):
            generate_page(source_path, template_path, dest_path.replace(".md", ".html"))
        else:
            generate_pages_recursive(source_path, template_path, dest_path)
