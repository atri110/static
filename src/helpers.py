from enum import Enum
from typing import List

import textnode
from leafnode import LeafNode
from parentnode import ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        splitted = block.split("\n")
        if len(splitted) > 1:
            inner_block = "\n".join(list(map(lambda x: x.strip(), splitted)))
            filtered_blocks.append(inner_block)
        else:
            filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    lines = block.split("\n")
    if (
        len(lines) > 1
        and lines[0].startswith("```")
        and lines[-1].endswith("```")
    ):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = get_parent_node_block(block_type, block)
        children.append(node)
    return ParentNode("div", children, None)


def get_parent_node_block(block_type: BlockType, block: str) -> ParentNode:
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html(block)
        case BlockType.HEADING:
            return heading_to_html(block)
        case BlockType.OLIST:
            return ordered_list_to_html(block)
        case BlockType.ULIST:
            return unordered_list_to_html(block)
        case BlockType.CODE:
            return code_to_html(block)
        case BlockType.QUOTE:
            return quote_to_html(block)
        case _:
            raise ValueError("wrong blocktype in switch_block_to_text fn")


def text_to_children(paragraph: str) -> List[LeafNode]:
    nodes = textnode.text_to_textnodes(paragraph)
    output = []
    for node in nodes:
        to_add = textnode.text_node_to_html_node(node)
        output.append(to_add)
    return output


def paragraph_to_html(sentence: str) -> ParentNode:
    lines = sentence.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html(sentence: str) -> ParentNode:
    level = 0
    for letter in sentence:
        if letter == "#":
            level += 1
        else:
            break
    if level >= len(sentence):
        raise ValueError(f"invalid heading lever {level}")
    text = sentence[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def ordered_list_to_html(sentence: str) -> ParentNode:
    lines = sentence.split("\n")
    html = []
    for item in lines:
        text = item[3:]
        nodes = text_to_children(text)
        childs = ParentNode("li", nodes)
        html.append(childs)
    return ParentNode("ol", html)


def unordered_list_to_html(sentence: str) -> ParentNode:
    lines = sentence.split("\n")
    html = []
    for item in lines:
        text = item[2:]
        nodes = text_to_children(text)
        child = ParentNode("li", nodes)
        html.append(child)
    return ParentNode("ul", html)


def code_to_html(sentence: str) -> ParentNode:
    if not sentence.startswith("```") and not sentence.endswith("```"):
        raise ValueError("invalid block code")
    text = sentence[4:-3]
    raw_text = textnode.TextNode(text, textnode.TextType.TEXT)
    child = textnode.text_node_to_html_node(raw_text)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html(sentence: str) -> ParentNode:
    lines = sentence.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
