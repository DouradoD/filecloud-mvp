from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Login(BaseService):

    def __init__(self, session, user_type: str, base_url: str):
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type, "login").get_endpoints()
    
    def admin_login(self, username: str, password: str, headers: dict):
        operation = self.endpoints['login']['operation']
        return self.post(self.endpoints["base_endpoint"], 
                         params={"op": operation,"adminuser": username, "adminpassword": password}, 
                         headers=headers)
    
    def admin_logout(self):
        operation = self.endpoints['logout']['operation']
        return self.post(self.endpoints["base_endpoint"], params={"op": operation})
    