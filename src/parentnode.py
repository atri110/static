from typing import Dict, List, Optional

from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(
        self,
        tag: str,
        children: List[HtmlNode],
        props: [Optional[Dict[str, str]]] = None
    ):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("tag is empty")
        if self.children is None:
            raise ValueError("missing value in HtmlNode class")

        child_nodes = ""
        for item in self.children:
            child_nodes += item.to_html()
        html = f'<{self.tag}>{child_nodes.strip()}</{self.tag}>'
        return html


def check_if_children_none(arr: List[HtmlNode]) -> bool:
    for item in arr:
        if item.children is not None:
            if not check_if_children_none(item.children):
                return False
            continue
        if not item.value:
            return False
    return True
