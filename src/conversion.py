import re
from re import findall
from unittest import case

from htmlnode import LeafNode, HTMLNode
from src.htmlnode import ParentNode
from textnode import TextNode, TextType, BlockType


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


def extract_markdown_images(text: str) -> list[(str, str)]:
    return findall(r"!\[(.*?)]\((.*?)\)", text)


def extract_markdown_links_from_text(text: str) -> list[(str, str)]:
    return findall(r"\[(.*?)]\((.*?)\)", text)


def split_nodes_image(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for image in images:
            texts: list = text.split("!", maxsplit=1)
            new_nodes.append(TextNode(texts[0], TextType.NORMAL))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            texts = text.split(")", maxsplit=1)
            text = texts[-1]

        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in nodes:
        links = extract_markdown_links_from_text(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for link in links:
            texts: list = text.split("[", maxsplit=1)
            new_nodes.append(TextNode(texts[0], TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINK, url=link[1]))
            texts = text.split(")", maxsplit=1)
            text = texts[-1]

        if len(text) != 0:
            new_nodes.append(TextNode(text, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    start_node = TextNode(text, TextType.NORMAL)
    nodes = split_nodes_delimiter([start_node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(text: str) -> list[str]:
    potential_blocks = re.split(r"\n\s*\n", text)
    potential_blocks = list(map(lambda block: block.strip(), potential_blocks))
    blocks = list(filter(lambda block: len(block) > 0, potential_blocks))
    return blocks


def block_to_block_type(block: str) -> BlockType:

    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("> "):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        return BlockType.ORDERED_LIST
    elif block.startswith("```"):
        return BlockType.CODE
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        tag = block_type_to_html_tag(block_type)
        if block_type == BlockType.CODE:
            code = block.replace("```", "").replace("\n", "").strip()
            html_node = LeafNode("code", code)
        else:
            text_nodes = text_to_textnodes(block)
            children = [text_node_to_html_node(text_node) for text_node in text_nodes]
            html_node = ParentNode(tag, children, {})

        block_nodes.append(html_node)

    root = ParentNode("div", block_nodes, {})
    return root


def block_type_to_html_tag(block_type: BlockType) -> str:
    match block_type:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return "h1"
        case BlockType.CODE:
            return "code"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"