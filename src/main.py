import os.path
import shutil

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


output_dir = os.path.relpath("../public")

if os.path.exists(output_dir):
    print("clearing build directory")
    shutil.rmtree("../public")

os.makedirs(output_dir)

static_dir = os.path.relpath("../static")
copy_dir(static_dir, output_dir)