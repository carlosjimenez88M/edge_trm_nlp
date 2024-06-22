#!/bin/bash

# Configuración del entorno Conda
source /Users/danieljimenez/opt/anaconda3/etc/profile.d/conda.sh
conda activate edge_trm_nlp

# Establecer la variable de entorno HYDRA_FULL_ERROR
export HYDRA_FULL_ERROR=1

# Ejecutar mlflow run con una ruta absoluta
mlflow run .