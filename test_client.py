import pytest 
from client import OniviaCoverageClient, OniviaProductOrderingClient, Order
import requests

@pytest.fixture
def onivia_coverage_client():
    return OniviaCoverageClient("http://auth-test.onivia.es","client_id","username", "pass")

@pytest.fixture
def onivia_product_ordering_client():
    return OniviaProductOrderingClient("http://auth-test.onivia.es","client_id","username", "pass")

## Tests for Onivia Coverage Client ##

def test_rubik_owner_oniviav2_client_check_login(mocker,onivia_coverage_client):
    mocker.patch.object(
        OniviaCoverageClient, 
        "get_token", 
        return_value={"access_token":"123", "token_type":"bearer"})
    onivia_coverage_client.check_login()
    assert onivia_coverage_client.token == "123"
    assert onivia_coverage_client.token_type == "bearer"

@pytest.mark.skip(reason="No way of currently testing this")
def test_rubik_owner_oniviav2_client__get(mocker, onivia_coverage_client):
    path = "test_path"
    mocker.patch.object(OniviaCoverageClient, "check_login", return_value=True)
    token = "1234567890"
    test = mocker.Mock()
    test.headers = {"test": "test"}
    test.content = b'{"test":"test"}'
    mocker.patch.object(requests, "get", return_value=test)
    onivia_coverage_client.token = token
    onivia_coverage_client._get(path)
    
    assert (
        onivia_coverage_client.last_request
        == "{'accept': '*/*', 'Authorization': 'bearer 1234567890'}\n"
    )

@pytest.mark.skip(reason="No way of currently testing this")
def test_rubik_owner_oniviav2_client__post(mocker, onivia_coverage_client):
    path = "test_path"
    mocker.patch.object(OniviaCoverageClient, "check_login", return_value=True)
    token = "1234567890"
    test = mocker.Mock()
    test.headers = {"test": "test"}
    test.content = b'{"test":"test"}'
    mocker.patch.object(requests, "post", return_value=test)
    onivia_coverage_client.token = token
    onivia_coverage_client._post(path, {})
    
    assert (
        onivia_coverage_client.last_request
        == "{'Content-Type': 'application/json', 'accept': 'application/json', 'Authorization': 'bearer 1234567890'}\n"
    )

def test_rubik_owner_oniviav2_client_coincident_streets(mocker, onivia_coverage_client):
    mocker.patch.object(OniviaCoverageClient, "check_login", return_value=True)
    name = "name"
    mocker.patch.object(
        OniviaCoverageClient, "_get",
        return_value=[
            {"g12":"1",
             "adressG12": "adressG121",
             "town":"town1",
             "province": "province1",
             "postalCode": "11111"},
            {"g12":"2",
             "adressG12": "adressG122",
             "town":"town2",
             "province": "province2",
             "postalCode": "2"}
        ]
    )
    assert type(onivia_coverage_client.get_coincident_streets(name)) == list
    assert type(onivia_coverage_client.get_coincident_streets(name)[0]) == dict 
    assert onivia_coverage_client.get_coincident_streets(name) == [
            {"g12":"1",
             "adressG12": "adressG121",
             "town":"town1",
             "province": "province1",
             "postalCode": "11111"},
            {"g12":"2",
             "adressG12": "adressG122",
             "town":"town2",
             "province": "province2",
             "postalCode": "2"}
    ]
    assert type(onivia_coverage_client.get_coincident_streets(name)[0]["g12"]) == str
    assert type(onivia_coverage_client.get_coincident_streets(name)[0]["adressG12"]) == str
    assert type(onivia_coverage_client.get_coincident_streets(name)[0]["town"]) == str
    assert type(onivia_coverage_client.get_coincident_streets(name)[0]["province"]) == str
    assert type(onivia_coverage_client.get_coincident_streets(name)[0]["postalCode"]) == str

