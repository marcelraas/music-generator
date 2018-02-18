#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

BASEDIR=${DIR}/../

source ${BASEDIR}/venv/bin/activate &&
export PYTHONPATH=${BASEDIR} &&
jupyter notebook .

