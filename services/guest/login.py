from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Login(BaseService):
    """
    Service for guest user login operations in FileCloud.
    """

    def __init__(self, session, user_type, base_url: str):
        """
        Initialize the Login service.
        """
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()["login"]

    def admin_login(self, username: str, password: str, headers: dict):
        """
        Log in as a guest user.
        """
        data = {"userid": username, "password": password}
        return self.post(self.endpoints["admin_login"], data=data, headers=headers)

    def admin_logout(self):
        """
        Log out the current guest user session.
        """
        return self.post(self.endpoints["admin_logout"])