import yaml
import os

class EndpointsLoader:
    def __init__(self, user_type:str):
        self.user_type = user_type
        self.endpoint_file_path = f'config/endpoints.yaml'
        self.endpoints = self.load_endpoints()

    def load_endpoints(self):
        if not os.path.exists(self.endpoint_file_path):
            raise FileNotFoundError(f"Endpoints file not found: {self.endpoint_file_path}")

        with open(self.endpoint_file_path, 'r') as file:
            endpoints = yaml.safe_load(file)

        return endpoints

    def get_endpoints(self):
        return self.endpoints[self.user_type]