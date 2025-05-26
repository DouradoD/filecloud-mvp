from services.admin.group import Group
from services.admin.user import User
from services.admin.login import Login
from helpers.helpers import read_json_file, parse_xml_response
from helpers.config_load import ConfigLoader
import logging
import requests
import copy

def get_user_id(session, user_data):
    # Get the user id from the user service
    user_service = User(session, config['user_type'], config["base_url"])
    user_service_response = user_service.get_user(user_data['username'])
    if user_service_response.status_code == 200:
        user_id = parse_xml_response(user_service_response.text)['users']['user']['username']
        return user_id
    else:
        logging.warning(f"User {user_data['username']} not found, skipping test.\n" \
                        f"user info: {user_data}")
        return None

def get_group_id(session, group_name):
    # Get the group id from the user service
    group_service = Group(session, config['user_type'], config['base_url'])
    group_service_response = group_service.get_group_by_name(group_name)
    if group_service_response.status_code == 200:
        group_id = parse_xml_response(group_service_response.text)['groups']['group']['groupid']
        return group_id
    else:
        logging.warning(f"Group {group_name} not found, skipping test.\n" \
                        f"group name: {group_name}")
        return None

def create_groups(session, config, group_list):
    # Create groups in the system based on a JSON file.
    group_service = Group(session, config['user_type'], config['base_url'])
    response = group_service.get_groups()
    list_of_the_groups_to_be_created = []
    # Check if the groups already exist in the system
    # and add them to the list of groups to be created if they don't.
    for group in group_list:
        if f'<groupname>{group}</groupname>' not in response.text:
            list_of_the_groups_to_be_created.append(group)
    # Create the groups in the system
    # and print the status of each creation.
    for group in list_of_the_groups_to_be_created:
        response = group_service.add_new_group(group)
        if response.status_code == 200:
            logging.info(f"Group {group} created successfully.")
        else:
            logging.warning(f"Failed to create group {group}. Status code: {response.status_code}, status text: {response.text}")

def add_users(session, config, user_list):
    # Creating a deep copy to not affect the original list
    user_list_copy = copy.deepcopy(user_list)
    # Read the JSON file containing the list of users to be added.
    user_service = User(session=session, user_type=config['user_type'], base_url=config["base_url"])
    for user_data in user_list_copy:
        # Remove the 'groups' key from the user dictionary
        user_data.pop('groups', None)
        # Add users to the system based on a JSON file.
        print(f"Adding user {user_data['username']} to the system.")
        response = user_service.add_new_user(user_data=user_data)
        # Check if the user already exists in the system
        # and skip the test if it does.
        # Otherwise, assert the response status code and reason.
        if response.status_code == 200:
            logging.info(f"User {user_data['username']} created successfully.")
        elif response.status_code == 400:
            xml_response = parse_xml_response(response.text)
            logging.warning(f"User not added, maybe this user is already in the sistem!\n"
                            f"User not added, because: {xml_response['commands']['command']['message']}\n" \
                            f"user info: {user_data}")
        else:
            logging.warning(f"Error to add this user: {user_data}\n Response text: {response.text}, status code: {response.status_code}")

def add_members_to_the_groups(session, config, user_list):
    # Get the list of users to be added to the groups
    group_service = Group(session, config['user_type'], config['base_url'])
    for user_data in user_list:
        # Get user id from user service
        user_name = get_user_id(session, user_data)
        for group in user_data['groups']:
            # Get the group id from the user service
            group_id = get_group_id(session, group)
            # Add member to the group
            response = group_service.add_member_to_group(group_id=group_id, user_id=user_name)
            # Check if the user is already a member of the group
            if response.status_code == 200:
                logging.info(f"User {user_data['username']} added to group {group} successfully.")
            elif response.status_code == 400:
                logging.warning(f"User is already a member of the group. username: {user_name} and groupid: {group_id}")
            else:
                logging.warning(f"Error to add this user: {user_data}\n Response text: {response.text}")

def login():
    session = requests.session()
    config_loader = ConfigLoader("prod")
    config = config_loader.get_config()
    config['user_type'] = "admin"
    response = Login(session, config['user_type'], config["base_url"]
                     ).admin_login(username=config["userid"], password=config["password"]
                         ,headers={'Accept': 'application/json'})

    assert response.status_code == 200
    if not response.json()['command'][0]['result'] == 1:
        raise Exception("Login failed!")
    return config, session

if __name__ == "__main__":
    # Load the JSON file containing the list of users and groups
    json_file_path = 'static_data/new_users.json'
    json_data = read_json_file(json_file_path)
    # Login to the system
    # and create groups and users based on the JSON file.
    config, session = login()
    create_groups(session, config, group_list=json_data['groups'])
    add_users(session, config, user_list=json_data['users'])
    add_members_to_the_groups(session, config, user_list=json_data['users'])

