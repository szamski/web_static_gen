import re
from textnode import TextNode, TextType
from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import text_node_to_html_node


class BlokType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def extract_markdown_img(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_url(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue
        if node.text_type is TextType.PLAIN:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0:
                raise Exception
            for i, part in enumerate(parts):
                if part == "":
                    continue
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.PLAIN))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue
        if node.text_type is TextType.PLAIN:
            parts = extract_markdown_img(node.text)
            if not parts:
                new_nodes.append(node)
                continue
            remaining = node.text
            for alt, url in parts:
                sections = remaining.split(f"![{alt}]({url})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.PLAIN))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                remaining = sections[1]
            if remaining:
                new_nodes.append(TextNode(remaining, TextType.PLAIN))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
            continue
        if node.text_type is TextType.PLAIN:
            parts = extract_markdown_url(node.text)
            if not parts:
                new_nodes.append(node)
                continue
            remaining = node.text
            for alt, url in parts:
                sections = remaining.split(f"[{alt}]({url})", 1)
                if sections[0]:
                    new_nodes.append(TextNode(sections[0], TextType.PLAIN))
                new_nodes.append(TextNode(alt, TextType.LINK, url))
                remaining = sections[1]
            if remaining:
                new_nodes.append(TextNode(remaining, TextType.PLAIN))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):

    new_md = markdown.strip().split("\n\n")

    return new_md


def block_to_block_type(markdown):
    if re.match(r"^#{1,6} ", markdown):
        return BlokType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlokType.CODE
    if markdown.startswith(">"):
        lines = markdown.split("\n")
        if all(line.startswith(">") for line in lines):
            return BlokType.QUOTE
    if markdown.startswith("- "):
        lines = markdown.split("\n")
        if all(line.startswith("- ") for line in lines):
            return BlokType.UNORDERED_LIST
    if re.match(r"[1-9].", markdown):
        lines = markdown.split("\n")
        if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
            return BlokType.ORDERED_LIST

    return BlokType.PARAGRAPH


def markdown_to_html_node(markdown):

    blocks = markdown_to_blocks(markdown)

    html_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlokType.HEADING:
            a = block.split(" ", 1)
            level = len(a[0])
            text = a[1]
            html_nodes.append(ParentNode(f"h{level}", text_to_children(text)))

        if block_type == BlokType.CODE:
            text = block.strip("```").strip("\n")
            text_node = TextNode(text, TextType.CODE)
            html_nodes.append(ParentNode("pre", [text_node_to_html_node(text_node)]))

        if block_type == BlokType.QUOTE:
            lines = block.split("\n", -1)
            stripped = [line.lstrip("> ") for line in lines]
            text = "\n".join(stripped)
            html_nodes.append(ParentNode("blockquote", text_to_children(text)))

        if block_type == BlokType.UNORDERED_LIST:
            lines = block.split("\n", -1)
            li_nodes = []
            for line in lines:
                text = line.lstrip("- ")
                li_nodes.append(ParentNode("li", text_to_children(text)))
            html_nodes.append(ParentNode("ul", li_nodes))

        if block_type == BlokType.ORDERED_LIST:
            lines = block.split("\n", -1)
            li_nodes = []
            for i, line in enumerate(lines):
                text = line.lstrip(f"{i + 1}. ")
                li_nodes.append(ParentNode("li", text_to_children(text)))
            html_nodes.append(ParentNode("ol", li_nodes))

        if block_type == BlokType.PARAGRAPH:
            html_nodes.append(ParentNode("p", text_to_children(block)))

    return ParentNode("div", html_nodes)


def extract_title(markdown):
    lines = markdown.split("\n", -1)

    for line in lines:
        if line.startswith("# "):
            stripped = line.split(" ", 1)
            return stripped[1].strip(" ")
    raise Exception


def text_to_children(text):

    child_text = text_to_textnodes(text)

    children = []

    for child in child_text:
        node = text_node_to_html_node(child)
        children.append(node)
    return children
