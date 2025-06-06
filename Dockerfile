FROM python:3.10-slim AS base_stage
ENV ROOT_DIR=/PythonProject-Template
ARG MODE=release
# MODE: 'release' or 'it' (will be interpreted as debug). This is used in the docker_entrypoint.sh script
ENV MODE=${MODE}

# Build stage
FROM base_stage AS build_stage

ARG DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt update -y &&  \
    apt install -y --no-install-recommends build-essential git dos2unix &&  \
    rm -rf /var/lib/apt/lists/*

# Files
WORKDIR "$ROOT_DIR"
COPY *_requirements.txt requirements.txt *.toml *.lock *.py ./
COPY src src
COPY dist dist
COPY docker_files docker_files
RUN dos2unix docker_files/*.sh

# Virtual environment
RUN python3 -m venv ./venv &&  \
    . ./venv/bin/activate &&  \
    pip install --upgrade pip &&  \
    pip install poetry &&  \
    poetry install --no-interaction --no-ansi

# rm unnecessary files
RUN rm -rf *_requirements.txt requirements.txt *.toml *.lock setup.py run_pytests.py src/*.egg-info dist

# Main stage
FROM base_stage AS main_stage

# Files
WORKDIR $ROOT_DIR
COPY --from=build_stage $ROOT_DIR ./

# Entrypoint
ENV PATH="venv/bin:$PATH"
ENTRYPOINT ["bash", "docker_files/docker_entrypoint.sh"]
