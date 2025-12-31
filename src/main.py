import os
import shutil
import sys

from generate_page import generate_pages_recursive


def copy_static(source, dest):
    if os.path.exists(dest):
        print(f"Deleting {dest}...")
        shutil.rmtree(dest)

    print(f"Creating {dest}...")
    os.makedirs(dest)

    copy_contents(source, dest)


def copy_contents(source, dest):
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(source_path):
            print(f"Copying {source_path} to {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"Creating directory {dest_path}")
            os.makedirs(dest_path)
            copy_contents(source_path, dest_path)


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    generate_pages_recursive("content/", "template.html", "docs/", basepath)


main()
