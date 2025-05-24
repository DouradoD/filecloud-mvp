from services.admin.group import Group
import xmltodict

def test_get_groups(config_and_login_session):
    """
    Test the get_groups method of the Group service.
    """
    config, session = config_and_login_session
    group_service = Group(session, config['user_type'], config['base_url'])
    response = group_service.get_groups()
    dict_response = xmltodict.parse(response.text)

    
    assert response.status_code == 200
    assert dict_response['groups']['meta']['total'] is not None
