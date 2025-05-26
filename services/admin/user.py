from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class User(BaseService):
    """
    Service for admin user management operations in FileCloud.
    """

    def __init__(self, session, user_type, base_url: str):
        """
        Initialize the User service.
        """
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()["user"]

    def get_user(self, username: str):
        """
        Retrieve a user's details by username.
        """
        return self.get(self.endpoints["get_user"], params={"username": username})

    def add_new_user(self, user_data: dict):
        """
        Add a new user to FileCloud.
        """
        return self.post(self.endpoints["add_new_user"], data=user_data)