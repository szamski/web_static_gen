import unittest

from markdown_parser import (
    extract_markdown_img,
    extract_markdown_url,
    markdown_to_blocks,
    block_to_block_type,
    BlokType,
    markdown_to_html_node,
    extract_title,
)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_img(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_url(self):
        matches = extract_markdown_url(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_markdown_to_blocks(self):
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


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_single_hash(self):
        self.assertEqual(block_to_block_type("# Heading"), BlokType.HEADING)

    def test_heading_three_hashes(self):
        self.assertEqual(block_to_block_type("### Heading 3"), BlokType.HEADING)

    def test_heading_six_hashes(self):
        self.assertEqual(block_to_block_type("###### Heading 6"), BlokType.HEADING)

    def test_heading_no_space_is_paragraph(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlokType.PARAGRAPH)

    def test_heading_seven_hashes_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Too many"), BlokType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nprint('hello')\n```"), BlokType.CODE)

    def test_code_block_multiline(self):
        self.assertEqual(block_to_block_type("```\nline1\nline2\n```"), BlokType.CODE)

    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type("> quote"), BlokType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(
            block_to_block_type("> line 1\n> line 2\n> line 3"), BlokType.QUOTE
        )

    def test_quote_missing_on_one_line(self):
        self.assertEqual(
            block_to_block_type("> line 1\nno quote here\n> line 3"), BlokType.PARAGRAPH
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- item 1\n- item 2\n- item 3"), BlokType.UNORDERED_LIST
        )

    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- only item"), BlokType.UNORDERED_LIST)

    def test_unordered_list_missing_dash(self):
        self.assertEqual(
            block_to_block_type("- item 1\nno dash\n- item 3"), BlokType.PARAGRAPH
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"), BlokType.ORDERED_LIST
        )

    def test_ordered_list_wrong_start(self):
        self.assertEqual(block_to_block_type("2. first\n3. second"), BlokType.PARAGRAPH)

    def test_ordered_list_wrong_order(self):
        self.assertEqual(block_to_block_type("1. first\n3. second"), BlokType.PARAGRAPH)

    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a normal paragraph"), BlokType.PARAGRAPH
        )

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("Line one\nLine two"), BlokType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        node = markdown_to_html_node("Just a paragraph")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].children[0].value, "Just a paragraph")

    def test_heading_h1(self):
        node = markdown_to_html_node("# Hello")
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[0].children[0].value, "Hello")

    def test_heading_h3(self):
        node = markdown_to_html_node("### Third level")
        self.assertEqual(node.children[0].tag, "h3")

    def test_code_block(self):
        node = markdown_to_html_node("```\nprint('hi')\n```")
        self.assertEqual(node.children[0].tag, "pre")
        self.assertEqual(node.children[0].children[0].tag, "code")
        self.assertEqual(node.children[0].children[0].value, "print('hi')")

    def test_quote(self):
        node = markdown_to_html_node("> Hello world")
        self.assertEqual(node.children[0].tag, "blockquote")

    def test_unordered_list(self):
        node = markdown_to_html_node("- item 1\n- item 2")
        self.assertEqual(node.children[0].tag, "ul")
        self.assertEqual(len(node.children[0].children), 2)
        self.assertEqual(node.children[0].children[0].tag, "li")
        self.assertEqual(node.children[0].children[1].tag, "li")

    def test_ordered_list(self):
        node = markdown_to_html_node("1. first\n2. second\n3. third")
        self.assertEqual(node.children[0].tag, "ol")
        self.assertEqual(len(node.children[0].children), 3)
        self.assertEqual(node.children[0].children[0].tag, "li")

    def test_paragraph_with_bold(self):
        node = markdown_to_html_node("Hello **world**")
        p = node.children[0]
        self.assertEqual(p.tag, "p")
        self.assertEqual(p.children[0].value, "Hello ")
        self.assertEqual(p.children[1].tag, "b")
        self.assertEqual(p.children[1].value, "world")

    def test_multiple_blocks(self):
        md = "# Title\n\nA paragraph\n\n- item 1\n- item 2"
        node = markdown_to_html_node(md)
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 3)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[1].tag, "p")
        self.assertEqual(node.children[2].tag, "ul")


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_title_with_trailing_whitespace(self):
        self.assertEqual(extract_title("# Hello   "), "Hello")

    def test_title_not_first_line(self):
        md = "Some text\n\n# My Title\n\nMore text"
        self.assertEqual(extract_title(md), "My Title")

    def test_h2_is_not_h1(self):
        with self.assertRaises(Exception):
            extract_title("## Not a title")

    def test_no_title_raises(self):
        with self.assertRaises(Exception):
            extract_title("Just a paragraph\n\nAnother one")

    def test_title_with_longer_text(self):
        self.assertEqual(extract_title("# The Great Gatsby"), "The Great Gatsby")


if __name__ == "__main__":
    unittest.main()

