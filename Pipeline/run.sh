#!/bin/bash
source /Users/danieljimenez/opt/anaconda3/etc/profile.d/conda.sh
conda activate edge_trm_nlp
export HYDRA_FULL_ERROR=1
mlflow run /Users/danieljimenez/Documents/Projects/Personal_Projects/edge_trm_nlp/Pipeline
