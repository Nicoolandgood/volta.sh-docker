# Volta.sh Docker

This repository contains Docker images for the [volta.sh](https://volta.sh/) toolchain.

## Usage

Either build the image or pull it from the repository:
```sh
# Building
docker build . --tag volta.sh:latest

# Pulling
docker pull volta.sh:latest
```

You can then run it with:
```sh
docker run -d volta.sh:latest
```

## Build arguments

In order to customize your image, you can pass arguments to docker before the building process.

### `NODE_VERSION`
The default `node` version installed when building the image. `latest` by default.

```sh
# This will run volta install node@16 during build.
docker build --build-arg="NODE_VERSION=16" .
```

### `PACKAGE_MANAGER`
The default package manager used inside the container. 
Possible values are `npm`, `yarn` and `pnpm`, `npm` by default.

```sh
# This will run volta install yarn during build.
docker build --build-arg="PACKAGE_MANAGER=yarn" .
```

### `VOLTA_USER`
The user created inside the container. `volta` by default.

```sh
docker build --build-arg="VOLTA_USER=jotaro" .
```

## Env variables

### `VOLTA_FEATURE_PNPM`
This enables the `pnpm` support. Its value is set to `1` by default.
You can find more information in [the volta pnpm support page.](https://docs.volta.sh/advanced/pnpm).

### `RUN_PACKAGE_MANAGER`
This runs the default package manager if set to `1`.
If not, `sleep infinity` is run.
Its value is set to `0` by default.

Before running the package manager, it will install dependencies as such:
```sh
# If pnpm is the default package manager
pnpm i
pnpm $@
```

Note that, by default, enabling this feature doesn't do much. It must be coupled with `CMD` override to
pass arguments to the package manager:

```dockerfile
# ...image customization

CMD ["start"]
```

will result to:

```sh
# If pnpm is the default package manager
pnpm i
pnpm start
```

### `PACKAGE_MANAGER_INSTALL_ARGS`

This variable appends arguments during the dependencies installation.

It could be used to install only production dependencies:

```sh
docker build --build-arg="PACKAGE_MANAGER=yarn" .
docker run -d -e PACKAGE_MANAGER_INSTALL_ARGS='--production' volta.sh:latest
```

will result to:
```sh
yarn install --production
yarn [some command]
```

## Entrypoint script

The entrypoint script is located in `/entrypoint.sh`. It can be replaced to personalize container start behavior.

Here is an example with `docker compose`:
```yaml
services:
    web-app:
        image: volta.sh:latest

        volume:
            ./my-entrypoint.sh:/entrypoint.sh
```