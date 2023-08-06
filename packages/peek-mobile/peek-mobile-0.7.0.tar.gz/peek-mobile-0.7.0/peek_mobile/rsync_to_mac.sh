#!/bin/bash

MAC_PATH="/media/psf/stash/build-ns"

PATHS="build-ns/app"
PATHS="$PATHS build-ns/hooks"
PATHS="$PATHS build-ns/package.json"
PATHS="$PATHS build-ns/package-lock.json"
PATHS="$PATHS build-ns/references.d.ts"
PATHS="$PATHS build-ns/tsconfig.json"

rsync -rvP  $PATHS $MAC_PATH

