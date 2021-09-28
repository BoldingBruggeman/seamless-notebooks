You can use the Jupyter Notebooks in this repository with Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/BoldingBruggeman/seamless-notebooks/HEAD?urlpath=lab%2Ftree%2Fsetups)

# Installing

You will need the [Anaconda Python distribution](https://www.anaconda.com/products/individual). On many systems that is already installed: try running `conda --version`.
If that fails, you may need to load an anaconda module first: try `module load anaconda` or `module load anaconda3`. If that still does not give you a working `conda` command,
you may want to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

Now make sure your conda environment is initialized:

```
conda init bash
```

This needs to be done just once, as it modifies your `.bashrc` that is sourced every time you login.

Now obtain the repository with setups and scripts:

```
git clone --recursive https://github.com/BoldingBruggeman/seamless-notebooks.git
cd seamless-notebooks
conda env create -f environment.yml
conda activate seamless-bb
bash ./install
```

# Staying up to date

To update this repository *including its submodules (FABM, ERSEM, PISCES, etc.)*, make sure you are in the `seamless-notebooks` directory and execute:

```
git pull --recurse-submodules
conda env update -f environment.yml
bash ./install
```

The last two commands update the conda (Python) environment and GOTM + pyfabm, respectively.
Depending on the changes in the repository, they may not be needed, but there is no harm in running them just in case - it just takes a little longer.

# Running a parallel sensitivity analysis

An example for a simple sensitivity analysis with GOTM-ERSEM for a Northern North Sea station is provided. To use this, first go to the `seamless-notebooks/parsac` directory.

To sample across parameter space, use:

```
parsac sensitivity sample northsea_sa.xml northsea_sa.pickle saltelli 64
```

To now run GOTM-ERSEM for all sampled parameter sets in parallel, use:

```
sbatch run.sbatch
```

NB this assumes you are on an HPC system that uses the SLURM job scheduler.

The above command submits a parallel job. It will report the identifier of the new job, e.g., "Submitted batch job 435384". Here, 435384 is the new job identifier (`<JOBID> ` below). You can monitor the job's progress with `squeue -u $USER`. After your job starts (status `ST` is `R`), you can monitor detailed progress with `tail -f <JOBID>.out`.

After the job completes, analyze your results and see sensitivity metrics with:

```
parsac sensitivity analyze northsea_sa.pickle sobol
```

To customize this for your own application:

* Most parsac settings are in an xml file. For the ERSEM North Sea example: `northsea_sa.xml`. To create your own, create a copy of this file under a new name.
* The parameters to perturb are listed under the `<parameters>` section in the xml file. Each entry includes the name where the parameter is set (`fabm.yaml` for biogeochemistry, `gotm.yaml` for hydrodynamics), the full path of the parameter in the file (e.g., `instances/P1/parameters/phim`), and the range of values the parameter can take, specified by its minimum and maximum.
* The target metrics for which sensitivity to parameters is to be assessed are listed under `<targets>`. Note that these metrics must be *scalar* values that computed in some way from the time- and depth-explicit GOTM result, e.g., by slicing at a particular time and depth, by averaging, taking the minimum or maximum, etc. You can add any numnber of targets.
* The method of sensitivity analysis is *not* set in the xml file, but on the command line as part of the `sample` step. For instance, in the above example `parsac sensitivity sample northsea_sa.xml northsea_sa.pickle saltelli 64` specifies the Saltelli sampling method. To get an overview of available methods, use `parsac sensitivity sample -h`. The methods corresponds to those provided by [SALib](https://salib.readthedocs.io/en/latest/index.html). Most will have additional settings that you can see with `parsac sensitivity sample <XMLFILE> <PICKLEFILE> <METHOD> -h`, for instance, `parsac sensitivity sample northsea_sa.xml northsea_sa.pickle saltelli -h`. For more information about each setting, see the SALib documentation.
* Likewise, the analysis method is specified on the command line as part of the `analyze` step. To see available methods, use `parsac sensitivity analyze -h`. As for the `sample` step, an analysis step may have additional arguments that you can see with `parsac sensitivity analyze <PICKLEFILE> <METHOD> -h`. *Note: in most cases, a particular analysis method needs to be combined with a specific sampling method, e.g., sampling with saltelli, analysis with sobol. See the SALib documentation.

# Running on CINECA

The Anaconda Python distribution is already installed and can be loaded with:

```
module load anaconda3
```
