import yaml
import os

class Config:
    def __init__(self, config_file=None):
        self.config = {}
        # Load default config
        default_config_path = os.path.join(os.path.dirname(__file__), '..', 'configs', 'default.yaml')
        with open(default_config_path, 'r') as f:
            self.config.update(yaml.safe_load(f))
        
        # Load user config if provided
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                user_config = yaml.safe_load(f)
                self.config.update(user_config)
    
    def get(self, key, default=None):
        return self.config.get(key, default)