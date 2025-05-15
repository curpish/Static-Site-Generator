from textnode import TextNode, TextType
from blocktype import BlockType, block_to_block_type

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_node_child = []
    
    for block in blocks:
        if block.strip():  # Only process non-empty blocks
            block_type = block_to_block_type(block)
            html_node_child.append(block_with_type_to_html_node(block, block_type))
    
    # Special case for completely empty markdown
    if not html_node_child:
        # We need to create a special case for the empty div
        # Return a custom object that renders to "<div></div>"
        class EmptyDiv:
            def to_html(self):
                return "<div></div>"
        return EmptyDiv()
    
    html_node = ParentNode("div", children=html_node_child)
    return html_node

def block_with_type_to_html_node(block, block_type):
    #Based on the type of block, create a new HTMLNode with the proper data including block data
    if block_type==BlockType.CODE:
        # Resolve the entire block and create the appropriate HTMLNode
        lines = block.splitlines()
        if lines[0] == "```" and lines[-1] == "```":
            code_lines = lines[1:-1]  #takes all lines except first and last line
            code_content = "\n".join(code_lines)+"\n" #allows a full line before and after the code block
            html_node = ParentNode("pre", [ParentNode("code", [LeafNode(None, code_content)])])        
            return html_node
        else:
            # return as formatted if not triple backtick
            return ParentNode("pre", [ParentNode("code", [LeafNode(None, block)])])
         
    elif block_type == BlockType.PARAGRAPH:
        normalized_block = " ".join(block.splitlines())
        children = text_to_children(normalized_block)
        node = ParentNode("p", children=children)
        return node 
    
    elif block_type == BlockType.QUOTE:
        # Remove '>' characters and process the content
        lines = block.strip().split("\n")
        quote_content = []
        for line in lines:
            # Remove the '>' and any leading space
            if line.startswith(">"):
                line = line[1:].lstrip()
            quote_content.append(line)
        
        quote_text = " ".join(quote_content)
        children = text_to_children(quote_text)
        node = ParentNode("blockquote", children=children)
        return node
       
    elif block_type == BlockType.HEADING:
        level = get_heading_level(block)
        heading_text = block[level+1:].strip()  # skips '#' chars and space
        children = text_to_children(heading_text)
        node = ParentNode(f"h{level}", children=children)        
        return node
    
    elif block_type == BlockType.ORDERED_LIST:
        # Split by newlines to get individual items
        items = block.strip().split("\n")
        list_items = []
        
        for item in items:
            # Remove the number and period, and any leading whitespace
            # Find the first period and take everything after it
            content = item[item.find(".")+1:].strip()
            # Create li node with properly processed content
            li_children = text_to_children(content)
            list_items.append(ParentNode("li", children=li_children))
        
        node = ParentNode("ol", children=list_items)
        return node   
    
    elif block_type == BlockType.UNORDERED_LIST:
        # Split by newlines to get individual items
        items = block.strip().split("\n")
        list_items = []
        
        for item in items:
            # Remove the dash and any leading whitespace
            content = item[item.find("-")+1:].strip()
            # Create li node with properly processed content
            li_children = text_to_children(content)
            list_items.append(ParentNode("li", children=li_children))
        
        node = ParentNode("ul", children=list_items)
        return node 

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in textnodes]

def get_heading_level(line):
    count = 0
    for char in line:
        if char == "#":
            count += 1
        else:
            break
    return count




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
    for old_node in old_nodes:
        # Only process NORMAL_TEXT nodes
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
            
        text = old_node.text
        current_index = 0
        remaining_text = text
        
        # Find all image markdown in the text
        images = extract_markdown_images(text)
        
        if not images:
            new_nodes.append(old_node)
            continue
            
        for image_alt, image_url in images:
            # Find the full image markdown
            image_markdown = f"![{image_alt}]({image_url})"
            image_index = text.find(image_markdown, current_index)
            
            if image_index == -1:
                continue  # Skip if not found
                
            # Add text before the image
            if image_index > current_index:
                prefix_text = text[current_index:image_index]
                if prefix_text:
                    new_nodes.append(TextNode(prefix_text, TextType.NORMAL_TEXT))
            
            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGES, image_url))
            
            # Update current index for next iteration
            current_index = image_index + len(image_markdown)
        
        # Add any remaining text after the last image
        if current_index < len(text):
            new_nodes.append(TextNode(text[current_index:], TextType.NORMAL_TEXT))
            
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
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        
        # If there's no tag, return the raw value
        if self.tag is None:
            return self.value
        
        # Handle self-closing tags like <img>
        props_html = self.props_to_html()
        if self.tag == "img":
            return f"<{self.tag}{props_html}>"
        
        # For regular tags, include opening and closing tags
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