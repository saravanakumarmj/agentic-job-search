
"""Load and validate environment-specific application configuration."""

import os
import tomllib
from pathlib import Path
from typing import Any

from dotenv import load_dotenv



# Project root: one level above the job_search package.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Load environment variables from the project root .env file.
load_dotenv(PROJECT_ROOT / ".env")

# Supported application environments.
VALID_ENVIRONMENTS = {"dev", "staging", "prod"}


def get_environment() -> str:
    """Read and validate the active environment."""

    environment = os.getenv("APP_ENV", "dev").strip().lower()

    if environment not in VALID_ENVIRONMENTS:
        raise ValueError(
            f"Invalid APP_ENV: {environment}. "
            f"Choose one of: {', '.join(sorted(VALID_ENVIRONMENTS))}"
        )

    return environment


def load_config() -> dict[str, Any]:
    """Load the TOML configuration for the active environment."""

    environment = get_environment()

    config_path = (
        PROJECT_ROOT
        / "config"
        / "environments"
        / f"{environment}.toml"
    )

    if not config_path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )

    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file)

    # Verify that the configuration matches the active environment.
    configured_environment = config.get("app", {}).get("environment")

    if configured_environment != environment:
        raise ValueError(
            f"Environment mismatch: APP_ENV={environment}, "
            f"but configuration specifies {configured_environment}"
        )

    # Validate required configuration sections.
    required_sections = ["app", "database", "resume", "job_search"]

    for section in required_sections:
        if section not in config:
            raise ValueError(f"Missing configuration section: {section}")

    # Resolve resume path relative to project root.
    resume_path = Path(config["resume"]["path"])

    if not resume_path.is_absolute():
        config["resume"]["path"] = str(PROJECT_ROOT / resume_path)

    return config
