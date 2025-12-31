import re
from enum import Enum
from htmlnode import LeafNode


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value=None,
                props={"src": text_node.url, "alt": text_node.text},
            )


def split_nodes_delimiter(old_nodes, delimeter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        tmp_nodes = []
        split_list = node.text.split(delimeter)
        if len(split_list) % 2 == 0:
            raise Exception("missing closing delimiters")
        for i in range(len(split_list)):
            if split_list[i] == "":
                continue
            if i % 2 == 0:
                tmp_nodes.append(TextNode(split_list[i], TextType.TEXT))
            else:
                tmp_nodes.append(TextNode(split_list[i], text_type))
        new_nodes.extend(tmp_nodes)
    return new_nodes


def check_matches(matches, tmp_string, type):
    tmp_nodes = []
    for match in matches:
        if type == TextType.LINK:
            split_string = f"[{match[0]}]({match[1]})"
        elif type == TextType.IMAGE:
            split_string = f"![{match[0]}]({match[1]})"
        tmp_string_parts = tmp_string.split(split_string, 1)
        tmp_string = tmp_string_parts[1]
        tmp_nodes.append(TextNode(tmp_string_parts[0], TextType.TEXT))
        tmp_nodes.append(TextNode(match[0], type, match[1]))
    if tmp_string:
        tmp_nodes.append(TextNode(tmp_string, TextType.TEXT))
    return tmp_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        matched_nodes = check_matches(matches, node.text, TextType.IMAGE)
        new_nodes.extend(matched_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        matched_nodes = check_matches(matches, node.text, TextType.LINK)
        new_nodes.extend(matched_nodes)
    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
