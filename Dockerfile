# podman build --tag tornado_hello_world:v1 .
# podman run --rm --interactive --tty --name hello_world tornado_hello_world:v1 /bin/sh
# podman run --rm --detach --tty --publish 8889:8888/tcp --name hello_world --name hello_world tornado_hello_world:v1
# Use a smaller image
FROM docker.io/library/alpine:latest

# Install the required Python modules
RUN apk add python3 py3-tornado

# Add the Python file to be used
COPY app.py /app.py
COPY cli.py /cli.py

# No need to run as root in the container
ARG USERNAME=appuser
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# Add a user account
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}

USER ${USERNAME}

# Set the command to run on start up
ENTRYPOINT ["python3", "/cli.py"]
