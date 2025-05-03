import unittest
from htmlnode import HTMLNode, LeafNode

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