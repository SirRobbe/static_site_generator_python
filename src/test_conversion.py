import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from conversion import text_node_to_html_node

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


# class TextType(Enum):
#     NORMAL = "normal"
#     BOLD = "bold"
#     ITALIC = "italic"
#     CODE = "code"
#     LINK = "link"
#     IMAGE = "image"
