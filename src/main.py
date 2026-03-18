from textnode import *
from file_ops import file_update

def main():

    textnode = TextNode("This is some anchor text", "link", "https://www.boot.dev")
    file_update()

    print(textnode)


main()