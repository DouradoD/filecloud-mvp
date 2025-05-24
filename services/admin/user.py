from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader
class User(BaseService):

    def __init__(self, session, user_type: str, base_url: str):
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type, "user").get_endpoints()

    def add_new_user(self, user_data: dict):
        """
        Add a new user.
        :param
        endpoint: API endpoint for adding a user. 
        user_data: Dictionary containing user data.
        :return: Response from the server.
        """
        return self.post(data=user_data)
    
    def get_user(self, user_id: str):
        """
        Get user details.
        :param user_id: ID of the user to retrieve.
        :return: Response from the server.
        """
        operation = self.endpoints['get_user']['operation']
        return self.get(endpoint=self.endpoints["base_endpoint"], params={"op": operation,"username": user_id})