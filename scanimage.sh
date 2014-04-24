#!/bin/bash

startdir=$(pwd)
tmpdir=$(date +%Y-%m-%d.%H.%M)

mkdir -p priv/$tmpdir
cd priv/$tmpdir

device=`scanimage -L`

device=${device##*device \`}
device=${device%%\'*}


if grep -q -v epkowa <<<$device; then
    echo "it's there"
fi

scanimage --device-name=${device} --batch='out%d.tiff' --wait-for-button=yes  --format=tiff -p

cd $startdir


