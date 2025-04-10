#!/usr/bin/env bash

# Create a Python 3.10 environment using Miniconda
MINICONDA_INSTALLER=Miniconda3-py310_23.3.1-0-Linux-x86_64.sh

wget https://repo.anaconda.com/miniconda/$MINICONDA_INSTALLER
bash $MINICONDA_INSTALLER -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"

conda init bash
source ~/.bashrc
conda create -y -n myenv python=3.10
source activate myenv

pip install -r requirements.txt