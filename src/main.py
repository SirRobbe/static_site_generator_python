from textnode import *
from htmlnode import HTMLNode

print("hello world")
node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")

child = HTMLNode(tag="a", value="link", props={"href": "https://www.boot.dev"})
parent = HTMLNode(tag="h1", value="title", children=[child])

print(parent)