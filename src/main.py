from file_ops import file_update, generate_page, generate_pages_recursive
import sys


def main():

    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    file_update()
    generate_pages_recursive("content", "template.html", "docs", basepath)


main()
