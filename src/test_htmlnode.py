import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "hello, world!", None, {"href": "https://boots.dev"})
        node2 = HTMLNode("p", "hello, world!", None, {"href": "https://boots.dev"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("p", "hello, world!", None, {"href": "https://boots.dev"})
        test_string = node.props_to_html()
        expected_string = ' href="https://boots.dev"'
        self.assertEqual(test_string, expected_string)

    def test_ne(self):
        node = HTMLNode("p", "hello, world!", None, {"href": "https://boots.dev"})
        node2 = HTMLNode("p", None, None, {"href": "https://boots.dev"})
        self.assertNotEqual(node, node2)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leat_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_links(self):
        child_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><a href="https://www.google.com">Click me!</a></div>',
        )

    def test_to_html_no_tag_raises(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "missing tag")

    def test_to_html_no_children_raises(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "missing children")

    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("b", "bold")
        child2 = LeafNode("i", "italic")
        child3 = LeafNode(None, "plain text")
        parent_node = ParentNode("p", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>bold</b><i>italic</i>plain text</p>",
        )

    def test_to_html_deeply_nested(self):
        inner = LeafNode("span", "deep")
        level3 = ParentNode("div", [inner])
        level2 = ParentNode("section", [level3])
        level1 = ParentNode("article", [level2])
        self.assertEqual(
            level1.to_html(),
            "<article><section><div><span>deep</span></div></section></article>",
        )

    def test_to_html_mixed_children(self):
        leaf1 = LeafNode("b", "bold")
        nested_leaf = LeafNode("i", "italic")
        parent_child = ParentNode("span", [nested_leaf])
        leaf2 = LeafNode(None, " and text")
        parent_node = ParentNode("p", [leaf1, parent_child, leaf2])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>bold</b><span><i>italic</i></span> and text</p>",
        )

    def test_to_html_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")
