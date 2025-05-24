from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Login(BaseService):

    def __init__(self, session, user_type: str, base_url: str):
        super().__init__(session, base_url)
        self.admin_service_info = EndpointsLoader(user_type).get_endpoints()
        self.endpoint = self.admin_service_info['default_endpoint']
        self.login_service = self.admin_service_info['login']
    
    def admin_login(self, username: str, password: str, headers: dict):
        operation = self.login_service['login']['operation']
        return self.post(self.endpoint, 
                         params={"op": operation,"adminuser": username, "adminpassword": password}, 
                         headers=headers)
    
    def admin_logout(self):
        operation = self.login_service['logout']['operation']
        return self.post(self.endpoint, params={"op": operation})
    