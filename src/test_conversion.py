import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from conversion import *

class TestConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node: HTMLNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node: HTMLNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")


    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node: HTMLNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")


    def test_text_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node: HTMLNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")


    def test_text_link(self):
        node = TextNode("This is a text node", TextType.LINK,url="https://example.com")
        html_node: HTMLNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props_to_html(), ' href="https://example.com"')


    def test_text_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, url="https://example.com")
        html_node: HTMLNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props_to_html(), ' src="https://example.com" alt="This is a text node"')

    def test_empty(self):
        # node is valid as a parameter in that case to check the correct error handling
        # noinspection PyTypeChecker
        node = TextNode("This has no valid type", None)
        self.assertRaises(Exception, text_node_to_html_node, node)


    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.NORMAL))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.NORMAL))

        node = TextNode("This is text with a **bold** word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.NORMAL))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.NORMAL))

        node = TextNode("This is text with a _italic_ word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.NORMAL))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.NORMAL))

        node1 = TextNode("This is a text with a **bold** word", TextType.NORMAL)
        node2 = TextNode("This is a text with a _italic_ word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("This is a text with a ", TextType.NORMAL))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.NORMAL))
        self.assertEqual(new_nodes[3], TextNode("This is a text with a ", TextType.NORMAL))
        self.assertEqual(new_nodes[4], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[5], TextNode(" word", TextType.NORMAL))


    def test_split_nodes_special_type_in_type(self):
        node = TextNode("This is bold text including an _italic phrase_ word", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("This is bold text including an ", TextType.BOLD))
        self.assertEqual(new_nodes[1], TextNode("italic phrase", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.BOLD))


    def test_split_nodes_empty(self):
        new_nodes = split_nodes_delimiter([], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [])


    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(images[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

        text = "This has no image"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 0)


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links_from_text(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("to boot dev", "https://www.boot.dev"))
        self.assertEqual(links[1], ("to youtube", "https://www.youtube.com/@bootdotdev"))

        text = "This has no links"
        links = extract_markdown_links_from_text(text)
        self.assertEqual(len(links), 0)
