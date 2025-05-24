from services.admin.user import User


def test_get_user(config_and_login):
    config, session = config_and_login
    user_type="admin"
    user = User(session=session, user_type=user_type, base_url=config["base_url"])
    user_name = "diogoaugustodourado"
    response = user.get_user(user_name)
    assert response is not None
    print(response)
    assert response["username"] == user_name

    
