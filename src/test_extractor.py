import unittest

from textnode import extract_markdown_images, extract_markdown_links


class TestExtractor(unittest.TestCase):
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_nothing(self):
        matches = extract_markdown_images(
            "This is text with an ![image(https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_symbols_in_alt_test(self):
        matches = extract_markdown_images(
            "This is text with an ![image@image_](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image@image_", "https://i.imgur.com/zjjcJKZ.png")], matches
        )
