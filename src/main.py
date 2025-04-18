import os.path
import shutil
import sys

import conversion

def copy_dir(src_dir: str, dest_dir: str):
    for entry in os.listdir(src_dir):
        src_path = os.path.join(src_dir, entry)
        dest_path = os.path.join(dest_dir, entry)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print("copy {} to {}".format(src_path, dest_path))
        elif os.path.isdir(src_path):
            os.makedirs(dest_path)
            copy_dir(src_path, dest_path)


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        content = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_content = conversion.markdown_to_html_node(content).to_html()
    title = conversion.extract_title(content)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    page = page.replace('href="/', f'href="{basepath}')
    page = page.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def main():

    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]

    output_dir = os.path.relpath("docs")

    if os.path.exists(output_dir):
        print("clearing build directory")
        shutil.rmtree(output_dir)

    os.makedirs(output_dir)

    static_dir = os.path.relpath("static")
    copy_dir(static_dir, output_dir)
    generate_page("content/index.md", "template.html", "docs/index.html", basepath)
    generate_page("content/blog/glorfindel/index.md", "template.html", "docs/blog/glorfindel/index.html", basepath)
    generate_page("content/blog/tom/index.md", "template.html", "docs/blog/tom/index.html", basepath)
    generate_page("content/blog/majesty/index.md", "template.html", "docs/blog/majesty/index.html", basepath)
    generate_page("content/contact/index.md", "template.html", "docs/contact/index.html", basepath)


main()