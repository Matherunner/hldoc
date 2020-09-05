#!/bin/bash

if [[ -z $INKSCAPE_BIN ]]; then
    printf "The INKSCAPE_BIN environmental variable must be set\n"
    exit 1
fi

"$INKSCAPE_BIN" -g --verb=com.jwchong.www.hlprpdf2svg $@
