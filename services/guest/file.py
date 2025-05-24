from services.base_service import BaseService
from helpers.endpoints_load import EndpointsLoader

class File(BaseService):

    def __init__(self, session, user_type, base_url: str):
        super().__init__(session, base_url)
        self.endpoints = EndpointsLoader(user_type, "file").get_endpoints()
    
    def create_folder(self, path:str , headers: dict):
        return self.post(self.endpoints["create_folder"], 
                         params={"path": path}, 
                         headers=headers)
    def file_exists(self, path:str , headers: dict = None):
        return self.post(self.endpoints["file_exists"], 
                        params={"path": path},
                        headers=headers)
    def get_file_list(self, path:str = None, cookies: dict = None, headers: dict = None):
        return self.post(self.endpoints["get_file_list"],
                        params={"path": path},
                        cookies=cookies, 
                        headers=headers)
    def upload_file(self, params:dict, files:dict=None):
        return self.post(self.endpoints["upload_file"],
                         files=files,
                         params=params)
    
    def get_file_info(self, path:str, cookies: dict = None, headers: dict = None):
        return self.post(self.endpoints["get_file_info"],
                         params={"path": path},
                         cookies=cookies,
                         headers=headers)
    def download_file(self, params, cookies: dict = None, headers: dict = None):
        return self.get(self.endpoints["download_file"],
                         params=params,
                         cookies=cookies,
                         headers=headers)