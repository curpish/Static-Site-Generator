from textnode import TextNode, TextType
from blocktype import BlockType, block_to_block_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_child = []
    for block in blocks:
       block_type = block_to_block_type(block)
       html_node_child.append(block_with_type_to_html_node(block, block_type))


    return html_node    

def block_with_type_to_html_node(block, block_type):
    
    if block_type == BlockType.PARAGRAPH:





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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.NORMAL_TEXT and delimiter and delimiter in node.text:
            current_node = node.text.split(delimiter)
            if len(current_node) > 1 and len(current_node) % 2 == 0:
                raise Exception(f'Unmatched markdown delimiter in text node: {node.text}')
            for idx, part in enumerate(current_node):
                if idx % 2 == 0:
                    # Even index: plain text
                    node_type = TextType.NORMAL_TEXT
                else:
                    # Odd index: delimited text
                    node_type = text_type
                new_nodes.append(TextNode(part, node_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    #takes raw markdown text and returns a list of tuples. 
    #Each tuple should contain the alt text and the URL of any markdown images. 
    import re
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    images = []
    for match in matches:
        alt_text = match[0]
        src_url = match[1]
        images.append((alt_text, src_url))
    return images

def extract_markdown_links(text):
    #extracts markdown links instead of images. 
    #It should return tuples of anchor text and URLs.
    import re
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    links = []
    for match in matches:
        anchor_text = match[0]
        src_url = match[1]
        links.append((anchor_text, src_url))
    return links


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text=node.text
        images = extract_markdown_images(text)
        while images:
            image_alt, image_link = images[0]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_link))
            if len(sections) > 1:
                text = sections[1]
                images = extract_markdown_images(text)
            else:
                break
        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL_TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text=node.text
        link = extract_markdown_links(text)
        while link:
            link_anchor, link_url = link[0]
            sections = text.split(f"[{link_anchor}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link_anchor, TextType.LINKS, link_url))
            if len(sections) > 1:
                text = sections[1]
                link = extract_markdown_links(text)
            else:
                break
        if text != "":
            new_nodes.append(TextNode(text, TextType.NORMAL_TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL_TEXT)]
    
    # First handle image and link markdown (more complex patterns)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # Then handle the simpler delimiter-based formatting
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)
    
    return nodes

def markdown_to_blocks(markdown):
    # First strip the entire markdown string
    markdown = markdown.strip()
    
    blocks = []
    # Split by double newlines
    for block in markdown.split('\n\n'):
        # Skip empty blocks
        if block.strip() == '':
            continue
            
        # Process lines within the block
        lines = block.split('\n')
        cleaned_lines = []
        for line in lines:
            cleaned_lines.append(line.strip())
        
        # Join the cleaned lines and add to blocks
        blocks.append('\n'.join(cleaned_lines))
    
    return blocks            

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