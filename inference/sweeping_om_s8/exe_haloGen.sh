#!/bin/bash

set -e

ENVNAME=TDAflow
ENVDIR=$ENVNAME

export PATH
mkdir $ENVDIR
cp /staging/hyip2/TDAflow/$ENVNAME.tar.gz ./
tar -xzf $ENVNAME.tar.gz -C $ENVDIR/
. $ENVDIR/bin/activate
rm $ENVNAME.tar.gz

python haloGen.py $1 $2 $3 $4 $5 $6 $7 $8 $9

rm haloGen.py

mkdir empty_dir
rsync -a --delete empty_dir/ $ENVNAME/
rmdir empty_dir