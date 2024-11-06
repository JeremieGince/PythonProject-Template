import os
import sys
import glob


def generate_doc(path_to_root_dir: str = '.'):
	pkg_name = glob.glob(f"{path_to_root_dir}/src/*/__init__.py")[0].split("/")[-2]
	commands = [
		rf"sphinx-apidoc -f -o {path_to_root_dir}/sphinx/source {path_to_root_dir}/src/{pkg_name}",
		rf"{path_to_root_dir}\sphinx\make clean html",
		rf"{path_to_root_dir}\sphinx\make html",
	]
	for command in commands:
		print(f"Executing: {command}")
		os.system(command)


if __name__ == '__main__':
	root_dir = sys.argv[1] if len(sys.argv) > 1 else '..'
	generate_doc(root_dir)
