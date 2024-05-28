#!/bin/bash

# Init conda:
conda init && bash -i

# Create symbolic link for R environment between the two conda installations: 
sudo ln -s /work/miniconda3/envs/myenv /opt/conda/envs

# Activate environment:
conda activate myenv

python -m ipykernel install --user --name myenv --display-name "myenv"