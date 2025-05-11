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

    def test_nested_inline_elements(self):
        md = "This is `code` inside **bold _and italic_**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <code>code</code> inside <b>bold <i>and italic</i></b></p></div>"
        )

    def test_multiple_heading_levels(self):
        md = "# Heading 1\n## Heading 2\n### Heading 3\n#### Heading 4\n##### Heading 5\n###### Heading 6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )

    def test_empty_blocks(self):
        md = "\n\n\n"  # Multiple empty lines
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")
        
        # Test with an empty paragraph between content
        md = "First paragraph\n\n\n\nSecond paragraph"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph</p><p>Second paragraph</p></div>"
        )         

    def test_formatted_list_items(self):
        md = "- Item with **bold**\n- Item with _italic_\n- Item with `code`"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item with <b>bold</b></li><li>Item with <i>italic</i></li><li>Item with <code>code</code></li></ul></div>"
        )
        
        # Test ordered list with formatting
        md = "1. First with **bold**\n2. Second with _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First with <b>bold</b></li><li>Second with <i>italic</i></li></ol></div>"
        )          
                                  
if __name__ == "__main__":
    unittest.main()