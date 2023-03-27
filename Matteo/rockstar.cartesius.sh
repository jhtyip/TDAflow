#!/bin/sh

# THE NAME OF THE SBATCH JOB

#SBATCH -J rockstar                                                                                                                    

# REDIRECT OUTPUT TO THE FOLLOWING STREAM                                                                                            
 
#SBATCH -e RUNinfo/rockstar-error%j                                       
#SBATCH -o RUNinfo/rockstar-out%j                                         

# NUMBER OF NODES                                                                                                                     
#SBATCH --ntasks 128
#SBATCH --exclusive

##SBATCH --mem-per-cpu=4GB                                                                                                             

# ENVIRONMENT                                                                                                                         
#SBATCH --partition=fat                                                                                                            
##SBATCH --constraint=[island1|island2|island3|island4|island5] 
##SBATCH --constraint=[haswell]

# SET THE TIME LIMIT [HRS:MINS:SECS]                                                                                                  
#SBATCH --time=02:00:00                                                                                                             

#SBATCH --mail-user=m.biagetti@uva.nl                                                                                                 
#SBATCH --mail-type=ALL                                                                                                               

#export LD_LIBRARY_PATH=/home/biagetti/lib:{LD_LIBRARY_PATH}     

exe=/home/bmatteo/Codes/Rockstar-0.99.9-RC3/rockstar

echo Entering $(pwd)

rm auto-rockstar.cfg 
$exe -c rockbao.cfg >& server.dat &
#perl -e 'sleep 1 while (!(-e "auto-rockstar.cfg"))'
sleep 20

echo Reading and Writing

srun $exe -c auto-rockstar.cfg

rm halos_*
