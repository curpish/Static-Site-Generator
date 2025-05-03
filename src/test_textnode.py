import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    def test_different_text(self):
        node = TextNode("Text one", TextType.BOLD_TEXT)
        node2 = TextNode("Text two", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)
    def test_url_none(self):
        node = TextNode("Some text", TextType.BOLD_TEXT, url=None)
        node2 = TextNode("Some text", TextType.BOLD_TEXT, url=None)
        self.assertEqual(node, node2)
    def test_different_url(self):
        node = TextNode("Same text", TextType.BOLD_TEXT, url="https://example.com")
        node2 = TextNode("Same text", TextType.BOLD_TEXT, url="https://different.com")
        self.assertNotEqual(node, node2)
    def test_different_type(self):
        node = TextNode("Text one", TextType.BOLD_TEXT)
        node2 = TextNode("Text one", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)



if __name__ == "__main__":
    unittest.main()

