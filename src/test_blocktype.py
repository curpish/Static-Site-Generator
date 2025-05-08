import unittest

from blocktype import BlockType, block_to_block_type

class TestBlocktype(unittest.TestCase):
    def test_blocktype_paragraph(self):
        text = "This is a paragraph."
        expected_type = BlockType.PARAGRAPH
        actual_type = block_to_block_type(text)
        self.assertEqual(actual_type, expected_type, f"Expected {expected_type}, but got {actual_type}.")
    def test_blocktype_heading(self):
        text = "# Heading"
        expected_type = BlockType.HEADING
        actual_type = block_to_block_type(text)
        self.assertEqual(actual_type, expected_type, f"Expected {expected_type}, but got {actual_type}.")
    def test_blocktype_code(self):
        text = "```\nthis is code\n```"
        expected_type = BlockType.CODE
        actual_type = block_to_block_type(text)
        self.assertEqual(actual_type, expected_type, f"Expected {expected_type}, but got {actual_type}.")
    def test_blocktype_quote(self):
        text = "> This is a quote."
        expected_type = BlockType.QUOTE
        actual_type = block_to_block_type(text)
        self.assertEqual(actual_type, expected_type, f"Expected {expected_type}, but got {actual_type}.")
    def test_blocktype_unordered_list(self):
        text = "- Item 1\n- Item 2"
        expected_type = BlockType.UNORDERED_LIST
        actual_type = block_to_block_type(text)
        self.assertEqual(actual_type, expected_type, f"Expected {expected_type}, but got {actual_type}.")
    def test_blocktype_ordered_list(self):
        text = "1. Item 1\n2. Item 2"
        expected_type = BlockType.ORDERED_LIST
        actual_type = block_to_block_type(text)
        self.assertEqual(actual_type, expected_type, f"Expected {expected_type}, but got {actual_type}.")
    def test_blocktype_empty(self):
        text = ""
        expected_type = BlockType.PARAGRAPH
        actual_type = block_to_block_type(text)
        self.assertEqual(actual_type, expected_type, f"Expected {expected_type}, but got {actual_type}.")

if __name__ == '__main__':
    unittest.main()