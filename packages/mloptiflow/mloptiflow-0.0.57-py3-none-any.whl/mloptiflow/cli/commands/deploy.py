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

        if kafka_monitoring:
            config.enable_monitoring()

        if containerized_api:
            config.enable_docker()
            config.setup()
            click.echo("Starting containerized deployment...")
            subprocess.run(
                [
                    "docker",
                    "compose",
                    "-f",
                    str(config.deployment_path / "docker-compose.yml"),
                    "up",
                    "-d",
                ]
            )
            return

        api_process = subprocess.Popen(
            [sys.executable, str(api_script)],
            env={**os.environ, "HOST": host, "PORT": str(port)},
        )

        click.echo(f"API server starting at http://{host}:{port}")
        click.echo("Documentation available at http://localhost:8000/docs")

        if with_api_test:
            if not api_test_script.exists():
                click.echo(
                    "Warning: test_inference_api.py not found, skipping inference API testing"
                )
            else:
                time.sleep(2)
                click.echo("\nStarting inference API testing...")
                api_test_process = subprocess.Popen(
                    [sys.executable, str(api_test_script)]
                )

        def signal_handler(signum, frame):
            click.echo("\nShutting down gracefully...")
            if with_api_test and "api_test_process" in locals():
                api_test_process.terminate()
            api_process.terminate()
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        api_process.wait()

    except Exception as e:
        raise click.ClickException(str(e))
