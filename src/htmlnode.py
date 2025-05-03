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