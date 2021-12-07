### EAT workflow

(for KB - export PATH=~/source/repos/EAT/eat/models/gotm/:$PATH )

### Multiple restart-files
```bash
cp eat_gotm.nml.org eat_gotm.nml
cp eat_pdaf.nml.org eat_pdaf.nml
```

Edit eat_gotm.nml and un-comment the line with shared_restart_file

```bash
mkdir restart_files
cp physics_restart.nc restart_files/restart.nc
cd restart_files
```

Generate a series of restart files via a python script.

```bash
generate_gotm_ensemble.py -e z -e zi restart.nc 10
```

Optionally plot e.g. temperature

```bash
multiplot -s "restart_????.nc" -e "statistics(temp[:,0,:,0,0], 'obs')"
```

or saving to a file

```bash
multiplot -s "restart_????.nc" -e "statistics(temp[:,0,:,0,0], 'obs')" -o temp.png
```

Preparing the run-directory

```bash
cd ..
cp restart_files/restart_????.nc .
```

Ready to run.

First in pure ensemble mode:

```bash
mpiexec -np 10 eat_model_gotm
```

or via a queue - please edit run.sbatch to reflect the type of run you are doing. We will need to maybe update run.sbatch to not use mpiexec - but srun.

```bash
sbatch run.sbatch
```

Now in full DA model:
```bash
cp restart_files/restart_????.nc .
```

On the command line:

```bash
mpiexec --oversubscribe -np 1 eat_obs_gotm.py --start "2016-01-01 12:00:00" --stop "2019-12-31 12:00:00" -o temp[-1] cci_sst.dat  : -np 1 eat_filter_pdaf : -np 10 eat_model_gotm
```

or via a queue - please edit run.sbatch to reflect the type of run you are doing. We will need to maybe update run.sbatch to not use mpiexec - but srun.
```bash
sbatch run.sbatch
```

### Multiple GOTM-yaml files
```bash
cp eat_gotm.nml.org eat_gotm.nml
cp eat_pdaf.nml.org eat_pdaf.nml
```

Edit eat_gotm.nml and un-comment the line with shared_yaml_file

```bash
cp yaml_files_physics/gotm_????.yaml .
```

Ready to run.

First in pure ensemble mode:

```bash
mpiexec -np 10 eat_model_gotm
```
or via a queue

```bash
sbatch run.sbatch
```

Optionally view the difference:
```bash
pyncview result_0001.nc  result_0010.nc
```

Now in full DA model:

On the command line:
```bash
#mpiexec --oversubscribe -np 1 eat_obs_gotm.py --start "2016-01-01 12:00:00" --stop "2019-12-31 12:00:00" -o temp[-1] cci_sst.dat  : -np 1 eat_filter_pdaf : -np 10 eat_model_gotm 
mpiexec --oversubscribe -np 1 eat_obs_gotm.py --start "2016-01-01 12:00:00" --stop "2016-03-15 12:00:00" -o temp[-1] cci_sst.dat  : -np 1 eat_filter_pdaf : -np 10 eat_model_gotm
```

or via a queue

```bash
sbatch run.sbatch
```

Use multiplot to view ensemble:
```bash
multiplot -s "result_????.nc" -e "statistics(temp[:,:,57,0,0], 'obs')"
```


