"""Configuration loading utilities"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any


def load_config(config_path: str) -> Dict[str, Any]:
    """Load configuration from JSON or YAML file"""
    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    if path.suffix == ".json":
        with open(path, "r") as f:
            return json.load(f)
    elif path.suffix in [".yaml", ".yml"]:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    else:
        raise ValueError(f"Unsupported config file format: {path.suffix}")


def save_config(config: Dict[str, Any], config_path: str) -> None:
    """Save configuration to JSON or YAML file"""
    path = Path(config_path)

    if path.suffix == ".json":
        with open(path, "w") as f:
            json.dump(config, f, indent=2)
    elif path.suffix in [".yaml", ".yml"]:
        with open(path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)
    else:
        raise ValueError(f"Unsupported config file format: {path.suffix}")
