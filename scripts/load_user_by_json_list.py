from services.admin.group import Group


def read_json_file(file_path):
    """
    Reads a JSON file and returns the data.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_groups(session, config):
    group_service = Group(session, config['user_type'], config['base_url'])
    response = group_service.get_groups()
    group_list = []
    list_of_the_groups_to_be_created = []
    for group in group_list:
        if f'<groupname>{group}</groupname>' not in response.text:
            list_of_the_groups_to_be_created.append(group)

    for group in list_of_the_groups_to_be_created:
        response = group_service.create_group(group)
        if response.status_code == 200:
            print(f"Group {group} created successfully.")
        else:
            print(f"Failed to create group {group}. Status code: {response.status_code}")