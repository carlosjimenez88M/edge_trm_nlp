import mlflow
import os
import hydra
from omegaconf import DictConfig
import subprocess
import logging
from time import sleep

# Logger Configuration ---------------
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(log_dir, 'main.log'),
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()


def clean_conda_envs():
    try:
        # List conda environments
        envs_output = subprocess.check_output(["conda", "env", "list"]).decode("utf-8")
        env_lines = envs_output.split("\n")
        for i in env_lines:
            print(i)

        logger.info("Conda environments listed successfully.")

        # Identify mlflow environments
        mlflow_envs = [line.split()[0].strip() for line in env_lines if "mlflow-" in line]
        current_env = [line.split()[0].strip() for line in env_lines if '*' in line]

        logger.info(f"Identified mlflow environments: {mlflow_envs}")

        # Remove mlflow environments, except edge_trm_nlp
        for env in mlflow_envs:
            if env == "edge_trm_nlp":
                logger.info(f"Skipping removal of protected environment: {env}")
                continue

            if env in current_env:
                logger.info(f"Skipping removal of current active environment: {env}")
                continue

            try:
                logger.info(f"Attempting to remove conda environment: {env}")
                if os.path.exists(env):
                    subprocess.check_call(["conda", "env", "remove", "-p", env, "--yes"])
                else:
                    subprocess.check_call(["conda", "env", "remove", "--name", env, "--yes"])
                logger.info(f"Removed conda environment: {env}")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to remove conda environment: {env}. Error: {e}")
    except Exception as e:
        logger.error(f"Error while listing conda environments: {e}")


@hydra.main(config_path=".", config_name='config', version_base=None)
def go(config: DictConfig):
    root_path = hydra.utils.get_original_cwd()

    _ = mlflow.run(
        f"file://{os.path.join(root_path, 'Pipeline/download_information')}",
        "main",
        parameters={
            "timezone": config["data"]["timezone"],
            "url_news": config["data"]["url_news"],
            "save_directory": config["data"]["save_directory"],
            "artifact_name": "News_Scraping"
        },
    )

    _ = mlflow.run(
        f"file://{os.path.join(root_path, 'Pipeline/download_information')}",
        "dolar",
        parameters={
            "url_dolar": config["data"]["url_dolar"],
            "save_directory": config["data"]["save_directory"],
        },
    )

    clean_conda_envs()


if __name__ == "__main__":
    go()