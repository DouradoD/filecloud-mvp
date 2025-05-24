

def test_get_user(config_and_login_session):
    config, login_response = config_and_login_session
    user_type="admin"
    """"
    user = User(user_type=user_type, base_url=config["base_url"][user_type])
    user_name = "diogoaugustodourado"
    response = user.get_user(user_name, cookies=login_response.cookies).json()
    assert response is not None
    print(response)
    assert response["username"] == user_name
    """
