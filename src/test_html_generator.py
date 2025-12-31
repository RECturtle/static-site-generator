import unittest
from html_generator import markdown_to_html_node


class TestHTMLGenerator(unittest.TestCase):
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

    def test_headings(self):
        md = """
    # Heading one

    This is **bolded** paragraph
    text in a p
    tag here

    ## Heading Two

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading one</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><h2>Heading Two</h2><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_quote(self):
        md = """> This is a quote
> with **bold** text
> across multiple lines"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text across multiple lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """- First item
- Second **bold** item
- Third item"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second <b>bold</b> item</li><li>Third item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """1. First item
2. Second _italic_ item
3. Third item"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second <i>italic</i> item</li><li>Third item</li></ol></div>",
        )
