#!/bin/bash

if [ -z "$PACKAGE_MANAGER" ]; then
    echo "PACKAGE_MANAGER not defined."
    exit 1
fi

volta install node@${NODE_VERSION}
volta install ${PACKAGE_MANAGER}

if [ $RUN_PACKAGE_MANAGER -eq 0 ]; then
    sleep infinity
    exit 0
fi

case "$PACKAGE_MANAGER" in
yarn)
    yarn install $PACKAGE_MANAGER_INSTALL_ARGS
    yarn $@
    ;;
npm)
    npm i $PACKAGE_MANAGER_INSTALL_ARGS
    npm $@
    ;;
pnpm)
    pnpm i $PACKAGE_MANAGER_INSTALL_ARGS
    pnpm $@
    ;;
*)
    echo "PACKAGE_MANAGER has unknown value. Use 'yarn', 'npm' or 'pnpm'."
    exit 1
    ;;
esac
