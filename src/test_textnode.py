import unittest

from textnode import TextNode, TextType
from htmlnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD, TextType.LINK)
        self.assertEqual(node, node2)
        
    def test_not_eq(self):   
        node = TextNode("This is a text node", TextType.BOLD, TextType.LINK)
        node2 = TextNode("This is a text noodle", TextType.BOLD, TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text noodle", TextType.BOLD, TextType.LINK)
        self.assertIsNone(node.url, node2.url)

    def test_text_prop(self):   
        node = TextNode("This is a text node", TextType.ITALIC, TextType.LINK)
        node2 = TextNode("This is a text noodle", TextType.BOLD, TextType.LINK)
        self.assertNotEqual(node.text_type, node2.text_type)

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()