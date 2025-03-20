from typing import Dict, List, Optional


class HtmlNode():
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[List["HtmlNode"]] = None,
        props: Optional[Dict[str, str]] = None
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented yet")

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        s = ""
        for key in self.props:
            s += f' {key}="{self.props[key]}"'
        return s

    def __repr__(self):
        return (
            f"HtmlNode: tag:{self.tag}, value:{self.value}, "
            f"children: {self.children}, props: {self.props}"
        )
