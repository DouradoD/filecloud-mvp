from services.guest.file import File

def test_get_file_list(config_and_login_session):
    config, session = config_and_login_session
    file = File(session=session, user_type=config['user_type'], base_url=config["base_url"])
    response = file.get_file_list()
    assert response is not None
    assert response.status_code == 200
    assert response.text is not None

def test_file_exists(config_and_login_session):
    config, session = config_and_login_session
    file = File(session=session, user_type=config['user_type'], base_url=config["base_url"])
    path = "/diogoaugustodourado/My Files"
    response = file.file_exists(path=path)
    assert response is not None

def test_get_file_info(config_and_login_session):
    config, session = config_and_login_session
    file = File(session=session, user_type=config['user_type'], base_url=config["base_url"])
    path = "/diogoaugustodourado/My Files"
    response = file.get_file_info(path=path)
    assert response is not None
    assert response.status_code == 200

def test_download_file(config_and_login_session):
    config, session = config_and_login_session
    file = File(session=session, user_type=config['user_type'], base_url=config["base_url"])
    params = {
        "filepath": "/diogoaugustodourado/My Files/FileCloud Admin Dashboard.png",
        "filename": "FileCloud Admin Dashboard.png",
        "checkonly": 1,
    }
    response = file.download_file(params=params)
    assert response is not None
    assert response.status_code == 200

def test_upload_file(config_and_login_session):
    config, session = config_and_login_session
    file_client = File(session, user_type=config['user_type'], base_url=config["base_url"])
    file_to_upload={'file': (open('tests/guest/test.docx','rb'))}

    params = {
        "appname": "explorer",
        "path": "/diogoaugustodourado",
        "offset": 0
    }
    
    response = file_client.upload_file(
        params=params,
        files=file_to_upload,
    )
    
    assert response is not None
    assert response.status_code == 200