from .main import cli
from .experiment import experiment

# Add experiment commands to main CLI
cli.add_command(experiment)

__all__ = ["cli"]