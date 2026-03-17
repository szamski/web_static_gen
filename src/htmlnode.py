from textnode import TextType, TextNode


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):

        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):

        raise NotImplementedError
    
    def props_to_html(self):

        if self.props is None:
            return ""

        new_props = ""
        for key, value in self.props.items():
            new_props += f' {key}="{value}"'
        return new_props

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):

        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f"{self.value}"
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        
        if self.tag is None:
            raise ValueError
        if self.children is None:
            raise ValueError("Children is empty")
        
        children_html = ""

        for child in self.children:
            children_html += child.to_html() 

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

# class TextType(Enum):
#     PLAIN = "plain"
#     BOLD = "bol"
#     ITALIC = "italic"
#     CODE = "code"
#     LINK = "link"
#     IMAGE = "image"


def text_node_to_html_node(text_node):
    
    if text_node.text_type is TextType.PLAIN:
        return LeafNode(None, text_node.text)
    if text_node.text_type is TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type is TextType.ITALIC:
        return LeafNode("i", text_node.text)   
    if text_node.text_type is TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type is TextType.LINK:
        return LeafNode("a", text_node.text, text_node.url)     
    if text_node.text_type is TextType.IMAGE:
        return LeafNode("img" "", {"src": text_node.url, "alt": text_node.text})
    
    raise Exception("Unknown text type")