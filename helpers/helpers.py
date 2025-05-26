import json
import xmltodict


def read_json_file(file_path):
    """
    Reads a JSON file and returns the data.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def parse_xml_response(response):
    """Standardize XML parsing with error handling"""
    try:
        return xmltodict.parse(response)
    except Exception as e:
        raise AssertionError(f"Invalid XML response: {str(e)}")