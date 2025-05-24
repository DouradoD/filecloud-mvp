from services.base_service import BaseService

class Group(BaseService):
    """
    Group service for managing user groups.
    """

    def __init__(self, base_url: str):
        super().__init__(base_url)

    def add_new_group(self, group_data: dict):
        """
        Add a new group.
        :param group_data: Dictionary containing group data.
        :return: Response from the server.
        """
        return self.post(data=group_data)
    
    def get_groups(self):
        """
        Get group details by group ID.
        :param group_id: ID of the group to retrieve.
        :return: Response from the server.
        """
        return self.get(endpoint="TBD")