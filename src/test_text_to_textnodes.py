import unittest

from textnode import TextNode, TextType
from markdown_parser import text_to_textnodes


class TestTextToTextNode(unittest.TestCase):

    def test_text_to_textnodes_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        self.assertEqual(result, [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_text_to_textnodes_plain_only(self):
        text = "Just plain text"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("Just plain text", TextType.PLAIN)])

    def test_text_to_textnodes_bold_only(self):
        text = "**bold**"
        result = text_to_textnodes(text)
        self.assertEqual(result, [TextNode("bold", TextType.BOLD)])


if __name__ == "__main__":
    unittest.main()