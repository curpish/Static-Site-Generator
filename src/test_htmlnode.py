import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks
from textnode import TextNode, TextType
from enum import Enum

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        # Test with no properties
        node = HTMLNode("p", "Hello, world!", None, None)
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html_one_prop(self):
        # Test with one property
        node = HTMLNode("a", "Click me!", None, {"href": "https://www.example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.example.com"')
        
    def test_props_to_html_multiple_props(self):
        # Test with multiple properties
        node = HTMLNode(
            "a", 
            "Click me!", 
            None, 
            {
                "href": "https://www.example.com",
                "target": "_blank"
            }
        )
        # Note that we can't guarantee order in dictionaries
        # so we need to check if both properties are present
        html = node.props_to_html()
        self.assertIn(' href="https://www.example.com"', html)
        self.assertIn(' target="_blank"', html)
        self.assertEqual(len(html.split()), 2)  # Should have 2 attributes

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        node = LeafNode("b", "Hello, world!")
        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

        node = LeafNode("i", "Hello, world!")
        self.assertEqual(node.to_html(), "<i>Hello, world!</i>")

        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

        node = LeafNode("a", "Click here", {"href": "https://boot.dev"})        
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Click here</a>')

    def test_to_html_with_children_1(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children_2(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child</b></div>",
        )
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_attributes(self):
        node = LeafNode("a", "Click here", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Click here</a>')

    def test_to_html_with_multiple_attributes(self):
        node = LeafNode("a", "Click here", {"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://boot.dev" target="_blank">Click here</a>',
        )
    
    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("a", "child 1")
        child_node2 = LeafNode("b", "child 2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><a>child 1</a><b>child 2</b></div>",
        )
    
    def test_to_html_parent_with_attributes(self):
        child_node1 = LeafNode("span", "text 1")
        child_node2 = LeafNode("b", "text 2")
        parent_node = ParentNode("div", [child_node1, child_node2], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><span>text 1</span><b>text 2</b></div>',
        )        
    def test_error_when_parent_node_tag_is_none(self):
        with self.assertRaises(ValueError) as context:
            parent_node = ParentNode(None, [LeafNode("span", "text")])
            parent_node.to_html()
        self.assertTrue("tag" in str(context.exception).lower())  # Check if error message mentions "tag"

    def test_error_when_parent_node_children_is_none(self):
        with self.assertRaises(ValueError) as context:
            parent_node = ParentNode("div", None)
            parent_node.to_html()
        self.assertTrue("children" in str(context.exception).lower())  # Check if error message mentions "children"    

    def test_leaf_as_child(self):
        child_node = LeafNode("a", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><a>child</a></div>",
        )
    
    def test_parent_as_child(self):
        grandchild1 = LeafNode("a", "text 1")
        grandchild2 = LeafNode("b", "text 2")
        child_node = ParentNode("span", [grandchild1, grandchild2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><a>text 1</a><b>text 2</b></span></div>",
        )
    
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD_TEXT)  # Just the text, not the markdown
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, 'Bold text')  # Just the text content

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC_TEXT)  # Just the text, not the markdown
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, 'Italic text')  # Just the text content

    def test_code(self):
        node = TextNode("Code text", TextType.CODE_TEXT)  # Just the text, not the markdown
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, 'Code text')  # Just the text content

    def test_links(self):
        node = TextNode("anchor text", TextType.LINKS, "http://example.com")  # Assuming TextType.LINK is correct and URL is passed as metadata
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, 'anchor text')  # Just the text content
        self.assertEqual(html_node.props['href'], 'http://example.com') # Check the href property
    
    def test_images(self):
        # Create a TextNode with text="alt text", type=TextType.IMAGES, and url="https://example.com/image.jpg"
        node = TextNode("alt text", TextType.IMAGES, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')  # Value should be empty for images
        self.assertEqual(html_node.props['src'], 'https://example.com/image.jpg')
        self.assertEqual(html_node.props['alt'], 'alt text')

    def test_split_nodes_delimiter_none(self):
        old_nodes = [
            TextNode("plain text", TextType.NORMAL_TEXT),
            TextNode("delimited text", TextType.IMAGES)
        ]
        delimiter = None
        text_type = TextType.NORMAL_TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, 'plain text')
        self.assertEqual(new_nodes[1].text, 'delimited text')

    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [
            TextNode("plain text", TextType.NORMAL_TEXT),
            TextNode("plain text", TextType.NORMAL_TEXT)
        ]
        text_type = TextType.NORMAL_TEXT
        delimiter = ''
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, 'plain text')
        self.assertEqual(new_nodes[1].text, 'plain text')
    
    def test_split_nodes_delimiter_unmatched_delimiter(self):
        old_nodes = [
            TextNode("plain text", TextType.NORMAL_TEXT),
            TextNode("`delimited text", TextType.NORMAL_TEXT)
        ]
        delimiter = "`"
        # test that the exception is raised!
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, delimiter, TextType.CODE_TEXT)
    
    def test_split_nodes_multiple_node_types(self):
        old_nodes = [
            TextNode("some `code` here", TextType.NORMAL_TEXT),
            TextNode("just plain", TextType.NORMAL_TEXT),
            TextNode("already code", TextType.CODE_TEXT)
        ]
        delimiter = "`"
        text_type = TextType.CODE_TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, 'some ')
        self.assertEqual(new_nodes[1].text, 'code')
        self.assertEqual(new_nodes[2].text, ' here')
        self.assertEqual(new_nodes[3].text, 'just plain')
        self.assertEqual(new_nodes[4].text, 'already code')
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL_TEXT)
        self.assertEqual(new_nodes[1].text_type, TextType.CODE_TEXT)
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL_TEXT)
        self.assertEqual(new_nodes[3].text_type, TextType.NORMAL_TEXT)
        self.assertEqual(new_nodes[4].text_type, TextType.CODE_TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.example.com)"
        )
        self.assertListEqual([("link", "https://www.example.com")], matches)
    
    def test_extract_markdown_many_images_and_links(self):
        #tests both functions separately
        markdown_text = """
        This is some text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.example.com).
        Another line with another image ![image2](https://i.imgur.com/abcdeFGH.png) and link [another link](https://example.org).
        """
        matches = extract_markdown_images(markdown_text)
        self.assertEqual(len(matches), 2)
        matches = extract_markdown_links(markdown_text)
        self.assertEqual(len(matches), 2)
    
    def test_extract_markdown_images_and_links_with_empty_alt_text_or_urls(self):
        # Handle edge cases like empty alt text or URLs
        markdown_text = """
        This is some text with an ![](https://i.imgur.com/empty-alt.png) and a [](https://www.empty-anchor.com).
        Another line with another image ![image2]() and link [another link]().
        """
        
        image_matches = extract_markdown_images(markdown_text)
        self.assertEqual(len(image_matches), 2)
        self.assertEqual(image_matches[0][0], "")  # Empty alt text
        self.assertEqual(image_matches[1][1], "")  # Empty URL
        
        link_matches = extract_markdown_links(markdown_text)
        self.assertEqual(len(link_matches), 2)
        self.assertEqual(link_matches[0][0], "")  # Empty anchor text
        self.assertEqual(link_matches[1][1], "")  # Empty URL

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL_TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [another link](https://example.org)",
            TextType.NORMAL_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL_TEXT),
                TextNode("link", TextType.LINKS, "https://example.com"),
                TextNode(" and another ", TextType.NORMAL_TEXT),
                TextNode("another link", TextType.LINKS, "https://example.org"),
            ],
            new_nodes,
        )

    def test_split_multiple_links_side_by_side(self):
        node = TextNode(
            "These are multiple links side by side: [link1](https://example.com/link1)[link2](https://example.com/link2)",
            TextType.NORMAL_TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("These are multiple links side by side: ", TextType.NORMAL_TEXT),
                TextNode("link1", TextType.LINKS, "https://example.com/link1"),   
                TextNode("link2", TextType.LINKS, "https://example.com/link2"),
            ],
            new_nodes,
        )
        

    def test_text_to_textnodes(self):
        # Test a complex markdown string with multiple elements
        markdown = "This is **text** with an _italic_ word and a `code block` and an ![image](https://example.com/image.jpg) and a [link](https://example.com)"
        
        nodes = text_to_textnodes(markdown)
        
        # Check that we got the expected number of nodes
        self.assertEqual(10, len(nodes))
        
        # Check each node has the correct type and content
        self.assertEqual(TextType.NORMAL_TEXT, nodes[0].text_type)
        self.assertEqual("This is ", nodes[0].text)
        
        self.assertEqual(TextType.BOLD_TEXT, nodes[1].text_type)
        self.assertEqual("text", nodes[1].text)
        
        self.assertEqual(TextType.NORMAL_TEXT, nodes[2].text_type)
        self.assertEqual(" with an ", nodes[2].text)
        
        self.assertEqual(TextType.ITALIC_TEXT, nodes[3].text_type)
        self.assertEqual("italic", nodes[3].text)
        
        self.assertEqual(TextType.NORMAL_TEXT, nodes[4].text_type)
        self.assertEqual(" word and a ", nodes[4].text)
        
        self.assertEqual(TextType.CODE_TEXT, nodes[5].text_type)
        self.assertEqual("code block", nodes[5].text)
        
        self.assertEqual(TextType.NORMAL_TEXT, nodes[6].text_type)
        self.assertEqual(" and an ", nodes[6].text)

    def test_text_to_textnodes(self):
        # Test a complex markdown string with multiple elements
        markdown = "This is **text** with an _italic_ word and a `code block` and an ![image](https://example.com/image.jpg) and a [link](https://example.com)"
        
        nodes = text_to_textnodes(markdown)
        
        # Check that we got the expected number of nodes
        self.assertEqual(10, len(nodes))
        
        # Check each node has the correct type and content
        self.assertEqual(TextType.NORMAL_TEXT, nodes[0].text_type)
        self.assertEqual("This is ", nodes[0].text)
        
        self.assertEqual(TextType.BOLD_TEXT, nodes[1].text_type)
        self.assertEqual("text", nodes[1].text)
        
        self.assertEqual(TextType.NORMAL_TEXT, nodes[2].text_type)
        self.assertEqual(" with an ", nodes[2].text)
        
        self.assertEqual(TextType.ITALIC_TEXT, nodes[3].text_type)
        self.assertEqual("italic", nodes[3].text)
        
        self.assertEqual(TextType.NORMAL_TEXT, nodes[4].text_type)
        self.assertEqual(" word and a ", nodes[4].text)
        
        self.assertEqual(TextType.CODE_TEXT, nodes[5].text_type)
        self.assertEqual("code block", nodes[5].text)
        
        self.assertEqual(TextType.NORMAL_TEXT, nodes[6].text_type)
        self.assertEqual(" and an ", nodes[6].text)
    
    def test_nested_formatting(self):
        # This tests how your parser handles nested formatting
        markdown = "This has **bold with _italic_ inside**"
        nodes = text_to_textnodes(markdown)
        # Check the expected behavior based on your implementation
        # One possible outcome:
        self.assertEqual(3, len(nodes))
        self.assertEqual("This has ", nodes[0].text)
        self.assertEqual(TextType.BOLD_TEXT, nodes[1].text_type)
        self.assertEqual("bold with _italic_ inside", nodes[1].text)

    def test_markdown_to_blocks(self):
            md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )
            
    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_only_whitespace(self):
        md = "   \n   \n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_multiple_consecutive_newlines(self):
        md = "First block\n\n\n\nSecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["First block", "Second block"])

    def test_trailing_newlines(self):
        md = "Some content\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Some content"])

    def test_leading_newlines(self):
        md = "\n\nSome content"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Some content"])

    def test_single_line(self):
        md = "Just one line with no newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just one line with no newlines"])    