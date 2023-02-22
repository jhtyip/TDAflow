#!/bin/bash

set -e

ENVNAME=TDAflow
ENVDIR=$ENVNAME

export PATH
mkdir $ENVDIR
cp /staging/hyip2/TDAflow/$ENVNAME.tar.gz ./
tar -xzf $ENVNAME.tar.gz -C $ENVDIR/
. $ENVDIR/bin/activate

python snapGen.py $1 $2

rm snapGen.py
rm $ENVNAME.tar.gz

mkdir empty_dir
rsync -a --delete empty_dir/ $ENVNAME/
rmdir empty_dir