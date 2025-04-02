from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode

def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.type:
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case _:
            raise Exception(f"Unknown text type: {text_node.type}")
