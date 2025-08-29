import re

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        return ''.join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None and self.tag != "img":
            raise ValueError("LeafNode must have a value unless it's an image")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        if self.tag == "img":
            return f'<{self.tag}{props_str}/>'
        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        props_str = self.props_to_html()
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{props_str}>{children_html}</{self.tag}>'

class TextType:
    NEWLINE = "newline"

def extract_markdown_links(text):
    pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    return list(pattern.finditer(text))

def extract_markdown_images(text):
    pattern = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
    return list(pattern.finditer(text))

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    newNodes = []
    for node in old_nodes:
        if isinstance(node, LeafNode) and node.tag is None:
            parts = node.value.split(delimiter)
            for i, part in enumerate(parts):
                if part:
                    newNodes.append(LeafNode(None, part))
                if i < len(parts) - 1:
                    newNodes.append(LeafNode("br", ""))
        else:
            newNodes.append(node)
    return newNodes
def split_nodes_italic(old_nodes):
    newNodes = []
    pattern = re.compile(r'(\*[^*]+\*|_[^_]+_)')
    for node in old_nodes:
        if isinstance(node, LeafNode) and node.tag is None:
            matches = list(pattern.finditer(node.value))
            last_index = 0
            for match in matches:
                if match.start() > last_index:
                    newNodes.append(LeafNode(None, node.value[last_index:match.start()]))
                text = match.group(0)[1:-1]  # Remove * or _
                newNodes.append(LeafNode("i", text))
                last_index = match.end()
            if last_index < len(node.value):
                newNodes.append(LeafNode(None, node.value[last_index:]))
        else:
            newNodes.append(node)
    return newNodes
def split_nodes_image(old_nodes):
    newNodes = []
    for node in old_nodes:
        if isinstance(node, LeafNode) and node.tag is None:
            matches = extract_markdown_images(node.value)
            if not matches:
                newNodes.append(node)
                continue
            last_index = 0
            for match in matches:
                if match.start() > last_index:
                    newNodes.append(LeafNode(None, node.value[last_index:match.start()]))
                alt_text, url = match.groups()
                newNodes.append(LeafNode("img", None, {"src": url, "alt": alt_text}))
                last_index = match.end()
            if last_index < len(node.value):
                newNodes.append(LeafNode(None, node.value[last_index:]))
        else:
            newNodes.append(node)
    return newNodes

def split_nodes_link(old_nodes):
    newNodes = []
    for node in old_nodes:
        if isinstance(node, LeafNode) and node.tag is None:
            matches = extract_markdown_links(node.value)
            if not matches:
                newNodes.append(node)
                continue
            last_index = 0
            for match in matches:
                if match.start() > last_index:
                    newNodes.append(LeafNode(None, node.value[last_index:match.start()]))
                link_text, url = match.groups()
                newNodes.append(LeafNode("a", link_text, {"href": url}))
                last_index = match.end()
            if last_index < len(node.value):
                newNodes.append(LeafNode(None, node.value[last_index:]))
        else:
            newNodes.append(node)
    return newNodes

def split_nodes_code(old_nodes):
    newNodes = []
    pattern = re.compile(r'(`+)(.+?)\1')
    for node in old_nodes:
        if isinstance(node, LeafNode) and node.tag is None:
            matches = list(pattern.finditer(node.value))
            last_index = 0
            for match in matches:
                if match.start() > last_index:
                    newNodes.append(LeafNode(None, node.value[last_index:match.start()]))
                code_text = match.group(2)  # Extract code text
                newNodes.append(LeafNode("code", code_text))
                last_index = match.end()
            if last_index < len(node.value):
                newNodes.append(LeafNode(None, node.value[last_index:]))
        else:
            newNodes.append(node)
    return newNodes

