from enum import Enum

class TextType(Enum):
    LINK = "link"
    IMAGE = "image"
    PLAIN_TEXT = "plainText"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ORDERED_LIST = "orderedList"
    UNORDERED_LIST = "unorderedList"

def block_to_block_type(block_str):
    if block_str.startswith("#"):
        return BlockType.HEADING
    elif block_str.startswith("```"):
        return BlockType.CODE
    elif block_str.startswith(">"):
        return BlockType.QUOTE
    elif block_str.startswith("1."):
        return BlockType.ORDERED_LIST
    elif block_str.startswith("- "):
        return BlockType.UNORDERED_LIST
    else:
        return BlockType.PARAGRAPH

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,tn2):
        if self.text == tn2.text and self.text_type == tn2.text_type and self.url == tn2.url:
            return True
        return False

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'