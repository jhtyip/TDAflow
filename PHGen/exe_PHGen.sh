#!/bin/bash

set -e

ENVNAME=PHLSS_j
ENVDIR=$ENVNAME

export PATH
mkdir $ENVDIR
cp /staging/hyip2/$ENVNAME.tar.gz ./
tar -xzf $ENVNAME.tar.gz -C $ENVDIR/
. $ENVDIR/bin/activate

python main.py $1 $2 $3

rm main.py
rm fclaux.py
rm param.py
rm pdiagram.py
rm $ENVNAME.tar.gz

mkdir empty_dir
rsync -a --delete empty_dir/ $ENVNAME/
rmdir empty_dir