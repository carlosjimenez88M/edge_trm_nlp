#!/bin/bash

# Asegúrate de que este script se ejecute en el entorno correcto
if [ -f "/Users/danieljimenez/opt/anaconda3/etc/profile.d/conda.sh" ]; then
    source /Users/danieljimenez/opt/anaconda3/etc/profile.d/conda.sh
else
    source ~/conda/etc/profile.d/conda.sh
fi

conda activate edge_trm_nlp

# Establecer la variable de entorno HYDRA_FULL_ERROR
export HYDRA_FULL_ERROR=1

# Ejecutar mlflow run con una ruta relativa
mlflow run .
