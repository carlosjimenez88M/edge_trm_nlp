#!/bin/bash

if [ -f "/Users/danieljimenez/opt/anaconda3/etc/profile.d/conda.sh" ]; then
    source /Users/danieljimenez/opt/anaconda3/etc/profile.d/conda.sh
else
    source ~/conda/etc/profile.d/conda.sh
fi

conda activate edge_trm_nlp


export HYDRA_FULL_ERROR=1


mlflow run .
