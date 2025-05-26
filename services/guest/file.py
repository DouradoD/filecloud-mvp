from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class File(BaseService):

    def __init__(self, session, user_type, base_url: str):
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type).get_endpoints()[ "file"]
    
    def file_exists(self, path:str , headers: dict = None):
        return self.post(self.endpoints["file_exists"], 
                        params={"file": path},
                        headers=headers)
    def upload_file(self, params:dict, files:dict=None):
        return self.post(self.endpoints["upload_file"],
                         files=files,
                         params=params)
    
    def get_file_info(self, params:dict, cookies: dict = None, headers: dict = None):
        return self.post(self.endpoints["get_file_info"],
                         params=params,
                         cookies=cookies,
                         headers=headers)
    def delete_file(self, path:str, name:str):
        return self.post(self.endpoints["delete_file"],
                         params={"path": path,
                                 "name": name})
    