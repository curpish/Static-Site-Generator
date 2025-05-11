import unittest
from htmlnode import markdown_to_html_node, block_with_type_to_html_node
from blocktype import BlockType, block_to_block_type

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_code_block_node(self):
        block = "This is code\nwith multiple lines\n  and indentation"
        block_type = BlockType.CODE
        node = block_with_type_to_html_node(block, block_type)
        html = node.to_html()
        expected = "<pre><code>This is code\nwith multiple lines\n  and indentation</code></pre>"
        self.assertEqual(html, expected)

    def test_heading(self):
        md = "# My **Heading**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>My <b>Heading</b></h1></div>")

    def test_ordered_list(self):
        md = "1. First\n2. Second\n3. Third"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>")

    def test_unordered_list(self):
        md = "- Apple\n- Banana\n- Cherry"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul></div>")
   
    def test_blockquote(self):
        md = "> This is a blockquote\n> with multiple lines"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html, 
            "<div><blockquote>This is a blockquote with multiple lines</blockquote></div>"
        )


                                  
if __name__ == "__main__":
    unittest.main()