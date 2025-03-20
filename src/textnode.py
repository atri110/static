from enum import Enum
from typing import Callable, List, Tuple

from leafnode import LeafNode
from regexhelper import extract_markdown_images, extract_markdown_links


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "Italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: "TextNode"):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode(
                "img",
                "",
                {"alt": text_node.text, "src": text_node.url}
            )
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")


def split_nodes_delimeter(
        old_nodes: List[TextNode],
        delimeter: str,
        text_type: TextType
) -> List[TextNode]:
    # if not old_nodes:
    #     raise ValueError("old_nodes is empty")
    output = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimeter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for key in range(len(sections)):
            if sections[key] == "":
                continue
            if key % 2 == 0:
                split_nodes.append(TextNode(sections[key], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[key], text_type))
        output.extend(split_nodes)
    return output


def split_nodes_helper(
        nodes: List[TextNode],
        fn: Callable[[str], List[Tuple[str, str]]],
        text_type: TextType
) -> List[TextNode]:
    output = []
    for node in nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue

        original_text = node.text
        to_extract = fn(original_text)
        if not to_extract:
            output.append(node)
            continue

        for val, url in to_extract:
            pattern = f"[{val}]({url})"
            if text_type == TextType.IMAGE:
                pattern = "!" + pattern

            sections = original_text.split(pattern, 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if sections[0] != "":
                output.append(TextNode(sections[0], TextType.TEXT))

            output.append(
                TextNode(
                    val,
                    text_type,
                    url
                )
            )
            original_text = sections[1]
        if original_text != "":
            output.append(TextNode(original_text, TextType.TEXT))
    return output


def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimeter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimeter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimeter(nodes, "`", TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes


def split_nodes_link(nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_helper(nodes, extract_markdown_links, TextType.LINK)


def split_nodes_image(nodes: List[TextNode]) -> List[TextNode]:
    return split_nodes_helper(nodes, extract_markdown_images, TextType.IMAGE)
