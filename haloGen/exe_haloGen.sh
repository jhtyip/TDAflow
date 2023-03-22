#!/bin/bash

set -e

ENVNAME=TDAflow_yt
ENVDIR=$ENVNAME

export PATH
mkdir $ENVDIR
cp /staging/hyip2/TDAflow/$ENVNAME.tar.gz ./
tar -xzf $ENVNAME.tar.gz -C $ENVDIR/
. $ENVDIR/bin/activate

cp /staging/hyip2/TDAflow/snapGen/snaps/fs_0.1_1.0_10_256_64_1_0.2001_0.6809.npy .

python haloGen.py fs_0.1_1.0_10_256_64_1_0.2001_0.6809

ls
cd halo_catalogs
ls
cd ..

tar -czf halo_catalogs.tar.gz halo_catalogs/
mv halo_catalogs.tar.gz /staging/hyip2/TDAflow/haloGen/halos/

rm haloGen.py
rm fs_0.1_1.0_10_256_64_1_0.2001_0.6809.npy
rm $ENVNAME.tar.gz

mkdir empty_dir
rsync -a --delete empty_dir/ halo_catalogs/
rsync -a --delete empty_dir/ $ENVNAME/
rmdir empty_dir