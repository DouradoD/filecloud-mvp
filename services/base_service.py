import requests

class BaseService:
    def __init__(self, session, base_url: str):
        self.base_url = base_url
        self.session = session

  
    def get(self, endpoint: str, cookies: dict = None, headers:dict = None, params: dict = None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, cookies=cookies, headers=headers, params=params)
        return response

    def post(self, endpoint: str, files=None, cookies: dict = None, headers: str = None, params: dict = None ,data: dict = None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url,cookies=cookies, headers=headers, params=params, files=files)
        return response
    
    def put(self, endpoint: str, data: dict = None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url, data=data)
        return response
    
    def delete(self, endpoint: str):
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url)
        return response
