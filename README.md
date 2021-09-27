You can use the Jupyter Notebooks in this repository with Binder:

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/BoldingBruggeman/seamless-notebooks/HEAD?urlpath=lab%2Ftree%2Fsetups)

# Staying up to date

To update this repository *including its submodules (FABM, ERSEM, PISCES, etc.)*, execute:

```
git pull --recurse-submodules
```

# Running on CINECA

First load required modules (you can put this in your `~/.bashrc` so you do not have to repeat this after every login):

```
module load anaconda3
```

Now obtain the repository with setups and scripts:

```
git clone --recursive https://github.com/BoldingBruggeman/seamless-notebooks.git
cd seamless-notebooks
conda env create -f environment.yml
conda activate seamless-bb
bash ./install
```