def test_rubik_owner_oniviav2_client_coincident_number_streets(mocker, onivia_coverage_client):
    mocker.patch.object(OniviaCoverageClient, "check_login", return_value=True)
    name = "name"
    number = "1"
    mocker.patch.object(
        OniviaCoverageClient, "_get",
        return_value=[
            {"g17":"1",
             "adressG17": "adressG171",
             "town": "town1",
             "province": "province1",
             "postalCode": "11111"},
            {"g17":"2",
             "adressG17": "adressG172",
             "town":"town2",
             "province": "province2",
             "postalCode": "2"}
        ]
    )
    assert type(onivia_coverage_client.get_coincident_number_streets(name, number)) == list
    assert type(onivia_coverage_client.get_coincident_number_streets(name, number)[0]) == dict 
    assert onivia_coverage_client.get_coincident_number_streets(name, number) == [
            {"g17":"1",
             "adressG17": "adressG171",
             "town":"town1",
             "province": "province1",
             "postalCode": "11111"},
            {"g17":"2",
             "adressG17": "adressG172",
             "town":"town2",
             "province": "province2",
             "postalCode": "2"}
    ]
    assert type(onivia_coverage_client.get_coincident_number_streets(name, number)[0]["g17"]) == str
    assert type(onivia_coverage_client.get_coincident_number_streets(name, number)[0]["adressG17"]) == str
    assert type(onivia_coverage_client.get_coincident_number_streets(name, number)[0]["town"]) == str
    assert type(onivia_coverage_client.get_coincident_number_streets(name, number)[0]["province"]) == str
    assert type(onivia_coverage_client.get_coincident_number_streets(name, number)[0]["postalCode"]) == str

def test_rubik_owner_oniviav2_client_num_street_g12(mocker, onivia_coverage_client):
    mocker.patch.object(OniviaCoverageClient, "check_login", return_value=True)
    g12 = "1111111111"
    mocker.patch.object(
        OniviaCoverageClient, "_get",
        return_value=[
            {"g17":"1",
             "number": "11"},
            {"g17":"2",
             "number": "22"}
        ]
    )
    assert type(onivia_coverage_client.get_num_street_g12(g12)) == list
    assert type(onivia_coverage_client.get_num_street_g12(g12)[0]) == dict 
    assert onivia_coverage_client.get_num_street_g12(g12) == [
            {"g17":"1",
             "number": "11"},
            {"g17":"2",
             "number": "22"}
    ]
    assert type(onivia_coverage_client.get_num_street_g12(g12)[0]["g17"]) == str
    assert type(onivia_coverage_client.get_num_street_g12(g12)[0]["number"]) == str

def test_rubik_owner_oniviav2_client_get_homes_by_g17(mocker, onivia_coverage_client):
    mocker.patch.object(OniviaCoverageClient, "check_login", return_value=True)
    g17 = "1111111111"
    mocker.patch.object(
        OniviaCoverageClient, "_get",
        return_value=[
            {"adress":"adress1",
             "gescal37": "1",
             "homeId": "111111"},
            {"adress":"adress2",
             "gescal37": "2",
             "homeId": "222222"}
        ]
    )
    assert type(onivia_coverage_client.get_homes_by_g17(g17)) == list
    assert type(onivia_coverage_client.get_homes_by_g17(g17)[0]) == dict 
    assert onivia_coverage_client.get_homes_by_g17(g17) == [
            {"adress":"adress1",
             "gescal37": "1",
             "homeId": "111111"},
            {"adress":"adress2",
             "gescal37": "2",
             "homeId": "222222"}
    ]
    assert type(onivia_coverage_client.get_homes_by_g17(g17)[0]["adress"]) == str
    assert type(onivia_coverage_client.get_homes_by_g17(g17)[0]["gescal37"]) == str
    assert type(onivia_coverage_client.get_homes_by_g17(g17)[0]["homeId"]) == str

## Tests for Onivia Product Ordering Client ##

def test_rubik_owner_oniviav2_client_product_order_create(mocker, onivia_product_ordering_client):
    mocker.patch.object(OniviaProductOrderingClient, "check_login", return_value=True)

    order = Order("1", "1", "1", "1", None)

    mocker.patch.object(OniviaProductOrderingClient, "_post",
        return_value={"orderId": "1"}
    )

    po = onivia_product_ordering_client.product_order_create(order)

    assert type(po) == dict 
    assert po == {"orderId": "1"}
    assert type(po["orderId"]) == str
