import os
import yaml
from typing import Dict, Any

def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Expand environment variables
    def expand_env_vars(item):
        if isinstance(item, str) and item.startswith("${") and item.endswith("}"):
            env_var = item[2:-1]
            return os.getenv(env_var)
        return item

    def process_dict(d):
        for k, v in d.items():
            if isinstance(v, dict):
                process_dict(v)
            elif isinstance(v, str):
                d[k] = expand_env_vars(v)
    
    process_dict(config)
    return config
