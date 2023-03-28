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

python main.py $1 $2 $3 $4 $5 $6 $7 $8 $9

rm main.py
rm fclaux.py
rm param.py
rm pdiagram.py

mkdir empty_dir
rsync -a --delete empty_dir/ $ENVNAME/
rmdir empty_dir