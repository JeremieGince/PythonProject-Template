import os
import argparse
import subprocess
import json
import time
from typing import Optional


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dockerfiles_folder",
        type=str,
        default=os.path.join(os.path.dirname(__file__), ".."),
    )
    parser.add_argument(
        "--tag",
        type=str,
        default="latest",
    )
    parser.add_argument(
        "--image_name",
        type=str,
        default=None,
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="release",
        choices=["release", "data", "trainings", "analysis", "it"],
        help="Mode of the project to run the container for. \n"
             "- release: This mode is responsible for running the __main__.py of the current package. \n"
             "- it: This is a development mode that is responsible for running the container in the interactive mode.",
    )
    parser.add_argument(
        "--args",
        type=str,
        default=None,
        help="Arguments to pass to the container as a JSON string "
    )
    parser.add_argument(
        "--only_run",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="If set, only runs the container without building the image.",
    )
    return parser


def build_images(
        *,
        dockerfiles_folder: str = ".",
        tag: str = "latest",
        image_name: Optional[str] = None,
):
    if not image_name:
        image_name = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
    images = []
    for root, dirs, files in os.walk(dockerfiles_folder):
        for file in files:
            if not file.startswith("Dockerfile"):
                continue
            post_name = file.replace("Dockerfile", "")
            full_image_name = f"{image_name}{post_name}:{tag}"
            print(f"Building image {full_image_name} from {os.path.join(root, file)}")
            cmd = f"docker build -t {full_image_name} -f {os.path.join(root, file)} ."
            print(f"{cmd = }")
            subprocess.run(cmd, shell=True, check=True, cwd=root)
            print(f"Built image {full_image_name}")
            images.append(full_image_name)
    print(f"Pruning old images")
    cmd = "docker image prune --force"
    print(f"{cmd = }")
    subprocess.run(cmd, shell=True, check=True)
    print(f"Pruned old images")
    return images

def run_container(
        *,
        container_name: str = None,
        image_name: str = None,
        tag: str = "latest",
        args: list = None,
        run_args: list = None,
):
    root_folder_name = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
    if not container_name:
        container_name = f"{image_name}-container"
    if not image_name:
        image_name = root_folder_name
    if ":" in image_name:
        image_name, tag = image_name.split(":")
    print(f"Removing container {container_name} if it exists")
    cmd = f"docker rm --force {container_name}"
    print(f"{cmd = }")
    subprocess.run(cmd, shell=True, check=False)
    print(f"Removed container {container_name}")
    time.sleep(1)
    print("-" * 80)
    print(f"Running container {container_name} from image {image_name}:{tag}")
    container_args = [
        "--name", container_name,
        "--detach",
        f"--volume="
        f"{os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))}"
        f":/{root_folder_name}/data",
    ]
    run_args_str = " ".join([str(arg) for arg in run_args]) if run_args else ""
    cmd = f"docker run {' '.join(container_args)} {run_args_str} {image_name}:{tag}"
    if args:
        cmd += " " + " ".join([str(arg) for arg in args])
    print(f"{cmd = }")
    subprocess.run(cmd, shell=True, check=True)
    print(f"Container {container_name} is now running in the background.")
    return

def main():
    args = get_args_parser().parse_args()
    if not args.image_name:
        args.image_name = os.path.basename(os.path.dirname(os.path.dirname(__file__)))
    print(f"Running with args: {json.dumps(vars(args), indent=4)}")
    if args.only_run:
        images = [f"{args.image_name}:{args.tag}"]
    else:
        images = build_images(
            dockerfiles_folder=args.dockerfiles_folder,
            tag=args.tag,
            image_name=args.image_name,
        )
    for image in images:
        run_container(
            image_name=image,
            tag=args.tag,
            args=json.loads(args.args) if args.args else None,
            container_name=f"{args.image_name}-{args.mode}",
            run_args=["-e", f"MODE={args.mode}"],
        )
    return 0


if __name__ == "__main__":
    exit(main())

