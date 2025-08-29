from textnode import TextNode
from textnode import TextType
import re
import os
def main():
    newnode = TextNode("Example Text", TextType.PLAIN_TEXT)
    print(newnode)
    #delete files in public folder
    for filename in os.listdir("public/"):
        file_path = os.path.join("public/", filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    #move all files from static to public
    for filename in os.listdir("static/"):
        src_path = os.path.join("static/", filename)
        dst_path = os.path.join("public/", filename)
        move_file(src_path, dst_path)
    generate_pages_recursive("content", "template.html", "public")
def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    images = [{'alt': alt, 'url': url} for alt, url in matches]
    return images

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    links = [{'text': text, 'url': url} for text, url in matches]
    return links

import shutil

def move_file(src, dst):
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copy(src, dst)

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    raise Exception("No title found in markdown")

from htmlnode import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    with open(from_path, 'r') as f:
        markdown = f.read()
    title = extract_title(markdown)
    # Convert markdown to HTML using your htmlnode logic
    html_node = markdown_to_html_node(markdown)
    content_html = html_node.to_html()
    with open(template_path, 'r') as f:
        template = f.read()
    html_content = template.replace("{{ Title }}", title)
    html_content = html_content.replace("{{ Content }}", content_html)
    with open(dest_path, 'w') as f:
        f.write(html_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, dirs, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                rel_dir = os.path.relpath(root, dir_path_content)
                rel_file = os.path.splitext(file)[0] + '.html'
                from_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir_path, rel_dir, rel_file)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()

