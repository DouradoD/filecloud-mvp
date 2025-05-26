from services.guest.file import File
from services.guest.versioning import Versioning
import logging
from helpers.helpers import parse_xml_response

remote_fileclound_path = "/diogoaugustodourado"
file_name= "docx_for_test_file.docx"
full_remote_path = f"{remote_fileclound_path}/{file_name}"
file_path_to_upload = "static_data/v{version}/docx_for_test_file.docx"


def file_exists(config_and_login_session):
    config, session = config_and_login_session
    file = File(session=session, user_type=config['user_type'], base_url=config["base_url"])
    file_path = "/diogoaugustodourado/test.docx"
    response = file.file_exists(path=file_path)
    dict_response = parse_xml_response(response.text)
    assert dict_response['commands']['command']['result'] == '1'

def upload_file(file_session, remote_path, file_path):
    file_to_upload={'file': (open(file_path,'rb'))}
    params = {
        "appname": "explorer",
        "path": remote_path,
        "offset": 0
    }
    response = file_session.upload_file(params=params,files=file_to_upload)
    assert response.status_code == 200, "Failed to upload file"

def delete_file(file_session, remote_path, file_name):
    response = file_session.delete_file(path=remote_path, name=file_name)
    dict_response = parse_xml_response(response.text) 
    assert response.status_code == 200, "Failed to delete file"
    assert dict_response['commands']['command']['result'] == '1', "Failed to delete file"

def exists_file(file_session, full_remote_path):
    response = file_session.file_exists(path=full_remote_path)
    dict_response = parse_xml_response(response.text)
    assert response.status_code == 200, "Failed to check if file exists"
    assert 'result' in response.text, "Failed to check if file exists"
    return True if dict_response['commands']['command']['result'] == '1' else False

def asset_file_properties(entry, expected_name, expected_path, expected_type, expected_size, expected_dirpath, expected_extension):
    assert entry['name'] == expected_name, "File name does not match"
    assert entry['path'] == expected_path, "File path does not match"
    assert entry['type'] == expected_type, "File type does not match"
    assert entry['size'] == expected_size, "File size does not match"
    assert entry['dirpath'] == expected_dirpath, "File directory path does not match"
    assert entry['ext'] == expected_extension, "File extension does not match"


def test_file_workflow(config_and_login_session):
    config, session = config_and_login_session
    file_session = File(session=session, user_type=config['user_type'], base_url=config["base_url"])
    versioning_session = Versioning(session=session, user_type=config['user_type'], base_url=config["base_url"])

    # Check if the file exists before uploading
    if exists_file(file_session, full_remote_path):
        delete_file(file_session, remote_fileclound_path, file_name)
    else:
        logging.info(f"File {full_remote_path} does not exist.")

    # Upload the file
    upload_file(file_session, remote_fileclound_path,file_path_to_upload.format(version='1'))

    # Checking if the file exists after upload
    assert exists_file(file_session, full_remote_path)

    # Get file info
    response = file_session.get_file_info(params={"file": full_remote_path, "includeextrafields" : "1","includelockinfo": "1"})
    dict_response_v1 = parse_xml_response(response.text)
    assert response.status_code == 200, "Failed to get file info"
    dict_file_info_v1 = dict_response_v1['fileinfo']['entry']
    asset_file_properties(entry=dict_file_info_v1,
                          expected_name=file_name,
                          expected_path=full_remote_path,
                          expected_type='file',
                          expected_size='0 B',
                          expected_dirpath=remote_fileclound_path,
                          expected_extension='docx')


    # Update the file
    upload_file(file_session, remote_fileclound_path,file_path_to_upload.format(version='2'))

    # Check if the file exists after update
    assert exists_file(file_session, full_remote_path)

    # Get file info after update
    response = file_session.get_file_info(params={"file": full_remote_path, "includeextrafields" : "1","includelockinfo": "1"})
    dict_response_v2 = parse_xml_response(response.text)
    dict_file_info_v2 = dict_response_v2['fileinfo']['entry']
    # Assertions for file info after update
    asset_file_properties(entry=dict_file_info_v2,
                          expected_name=file_name,
                          expected_path=full_remote_path,
                          expected_type='file',
                          expected_size='4 KB',
                          expected_dirpath=remote_fileclound_path,
                          expected_extension='docx')

    v1_epoch = int(dict_file_info_v1['modifiedepoch'])
    v2_epoch = int(dict_file_info_v2['modifiedepoch'])

    assert v1_epoch < v2_epoch, "File was not updated: v1 is not older than v2"

    
    # Get versions of the file
    response_get_versions = versioning_session.get_versions(params={"filepath": remote_fileclound_path, "filename" : file_name})
    dict_response_get_versions = parse_xml_response(response_get_versions.text)
    dict_versions_info = dict_response_get_versions['versions']['version']
    assert response_get_versions.status_code == 200, "Failed to get file versions"
    assert int(dict_response_get_versions['versions']['meta']['total']) >= 2, "File versions count does not match"

    # Version 1 Validation
    v1_version = dict_versions_info[1]  # Older version comes second
    assert v1_version['versionnumber'] == 'Version 1', \
        f"Version 1 number mismatch: {v1_version['versionnumber']}"
    assert v1_version['size'] == dict_file_info_v1['size'], \
        f"Size mismatch: Version1={v1_version['size']}, FileInfoV1={dict_file_info_v1['size']}"
    assert v1_version['filename'] == dict_file_info_v1['name'], \
        "Filename mismatch in Version 1"
    assert v1_version['createdby'] == dict_file_info_v1.get('createdby', 'diogoaugustodourado'), \
        "Creator mismatch in Version 1"
    
    # Version 2 Validation
    v2_version = dict_versions_info[0]  # Newest version is first
    assert v2_version['versionnumber'] == 'Version 2', \
        f"Version 2 number mismatch: {v2_version['versionnumber']}"
    assert v2_version['size'] == dict_file_info_v2['size'], \
        f"Size mismatch: Version2={v2_version['size']}, FileInfoV2={dict_file_info_v2['size']}"
    
    # Cross-Version Checks
    assert v1_version['createdby'] == v2_version['createdby'], \
        "Creator should be the same for all versions"
    assert v1_version['date'] < v2_version['date'], \
        f"Version 1 date ({v1_version['date']}) should precede Version 2 ({v2_version['date']})"


