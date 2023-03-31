#!/bin/bash

set -e

ENVNAME=PHLSS_j
ENVDIR=$ENVNAME

export PATH
mkdir $ENVDIR
cp /staging/hyip2/$ENVNAME.tar.gz ./
tar -xzf $ENVNAME.tar.gz -C $ENVDIR/
. $ENVDIR/bin/activate
rm $ENVNAME.tar.gz

python PIGen.py $1 $2 $3 $4 $5 $6 $7 $8 $9 $(10) $(11) $(12)

rm PIGen.py

mkdir empty_dir
rsync -a --delete empty_dir/ $ENVNAME/
rmdir empty_dir