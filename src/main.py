import os
import shutil
import sys

from generator import generate_pages_recursive


def sync_replace_files_in_dict(
    source_path: str = None,
    destination_path: str = None
) -> None:
    if not source_path or not destination_path:
        raise ValueError("no source_path or destination_path")

    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source path '{source_path}' does not exist.")

    # Try to remove contents from destination_path
    if os.path.exists(destination_path):
        try:
            shutil.rmtree(destination_path)
        except Exception as e:
            raise RuntimeError(f"Failed to remove destination path: {e}")

    # Create destination directory
    os.makedirs(destination_path, exist_ok=True)

    def copy_recursive(src: str, dst: str) -> None:
        for item in os.listdir(src):
            src_item = os.path.join(src, item)
            dst_item = os.path.join(dst, item)
            if os.path.isdir(src_item):
                os.makedirs(dst_item, exist_ok=True)
                print(f"Created directory: {dst_item}")
                copy_recursive(src_item, dst_item)
            else:
                shutil.copy2(src_item, dst_item)
                print(f"Copied file: {dst_item}")

    copy_recursive(source_path, destination_path)


def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    sync_replace_files_in_dict("./static", "./docs")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)


if __name__ == "__main__":
    main()
