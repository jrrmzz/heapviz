#!/bin/bash

BASE="$(dirname -- $1)"
if [ -h $1 ]
then
    BASE="$(dirname -- $(readlink $1))"
fi

BASE_ABS=$(cd "${BASE}"; pwd)

SCRIPT_NAME=${BASE_ABS}/$(basename $1)
STARTING_INSTRUCTION=$2

# ZOOM=1 => 72 ppi; 4 => 288 ppi
ZOOM=4

pushd $(dirname $0) 2>&1 >/dev/null
python3 heapviz.py ${SCRIPT_NAME} ${STARTING_INSTRUCTION}
python webkit2png/webkit2png -F -z ${ZOOM} -o ${SCRIPT_NAME} file://${SCRIPT_NAME}.heapviz.html
python autocrop.py ${SCRIPT_NAME}-full.png ${SCRIPT_NAME}.png

rm ${SCRIPT_NAME}-full.png
rm ${SCRIPT_NAME}.heapviz.html
popd