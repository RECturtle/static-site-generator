import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type


class TestBlocktoBlockType(unittest.TestCase):
    def test_paragraph(self):
        test = "this is clearly a paragraph\n- totally\n* not a list."
        self.assertEqual(block_to_block_type(test), BlockType.PARAGRAPH)

    def test_heading_one(self):
        tests = ["# ", "## word", "### word", "#### ", "##### ", "###### "]
        for test in tests:
            self.assertEqual(block_to_block_type(test), BlockType.HEADING)


    def test_malformed_heading(self):
        tests = ["#", "##word", "###word", "####", "#####", "######"]
        for test in tests:
            self.assertEqual(block_to_block_type(test), BlockType.PARAGRAPH)

    def test_code(self):
        tests = ["```this is cool code```", "```\nmycode is cool\nmorecode```"]
        for test in tests:
            self.assertEqual(block_to_block_type(test), BlockType.CODE)       

    def test_quote(self):
        test = ">hi\n>hi\n> good bye\n> hi"
        self.assertEqual(block_to_block_type(test), BlockType.QUOTE)

    def test_unordered_list(self):
        test = "- hi\n- hi\n- good bye\n- hi"
        self.assertEqual(block_to_block_type(test), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        test = "1. hi\n2. hi\n3. good bye\n4. hi"
        self.assertEqual(block_to_block_type(test), BlockType.ORDERED_LIST)


class TestMarkdownSplitter(unittest.TestCase):
    def test_markdown_to_blocks_base(self):
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

    def test_markdown_to_blocks_empty(self):
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

    # Edge cases
    def test_empty_string(self):
        """What happens with no input?"""
        self.assertEqual(markdown_to_blocks(""), [])

    def test_single_block(self):
        """What if there's only one block, no splitting needed?"""
        self.assertEqual(markdown_to_blocks("Just one paragraph"), ["Just one paragraph"])

    def test_only_whitespace(self):
        """Input that looks empty but isn't"""
        self.assertEqual(markdown_to_blocks("   \n\n   \n"), [])

    # Whitespace handling
    def test_multiple_blank_lines(self):
        """Do 3+ blank lines between blocks still produce 2 blocks?"""
        md = "Block one\n\n\n\nBlock two"
        self.assertEqual(markdown_to_blocks(md), ["Block one", "Block two"])

    def test_leading_trailing_whitespace_in_blocks(self):
        """Are blocks trimmed of extra spaces?"""
        md = "  padded block  \n\n  another padded  "
        self.assertEqual(markdown_to_blocks(md), ["padded block", "another padded"])

    # Different block types
    def test_code_block(self):
        """Code blocks with internal blank lines"""
        md = "```\ncode\nmore code\n```\n\nParagraph"
        self.assertEqual(markdown_to_blocks(md), ["```\ncode\nmore code\n```", "Paragraph"])

    def test_headers(self):
        """Headers as separate blocks"""
        md = "# Header\n\nParagraph"
        self.assertEqual(markdown_to_blocks(md), ["# Header", "Paragraph"])
