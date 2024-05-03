#!/bin/bash

# Create symbolic link for R environment between the two conda installations: 
sudo ln -s /work/miniconda3/bin/conda /usr/bin/conda

# Init conda:
conda init && bash -i

# Activate environment:
conda activate myenv
