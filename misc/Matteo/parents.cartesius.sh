#!/bin/sh

#SBATCH -J rockstar
#SBATCH -o RUNinfo/rockstar_parents-out%J.o
#SBATCH -e RUNinfo/rockstar_parents-error%J.e
#SBATCH --ntasks 32
#SBATCH --partition=thin
##SBATCH --mem-per-cpu=4GB
#SBATCH --time=1:00:00                                                                                                                                                 
#SBATCH --mail-user=M.biagetti@uva.nl                                     
#SBATCH --mail-type=ALL


exe=/home/bmatteo/Codes/Rockstar-0.99.9-RC3/util/find_parents

$exe out_0.list 2000 > out_0_parents.list
sleep 5

$exe out_1.list 2000 > out_1_parents.list
sleep 5

$exe out_2.list 2000 > out_2_parents.list
sleep 5

#$exe out_3.list 2000 > out_3_parents.list


#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_085_run2/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                  
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_085_run3/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_085_run4/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_085_run5/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_085_run6/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_083_run1/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_083_run2/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_083_run5/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_083_run6/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_087_run1/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_087_run2/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_087_run5/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_gaussian_1536_2Gpc_087_run6/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_250_1536_2Gpc_085_run1/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
##perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'                                                     
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_250_1536_2Gpc_085_run2/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list                                                               
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_250_1536_2Gpc_085_run2/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_250_1536_2Gpc_085_run3/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_250_1536_2Gpc_085_run4/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_250_1536_2Gpc_085_run5/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_250_1536_2Gpc_085_run6/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_m250_1536_2Gpc_085_run1/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_m250_1536_2Gpc_085_run2/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_m250_1536_2Gpc_085_run3/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_m250_1536_2Gpc_085_run4/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

#$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_m250_1536_2Gpc_085_run5/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list

#cd /space/nbody/matteo/byagox_NGaussian_250_1536_2Gpc_085_run6/FOF/Rockstar/

#$exe out_0.list 2000 > out_0_parents.list
#sleep 5

#$exe out_1.list 2000 > out_1_parents.list
#sleep 5

##$exe out_2.list 2000 > out_2_parents.list
#sleep 5

#$exe out_3.list 2000 > out_3_parents.list
