#!/bin/bash
#SBATCH --account=train21_seamless
#SBATCH --partition=g100_usr_prod
#SBATCH --nodes=4
#SBATCH --ntasks-per-node 1
#SBATCH --cpus-per-task 48
#SBATCH --time=01:00:00
#SBATCH --output=%j.out
#SBATCH --error=%j.err

conda activate seamless-bb

# Generate secret for Parallel Python authentication between server and client
secret=`cat /dev/urandom | tr -cd 'a-f0-9' | head -c 32`

# Pick IP port for Parallel Python communication (IANA: use 49152 to 65535 for dynamic/private ports)
port=`python -c 'import random; print(random.randint(49152,65535))'`

# run the servers
srun --output %j-%3t.out --error %j-%3t.err ppserver.py -w $SLURM_CPUS_PER_TASK -t 3600 -s $secret -p $port -r &

# launch the parsac job
parsac sensitivity run --ppservers $SLURM_JOB_NODELIST:$port --ncpus 0 --secret=$secret sa.pickle
