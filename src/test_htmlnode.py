import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_empty_props(self):
        node = HTMLNode(props={})
        props = node.props_to_html()
        self.assertEqual(props, "")

    def test_single_props(self):
        node = HTMLNode(props={"href": "https://test.com"})
        props = node.props_to_html()
        self.assertEqual(props, ' href="https://test.com"')

    def test_multiple_props(self):
        node = HTMLNode(props={"a": "1", "b": "2"})
        props = node.props_to_html()
        self.assertEqual(props, ' a="1" b="2"')

    def test_no_props(self):
        node = HTMLNode(tag="h1")
        props = node.props_to_html()
        self.assertEqual(props, "")