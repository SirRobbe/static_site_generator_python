import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")


    def test_no_tag_to_html_p(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")


    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


    def test_to_html_to_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("b", "bold")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>bold</b></div>")


    def test_to_html_with_props(self):
        child_node = LeafNode("b", "important")
        parent_node = ParentNode("a", [child_node], props={"href": "https://test.com"})
        self.assertEqual(parent_node.to_html(), '<a href="https://test.com"><b>important</b></a>')


    def test_no_tag(self):
        # None type here is ok because we test for invalid input
        # noinspection PyTypeChecker
        parent_node = ParentNode(None, [])
        self.assertRaises(ValueError, parent_node.to_html)


    def test_no_children(self):
        # None type here is ok because we test for invalid input
        # noinspection PyTypeChecker
        parent_node = ParentNode("p", None)
        self.assertRaises(ValueError, parent_node.to_html)


    def test_empty_children(self):
        parent_node = ParentNode("p", [])
        self.assertEqual(parent_node.to_html(), '<p></p>')
