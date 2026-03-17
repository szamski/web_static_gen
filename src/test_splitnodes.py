import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType

class TestSplitNodes(unittest.TestCase):
    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.PLAIN),
            ])

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.PLAIN)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("Just plain text", TextType.PLAIN)])
    # powinien zwrócić jeden node, bez zmian

    def test_unclosed_delimiter(self):
        node = TextNode("This is **broken", TextType.PLAIN)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    # jak testować czy rzuca wyjątek? → assertRaises
