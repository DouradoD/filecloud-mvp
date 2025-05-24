import pytest
import requests
from helpers.config_load import ConfigLoader
from services.admin.login import Login


@pytest.fixture(scope="session")
def config_and_login_session():
    session = requests.session()
    config_loader = ConfigLoader("prod")
    config = config_loader.get_config()
    config['user_type'] = "admin"
    response = Login(session, config['user_type'], config["base_url"]
                     ).admin_login(username=config["userid"], password=config["password"]
                         ,headers={'Accept': 'application/json'})

    assert response.status_code == 200
    assert response.json()['command'][0]['result'] == 1
    yield config, session
    