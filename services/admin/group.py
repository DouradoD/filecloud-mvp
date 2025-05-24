from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Group(BaseService):
    """
    Group service for managing user groups.
    """

    def __init__(self, session, user_type, base_url: str):
        super().__init__(session, base_url)
        self.admin_service_info = EndpointsLoader(user_type).get_endpoints()
        self.endpoint = self.admin_service_info['default_endpoint']
        self.group_service = self.admin_service_info['group']

    def add_new_group(self, group_name: str):
        """
        Add a new group.
        :param group_data: Dictionary containing group data.
        :return: Response from the server.
        """
        operation = self.group_service['add_group']['operation']
        params = {"op": operation, "groupname": 'TestingCreateGroup'}
        return self.post(endpoint=self.endpoint, params=params)
    
    def get_groups(self):
        """
        Get group details
        :return: Response from the server.
        """
        operation = self.group_service['get_groups']['operation']
        return self.get(endpoint=self.endpoint, params={"op": operation})