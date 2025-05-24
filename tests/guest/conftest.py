import pytest
import requests

from helpers.config_load import ConfigLoader
from services.guest.login import Login


@pytest.fixture(scope="session")
def config_and_login():
    session = requests.session()
    config_loader = ConfigLoader("prod")
    config = config_loader.get_config()
    config['user_type'] = "guest"
    response = Login(session, "guest", config["base_url"]
                           ).admin_login(config["userid"], 
                                         config["password"],
                                         headers={'Accept': 'application/json'})
    assert response.status_code == 200
    assert response.json()['command'][0]['result'] == 1
    yield config, session
    