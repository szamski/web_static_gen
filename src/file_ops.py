import os, shutil
from markdown_parser import markdown_to_html_node, extract_title


def file_update():
    try:
        if os.path.exists("public/"):
            shutil.rmtree("public/")
        shutil.copytree("static/", "public/")

    except Exception as e:
        return f"Error: {e}"


def generate_page(from_path, template_path, dest_path):

    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")

    try:
        with open(from_path, "r") as f:
            file_content_md = f.read()
        with open(template_path, "r") as f:
            file_content_template = f.read()

        text = extract_title(file_content_md)
        html = markdown_to_html_node(file_content_md).to_html()
        completed = file_content_template.replace("{{ Title }}", text).replace(
            "{{ Content }}", html
        )

        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w") as f:
            f.write(completed)

    except Exception as e:
        return f"Error {e}"


def generate_pages_recursive(content_path, template_path, dest_path):

    try:
        for dirpath, dirnames, filenames in os.walk(content_path):
            for filename in filenames:
                if filename.endswith(".md"):
                    src = os.path.join(dirpath, filename)
                    rel = os.path.relpath(src, content_path)
                    dest = os.path.join(dest_path, rel.replace(".md", ".html"))
                    generate_page(src, template_path, dest)

    except Exception as e:
        return f"Error {e}"
