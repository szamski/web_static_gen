from enum import Enum
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, text_node_to_html_node, HTMLNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.PLAIN:
            new_nodes.append(node)
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

        