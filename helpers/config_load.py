import yaml
import os

class ConfigLoader:
    def __init__(self, env):
        self.config_path = f'config/{env}.yaml'
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)

        return config

    def get_config(self):
        return self.config