from __future__ import annotations

class HTMLNode:
    def __init__(self,
                 tag: str = None,
                 value: str = None,
                 children: list[HTMLNode] = None,
                 props: dict[str, str] = None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self) -> str:
        raise NotImplementedError()


    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0:
            return ""

        prop_strings = list(map(lambda prop_key: f"{prop_key}=\"{self.props[prop_key]}\"", self.props))
        return " " + " ".join(prop_strings)


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)


    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)


    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")

        if self.children is None:
            raise ValueError("ParentNode must have children")

        children_html = list(map(lambda child: child.to_html(), self.children))
        return f"<{self.tag}{self.props_to_html()}>{"".join(children_html)}</{self.tag}>"