import os
import yaml
from typing import Dict, Any


class ServerConfig:
    """Configuration for the server."""
    
    def __init__(self, config_data: Dict[str, Any]):
        self.host = config_data.get('host', '127.0.0.1')
        self.port = config_data.get('port', 8080)
        self.log_level = config_data.get('log_level', 'info')
        self.data_dir = config_data.get('data_dir', './data')
        self.max_concurrent = config_data.get('max_concurrent', 10)
        self.request_timeout = config_data.get('request_timeout', 30)


def load_config(config_file: str) -> ServerConfig:
    """Load configuration from a YAML file."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found: {config_file}")
    
    with open(config_file, 'r') as f:
        config_data = yaml.safe_load(f)
    
    return ServerConfig(config_data or {})
