import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
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