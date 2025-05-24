from helpers.endpoints_load import EndpointsLoader


def test_endponit_loaders():
    endpoints_loader = EndpointsLoader("admin", "user")
    endpoints = endpoints_loader.get_endpoints()
    assert endpoints is not None
    assert "add_user" in endpoints
