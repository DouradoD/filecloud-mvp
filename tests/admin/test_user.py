from services.admin.user import User
import logging
logging.basicConfig(level=logging.WARNING)


def test_get_user(config_and_login_session):
    config, session = config_and_login_session
    user = User(session=session, user_type=config['user_type'], base_url=config["base_url"])
    user_name = "diogoaugustodourado"
    response = user.get_user(user_name)
    assert response.status_code == 200
    assert '<username>diogoaugustodourado</username>' in response.text
    assert '<email>diogo.augusto.dourado@gmail.com</email>' in response.text

def test_add_new_user(config_and_login_session):
    config, session = config_and_login_session
    user = User(session=session, user_type=config['user_type'], base_url=config["base_url"])
    params = {"username": "John Doe","displayname":"John Doe", "email":"john_doe@gmail.com", "password": "John$Doe", "authtype":"0","status":1}
    response = user.add_new_user(user_data=params)
    if 'Username already exists and is not available' in response.text:
        logging.warning("User already exists, skipping test.\n" \
        f"user info: {params}")
        pass
    else:
        assert response.status_code == 200
        assert '<result>1</result>' in response.text
        assert response.reason == "OK"


    
