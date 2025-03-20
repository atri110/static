from typing import Dict, Optional

from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(
        self,
        tag: Optional[str] = None,
        value: str = "",
        props: Optional[Dict[str, str]] = None,
    ):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        # if not self.value:
        #     raise ValueError("value is empty")
        if not self.tag:
            return self.value
        html = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        return html
