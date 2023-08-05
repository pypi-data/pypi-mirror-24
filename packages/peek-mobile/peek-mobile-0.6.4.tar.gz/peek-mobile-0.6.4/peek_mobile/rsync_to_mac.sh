#!/bin/bash

rsync -avP --delete build-ns /media/psf/stash --exclude node_modules --exclude platforms


