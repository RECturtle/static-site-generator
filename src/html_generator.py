import blocks
import htmlnode
import textnode


def text_to_children(text):
    """Convert text with inline markdown to a list of HTMLNodes."""
    text = " ".join(text.split())
    nodes = textnode.text_to_textnodes(text)
    return [textnode.text_node_to_html_node(n) for n in nodes]


def markdown_to_html_node(markdown):
    block_nodes = []
    md_blocks = blocks.markdown_to_blocks(markdown)
    for block in md_blocks:
        block_type = blocks.block_to_block_type(block)
        match block_type:
            case blocks.BlockType.PARAGRAPH:
                children = text_to_children(block)
                block_nodes.append(htmlnode.ParentNode("p", children))
            case blocks.BlockType.HEADING:
                split = block.split(" ", 1)
                heading_level = len(split[0])
                text = split[1] if len(split) > 1 else ""
                children = text_to_children(text)
                block_nodes.append(htmlnode.ParentNode(f"h{heading_level}", children))
            case blocks.BlockType.CODE:
                code_content = block[3:-3].strip()
                code_node = textnode.TextNode(code_content, textnode.TextType.TEXT)
                code_html = textnode.text_node_to_html_node(code_node)
                code_element = htmlnode.ParentNode("code", [code_html])
                block_nodes.append(htmlnode.ParentNode("pre", [code_element]))
            case blocks.BlockType.QUOTE:
                lines = block.split("\n")
                content = "\n".join(line[1:].strip() for line in lines)
                children = text_to_children(content)
                block_nodes.append(htmlnode.ParentNode("blockquote", children))
            case blocks.BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_items = []
                for line in lines:
                    item_text = line[2:]
                    children = text_to_children(item_text)
                    list_items.append(htmlnode.ParentNode("li", children))
                block_nodes.append(htmlnode.ParentNode("ul", list_items))
            case blocks.BlockType.ORDERED_LIST:
                lines = block.split("\n")
                list_items = []
                for line in lines:
                    item_text = line.split(". ", 1)[1]
                    children = text_to_children(item_text)
                    list_items.append(htmlnode.ParentNode("li", children))
                block_nodes.append(htmlnode.ParentNode("ol", list_items))
    parent = htmlnode.ParentNode("div", block_nodes)
    return parent
