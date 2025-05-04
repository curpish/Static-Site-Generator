from textnode import TextNode, TextType

def text_node_to_html_node(text_node):
    if not isinstance(text_node, TextNode):
        raise ValueError(f"Expected TextNode, got {type(text_node)}")
    
    if text_node.text_type == TextType.NORMAL_TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINKS:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported text node type: {text_node.text_type}")    

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = ""
        for key, value in self.props.items():
            props_str += f' {key}="{value}"'
        return props_str

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag}, "
            f"value={self.value}, "
            f"children={self.children}, "
            f"props={self.props}, )"
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        # Call the parent's __init__, with empty children list
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        # You already check for value in the constructor, but you could add another check here
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        # If there's no tag, return the raw value
        if self.tag is None:
            return self.value
        
        # Otherwise, render a proper HTML tag with properties
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        # Render the parent node as an HTML element with properties and children
        if self.children is None or not isinstance(self.children, list):
            raise ValueError("ParentNode must have children")
        if len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child")
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if any(not isinstance(child, HTMLNode) for child in self.children):
            raise ValueError("All children must be HTMLNode instances")

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{''.join(child.to_html() for child in self.children)}</{self.tag}>"