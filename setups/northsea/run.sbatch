#!/bin/bash
#SBATCH --account=tra21_seamless
#SBATCH --partition=g100_usr_prod
#KB#SBATCH --nodes=4
#SBATCH --ntasks 10
#KB #SBATCH --ntasks 12
#SBATCH --time=01:00:00
#SBATCH --output=%j.out
#SBATCH --error=%j.err

#conda init bash
conda activate seamless-bb
export PYTHONUNBUFFERED=TRUE

hostnames=`scontrol show hostnames $SLURM_JOB_NODELIST | sed -z 's/\n/:'"$port"',/g'`
echo Host names provided to eat: $hostnames

# launch the eat job
echo Starting eat

# ensemble run only
mpiexec -n 10 eat_model_gotm

# assimilate the full period
#srun -np 1 eat_obs_gotm.py --start "2016-01-01 12:00:00" --stop "2019-12-31 12:00:00" -o temp[-1] cci_sst.dat  : -np 1 eat_filter_pdaf : -np 10 eat_model_gotm

# assimilate the only a period that prevents blow up
#srun -np 1 eat_obs_gotm.py --start "2016-01-01 12:00:00" --stop "2016-03-15 12:00:00" -o temp[-1] cci_sst.dat  : -np 1 eat_filter_pdaf : -np 10 eat_model_gotm

echo Done
