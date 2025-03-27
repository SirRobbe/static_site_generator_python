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