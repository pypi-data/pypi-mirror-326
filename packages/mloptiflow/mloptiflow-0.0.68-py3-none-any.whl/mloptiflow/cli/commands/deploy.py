import click
import subprocess
import sys
import os
from pathlib import Path
import signal
import time
from mloptiflow.deployment.config import DeploymentConfig


@click.group()
def deploy():
    """Deploy and test ML models."""
    pass


def _run_api_tests(test_script: Path):
    """Helper to run API tests"""
    if not test_script.exists():
        raise click.ClickException("API test script not found")
    subprocess.run([sys.executable, str(test_script)], check=True)


@deploy.command()
@click.option(
    "--kafka-monitoring", is_flag=True, help="Enable Kafka-based model monitoring"
)
@click.option("--containerized-api", is_flag=True, help="Run API in Docker container")
@click.option("--host", default="0.0.0.0", help="Host to bind the API server")
@click.option("--port", default=8000, type=int, help="Port to bind the API server")
@click.option("--with-api-test", is_flag=True, help="Run inference API testing script")
def start(
    kafka_monitoring: bool,
    containerized_api: bool,
    host: str,
    port: int,
    with_api_test: bool,
):
    """Start the model deployment"""
    try:
        config = DeploymentConfig(os.getcwd())
        cwd = Path.cwd()
        api_script = cwd / "app.py"
        api_test_script = cwd / "scripts" / "test_inference_api.py"

        if not api_script.exists():
            raise click.ClickException("app.py not found. Are you in the project root?")

        if containerized_api:
            click.echo("Building container image...")
            subprocess.run(
                [
                    "docker",
                    "build",
                    "-t",
                    "mloptiflow-api",
                    "-f",
                    str(config.deployment_path / "Dockerfile.api"),
                    ".",
                ],
                check=True,
            )

            docker_cmd = [
                "docker",
                "run",
                "-d",
                "-p",
                f"{port}:8000",
                "-v",
                f"{cwd}/mlruns:/app/mlruns",
                "-e",
                "MLFLOW_TRACKING_URI=file:///app/mlruns",
            ]

            if kafka_monitoring:
                docker_cmd += ["--network=host", "-e", "KAFKA_BROKERS=localhost:9092"]

            docker_cmd += ["mloptiflow-api"]

            click.echo("Starting containerized API...")
            subprocess.run(docker_cmd, check=True)

            if with_api_test:
                time.sleep(2)
                _run_api_tests(api_test_script)

            return

        if kafka_monitoring:
            config.enable_monitoring()

        api_process = subprocess.Popen(
            [sys.executable, str(api_script)],
            env={**os.environ, "HOST": host, "PORT": str(port)},
        )

        click.echo(f"API server starting at http://{host}:{port}")

        if with_api_test:
            api_test_process = subprocess.Popen([sys.executable, str(api_test_script)])

        def signal_handler(signum, frame):
            click.echo("\nShutting down gracefully...")
            if with_api_test:
                api_test_process.terminate()
            api_process.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        api_process.wait()

    except Exception as e:
        raise click.ClickException(str(e))
