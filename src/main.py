from textnode import *
from file_ops import file_update, generate_page, generate_pages_recursive


def main():

    textnode = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    file_update()
    generate_pages_recursive("content", "template.html", "public")
    print(textnode)


main()
