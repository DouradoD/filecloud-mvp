from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Versioning(BaseService):

    def __init__(self, session, user_type, base_url: str):
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()["versioning"]

    def get_versions(self, params:dict):
        return self.post(self.endpoints["get_versions"],
                         params=params)