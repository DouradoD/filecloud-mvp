from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader
class User(BaseService):

    def __init__(self, session, user_type: str, base_url: str):
        super().__init__(session, base_url)
        self.admin_service_info = EndpointsLoader(user_type).get_endpoints()
        self.endpoint = self.admin_service_info['default_endpoint']
        self.user_service = self.admin_service_info['user']

    def add_new_user(self, user_data: dict):
        """
        Add a new user.
        :param
        endpoint: API endpoint for adding a user. 
        user_data: Dictionary containing user data.
        :return: Response from the server.
        """
        operation = self.user_service['add_user']['operation']
        params = {**{"op": operation}, **user_data}
        return self.post(endpoint=self.endpoint, params=params)
        
    def get_user(self, user_id: str):
        """
        Get user details.
        :param user_id: ID of the user to retrieve.
        :return: Response from the server.
        """
        operation = self.user_service['get_user']['operation']
        return self.post(endpoint=self.endpoint, params={"op": operation,"username": user_id})