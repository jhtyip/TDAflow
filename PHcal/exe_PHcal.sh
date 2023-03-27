#!/bin/bash

set -e

ENVNAME=PHLSS_j
ENVDIR=$ENVNAME

export PATH
mkdir $ENVDIR
cp /staging/hyip2/$ENVNAME.tar.gz ./
tar -xzf $ENVNAME.tar.gz -C $ENVDIR/
. $ENVDIR/bin/activate

mkdir $1_$2_$3
cp /staging/hyip2/compressed_cat/$1_$2_$3.tar.gz ./
tar -xzvf $1_$2_$3.tar.gz -C $1_$2_$3/

python mainRunner.py $4 $5 $1 $2 $3
python tar_rm_Output.py $1 $2 $3 $4 $5

mv $1_$2_$3_$5.tar.gz /staging/hyip2/PHcal/

rm fclaux.py
rm main.py
rm mainRunner.py
rm param.py
rm pdiagram.py
rm tar_rm_Output.py

rm $ENVNAME.tar.gz
rm $1_$2_$3.tar.gz
mkdir empty_dir
rsync -a --delete empty_dir/ $ENVNAME/
rsync -a --delete empty_dir/ $1_$2_$3/
rmdir empty_dir