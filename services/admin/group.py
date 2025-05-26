from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class Group(BaseService):
    """
    Service for admin group management operations in FileCloud.
    """

    def __init__(self, session, user_type, base_url: str):
        """
        Initialize the Group service.
        """
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()["group"]

    def get_groups(self):
        """
        Retrieve all groups.
        """
        return self.get(self.endpoints["get_groups"])

    def get_group_by_name(self, group_name: str):
        """
        Retrieve a group's details by name.
        """
        return self.get(self.endpoints["get_group_by_name"], params={"groupname": group_name})

    def add_new_group(self, group_name: str):
        """
        Add a new group to FileCloud.
        """
        return self.post(self.endpoints["add_new_group"], data={"groupname": group_name})