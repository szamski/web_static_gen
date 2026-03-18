import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from converters import text_node_to_html_node
from textnode import TextType, TextNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("python", 12, None, None)
        node2 = HTMLNode("python", 12, None, None)
        self.assertEqual(node, node2)
        
    def test_not_eq(self):   
        node = HTMLNode("nodejs", 12, None, None)
        node2 = HTMLNode("python", 12, None, None)
        self.assertNotEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

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
    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

if __name__ == "__main__":
    unittest.main()