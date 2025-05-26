from services.admin.group import Group
from helpers.helpers import parse_xml_response

def test_get_groups(config_and_login_session):
    """
    Test the get_groups method of the Group service.
    """
    config, session = config_and_login_session
    group_service = Group(session, config['user_type'], config['base_url'])
    response = group_service.get_groups()
    dict_response = parse_xml_response(response.text)

    
    assert response.status_code == 200
    assert dict_response['groups']['meta']['total'] is not None

def test_get_group_by_name(config_and_login_session):
    """
    Test the get_group_by_name method of the Group service.
    """
    config, session = config_and_login_session
    group_service = Group(session, config['user_type'], config['base_url'])
    
    # Assuming 'test_group' is a valid group name in the system
    group_name = "Accounting"
    response = group_service.get_group_by_name(group_name)
    dict_response = parse_xml_response(response.text)

    assert response.status_code == 200
    assert dict_response['groups']['group']['groupname'] == group_name
