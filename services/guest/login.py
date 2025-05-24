from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Login(BaseService):

    def __init__(self, session, user_type, base_url: str):
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()["login"]
    
    def admin_login(self, username: str, password: str, headers: dict):
        return self.post(self.endpoints["login"], 
                         params={'userid': username, 'password': password} , 
                         headers=headers)
    
    def admin_logout(self):
        return self.post(self.endpoints["logout"])
    