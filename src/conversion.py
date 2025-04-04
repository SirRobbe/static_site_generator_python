from htmlnode import LeafNode, HTMLNode
from textnode import TextNode, TextType


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


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    new_nodes = []

    for node in old_nodes:
        node_parts = node.text.split(delimiter)
        for i in range(0, len(node_parts)):
            if i == 0 or i == (len(node_parts) - 1):
                new_nodes.append(TextNode(node_parts[i], node.type))
            else:
                new_nodes.append(TextNode(node_parts[i], text_type))

    return new_nodes