def split_nodes_bold(old_nodes):
    newNodes = []
    pattern = re.compile(r'(\*\*[^*]+\*\*|__[^_]+__)')
    for node in old_nodes:
        if isinstance(node, LeafNode) and node.tag is None:
            matches = list(pattern.finditer(node.value))
            last_index = 0
            for match in matches:
                if match.start() > last_index:
                    newNodes.append(LeafNode(None, node.value[last_index:match.start()]))
                text = match.group(0)[2:-2]  # Remove ** or __
                newNodes.append(LeafNode("b", text))
                last_index = match.end()
            if last_index < len(node.value):
                newNodes.append(LeafNode(None, node.value[last_index:]))
        else:
            newNodes.append(node)
    return newNodes

def text_to_textnodes(text):
    return split_nodes_image(
        split_nodes_code(
        split_nodes_link(
            split_nodes_italic(
                split_nodes_bold(
                    split_nodes_delimiter([LeafNode(None, text)], '\n', TextType.NEWLINE)
                )
            )
        )
    ))

def markdown_to_blocks(markdown):
    import re
    lines = markdown.split('\n')
    blocks = []
    current_paragraph = []
    i = 0
    numbered_list_pattern = re.compile(r'^\d+\.\s*(.*)')

    while i < len(lines):
        line = lines[i]
        if line.startswith('#'):
            if current_paragraph:
                blocks.append(ParentNode("p", text_to_textnodes(''.join(node.value for node in current_paragraph))))
                current_paragraph = []
            header_level = len(line) - len(line.lstrip('#'))
            header_text = line.lstrip('#').strip()
            blocks.append(ParentNode(f'h{header_level}', text_to_textnodes(header_text)))
            i += 1

        elif line.startswith('>'):
            if current_paragraph:
                blocks.append(ParentNode("p", text_to_textnodes(''.join(node.value for node in current_paragraph))))
                current_paragraph = []
            quote_lines = []
            while i < len(lines) and lines[i].startswith('>'):
                quote_lines.append(lines[i][1:].strip())
                i += 1
            quote_text = ' '.join(quote_lines)
            blocks.append(ParentNode("blockquote", text_to_textnodes(quote_text)))

        elif line.startswith('- '):
            if current_paragraph:
                blocks.append(ParentNode("p", text_to_textnodes(''.join(node.value for node in current_paragraph))))
                current_paragraph = []
            list_items = []
            while i < len(lines) and lines[i].startswith('- '):
                item_text = lines[i][2:].strip()
                list_items.append(ParentNode("li", text_to_textnodes(item_text)))
                i += 1
            blocks.append(ParentNode("ul", list_items))

        elif numbered_list_pattern.match(line):
            if current_paragraph:
                blocks.append(ParentNode("p", text_to_textnodes(''.join(node.value for node in current_paragraph))))
                current_paragraph = []
            list_items = []
            while i < len(lines) and numbered_list_pattern.match(lines[i]):
                match = numbered_list_pattern.match(lines[i])
                item_text = match.group(1).strip() if match else ''
                list_items.append(ParentNode("li", text_to_textnodes(item_text)))
                i += 1
            blocks.append(ParentNode("ol", list_items))

        elif line.strip() == '':
            if current_paragraph:
                blocks.append(ParentNode("p", text_to_textnodes(''.join(node.value for node in current_paragraph))))
                current_paragraph = []
            i += 1
        elif line.startswith('```'):
            if current_paragraph:
                blocks.append(ParentNode("p", text_to_textnodes(''.join(node.value for node in current_paragraph))))
                current_paragraph = []
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Skip closing ```
            code_content = '\n'.join(code_lines)
            blocks.append(ParentNode("pre", [LeafNode("code", code_content)]))

        else:
            current_paragraph.append(LeafNode(None, line))
            i += 1

    if current_paragraph:
        blocks.append(ParentNode("p", text_to_textnodes(''.join(node.value for node in current_paragraph))))
    return blocks
def markdown_to_html_node(markdown):
    return ParentNode("div", markdown_to_blocks(markdown))

def markdown_to_html(markdown):
    return markdown_to_html_node(markdown).to_html()