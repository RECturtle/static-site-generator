import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if re.match(r"[#]{1,6} ", block):
        return BlockType.HEADING
    if re.match(r"```.*```", block, re.DOTALL):
        return BlockType.CODE

    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    ordered = True
    for i in range(1, len(lines) + 1):
        if not lines[i - 1].startswith(f"{i}. "):
            ordered = False
    if ordered:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    return [
        block.strip() for block in markdown.strip().split("\n\n") if block.strip() != ""
    ]
