FROM debian:bookworm-slim

LABEL maintainer="Nicoolandgood <nicolas+nicoolandgood@barestho.com>"

# Dependencies downloads
RUN apt update && apt install -y curl

# Build arguments
ARG VOLTA_USER=volta

# Variables
ENV NODE_VERSION=latest
ENV PACKAGE_MANAGER=npm
ENV SHELL="/bin/bash"
ENV PACKAGE_MANAGER=${PACKAGE_MANAGER}
ENV HOME=/home/${VOLTA_USER}
ENV PACKAGE_MANAGER_INSTALL_ARGS=""
ENV RUN_PACKAGE_MANAGER=0

# Creating volta user
RUN useradd ${VOLTA_USER} --home-dir=${HOME}

# Copying entrypoint script
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod 755 /entrypoint.sh

USER ${VOLTA_USER}
WORKDIR ${HOME}

# Installing volta for current user
RUN curl https://get.volta.sh | bash

# Volta env vars
ENV VOLTA_HOME="${HOME}/.volta"
ENV PATH="${VOLTA_HOME}/bin:${PATH}"
ENV VOLTA_FEATURE_PNPM=1

ENTRYPOINT ["/entrypoint.sh"]