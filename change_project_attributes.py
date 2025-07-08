r"""
This script is used to change the name of a project. It is useful when you want to change the name of a project and you
want to update all the references to the old name in the project.

You can delete this script after you have changed the name of the project.
"""
import json
import os
import re
import shutil
import sys
import glob
import datetime
import argparse


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project_name",
        default=None,
        type=str,
        help="New name of the project",
        required=True,
    )
    parser.add_argument(
        "--package_name",
        default=None,
        type=str,
        help="New name of the package",
        required=False,
    )
    parser.add_argument(
        "--author",
        default=None,
        type=str,
        help="Author of the project",
        required=True,
    )
    parser.add_argument(
        "--email",
        default=None,
        type=str,
        help="Email of the author of the project",
        required=True,
    )
    parser.add_argument(
        "--url",
        default=None,
        type=str,
        help="URL of the project",
        required=False,
    )
    return parser


def update_pyproject_toml(args):
    with open("pyproject.toml", "r") as f:
        content = f.read()
    if args.project_name is not None:
        content = re.sub(r'name = "(.*?)"', f'name = "{args.project_name}"', content)
    if args.author is not None:
        if args.email is None:
            new_author = 'authors = [{name = "%s"},]' % args.author
        else:
            new_author = 'authors = [{name = "%s", email = "%s"},]' % (args.author, args.email)
        print(f"Setting author to {new_author}")
        content = re.sub(r'authors = \[.*?]', new_author, content)
    if args.package_name is not None:
        content = re.sub(
            r'packages = \[{include = ".*?", from="src"\}]',
            f'packages = [{{include = "{args.package_name}", from="src"}}]',
            content
        )
    with open("pyproject.toml", "w") as f:
        f.write(content)
    return 0


def update_init_file(args):
    # find first __init__.py file in src directory
    init_file = glob.glob("src/**/__init__.py", recursive=True)[0]
    with open(init_file, "r") as f:
        content = f.read()

    if args.author is not None:
        content = re.sub(r'__author__ = "(.*?)"', f'__author__ = "{args.author}"', content)
        year = datetime.datetime.now().year
        content = re.sub(r'__copyright__ = "(.*?)"', f'__copyright__ = "Copyright {year}, {args.author}"', content)
    if args.email is not None:
        content = re.sub(r'__email__ = "(.*?)"', f'__email__ = "{args.email}"', content)
    if args.url is not None:
        content = re.sub(r'__url__ = "(.*?)"', f'__url__ = "{args.url}"', content)
    if args.pakage_name is not None:
        content = re.sub(r'__package__ = "(.*?)"', f'__package__ = "{args.package_name}"', content)
    with open(init_file, "w") as f:
        f.write(content)
    return 0


def update_pkg_folder_name(args):
    if args.package_name is not None:
        # get the first directory in src
        pkg_dir = glob.glob("src/*")[0]
        os.rename(pkg_dir, f"src/{args.package_name}")
    return 0


def update_sphinx_conf_py(args):
    with open("sphinx/source/conf.py", "r") as f:
        content = f.read()
    if args.project_name is not None:
        content = re.sub(r'project = "(.*?)"', f'project = "{args.project_name}"', content)
    if args.package_name is not None:
        content = re.sub(r'import (.*?) as pkg', f'import {args.package_name} as pkg', content)
    with open("sphinx/source/conf.py", "w") as f:
        f.write(content)
    return 0


def update_sphinx_index_rst(args):
    with open("sphinx/source/index.rst", "r") as f:
        content = f.read()
    if args.project_name is not None:
        content = re.sub(r'Welcome to (.*?)’s documentation!', f'Welcome to {args.project_name}’s documentation!', content)
    if args.package_name is not None:
        content = re.sub(r'.. automodule:: pkg', f'.. automodule:: {args.package_name}', content)
    with open("sphinx/source/index.rst", "w") as f:
        f.write(content)
    return 0


def update_sphinx_modules(args):
    with open("sphinx/source/modules.rst", "r") as f:
        content = f.read()
    if args.package_name is not None:
        content = re.sub(r'pkg', args.package_name, content)
    with open("sphinx/source/modules.rst", "w") as f:
        f.write(content)
    return 0


def update_readme_md(args):
    with open("README.md", "r") as f:
        content = f.read()
    if args.project_name is not None:
        content = re.sub(r'# PythonProject-Template', f'# {args.project_name}\n', content)
    with open("README.md", "w") as f:
        f.write(content)
    return 0


def update_license(args):
    if not os.path.exists("LICENSE"):
        return 0
    with open("LICENSE", "r") as f:
        content = f.read()
    if args.author is not None:
        content = re.sub(r'Copyright (.*?) (.*?)', f'Copyright {datetime.datetime.now().year} {args.author}', content)
    with open("LICENSE", "w") as f:
        f.write(content)
    return 0


def update_docs_yml(args):
    if not os.path.exists(".github/workflows/docs.yml"):
        return 0
    with open(".github/workflows/docs.yml", "r") as f:
        content = f.read()
    if args.package_name is not None:
        content = re.sub(r'<package_name>', args.package_name, content)
    with open(".github/workflows/docs.yml", "w") as f:
        f.write(content)
    return 0


def update_dockerfile(args):
    if not os.path.exists("Dockerfile"):
        return 0
    with open("Dockerfile", "r") as f:
        content = f.read()
    root_dir = os.path.basename(os.path.dirname(__file__))
    print(f"ROOT_DIR=/{root_dir}")
    content = re.sub(r'ENV ROOT_DIR=/(.*?)\n', f'ENV ROOT_DIR=/{root_dir}\n', content)
    with open("Dockerfile", "w") as f:
        f.write(content)
    return 0


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.package_name is None:
        # Camel case to snake case
        args.package_name = re.sub(r'(?<!^)(?=[A-Z])', '_', args.project_name).lower()
        print(f"Package name not provided. Setting package name to {args.package_name}")
    if args.url is None:
        args.url = f"https://github.com/{args.author}/{args.project_name}"
        print(f"URL not provided. Setting URL to {args.url}")

    print(f"Updating project variables with the following values:")
    print(json.dumps(vars(args), indent=4))

    update_pyproject_toml(args)
    update_init_file(args)
    update_pkg_folder_name(args)
    update_sphinx_conf_py(args)
    update_sphinx_index_rst(args)
    update_sphinx_modules(args)
    update_readme_md(args)
    update_license(args)
    update_docs_yml(args)
    update_dockerfile(args)
    return 0


if __name__ == '__main__':
    sys.exit(main())

