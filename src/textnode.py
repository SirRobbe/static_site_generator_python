import enum
from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, type: TextType, url: str = None):
        self.text = text
        self.type = type
        self.url = url


    def __eq__(self, other):
        return self.text == other.text and self.type == other.type and self.url == other.url


    def __repr__(self):
        return f"TextNode({self.text}, {self.type.value}, {self.url})"


class BlockType(Enum):
    PARAGRAPH = "paragraph",
    HEADING = "heading",
    CODE = "code",
    QUOTE = "quote",
    UNORDERED_LIST = "unordered_list",
    ORDERED_LIST = "ordered_list",
