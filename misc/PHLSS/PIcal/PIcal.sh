#!/bin/bash

set -e

ENVNAME=PHLSS_j
ENVDIR=$ENVNAME

export PATH
mkdir $ENVDIR
cp /staging/hyip2/$ENVNAME.tar.gz ./
tar -xzf $ENVNAME.tar.gz -C $ENVDIR/
. $ENVDIR/bin/activate

cp /staging/hyip2/bounds.npy ./
cp /staging/hyip2/PHcal/$1_0_25_5.tar.gz ./
mkdir $1_0_25_5
tar -xzf $1_0_25_5.tar.gz -C $1_0_25_5
cp /staging/hyip2/PHcal/$1_25_50_5.tar.gz ./
mkdir $1_25_50_5
tar -xzf $1_25_50_5.tar.gz -C $1_25_50_5
cp /staging/hyip2/PHcal/$1_50_75_5.tar.gz ./
mkdir $1_50_75_5
tar -xzf $1_50_75_5.tar.gz -C $1_50_75_5
cp /staging/hyip2/PHcal/$1_75_100_5.tar.gz ./
mkdir $1_75_100_5
tar -xzf $1_75_100_5.tar.gz -C $1_75_100_5

python PIcal.py $1

rm PIcal.py

rm bounds.npy
rm $1_0_25_5.tar.gz
rm -r $1_0_25_5
rm $1_25_50_5.tar.gz
rm -r $1_25_50_5
rm $1_50_75_5.tar.gz
rm -r $1_50_75_5
rm $1_75_100_5.tar.gz
rm -r $1_75_100_5

rm $ENVNAME.tar.gz
rm -r $ENVDIR