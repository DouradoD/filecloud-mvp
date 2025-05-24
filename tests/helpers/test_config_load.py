from helpers.config_load import ConfigLoader


def test_config_load():
    config_loader = ConfigLoader("test")
    config = config_loader.get_config()
    assert config is not None
    assert config["base_url"] == "https://api.example.com"
    assert config["userid"] == "userid"
    assert config["password"] == "password"
    assert config['headers']['Accept'] == "application/json"
