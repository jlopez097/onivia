import pytest 
from client import Client
import requests
import json

def test_client_check_login(mocker):
    mocker.patch.object(Client, "_post", return_value={"access_token":"123"})
    client = Client("client_id","username", "pass")
    client.check_login()
    assert client.token == "123"

@pytest.mark.skip(reason="No way of currently testing this")
def test_client__get(mocker):
    path = "test_path"
    mocker.patch.object(Client, "check_login", return_value=True)
    token = "1234567890"
    test = mocker.Mock()
    test.headers = {"test": "test"}
    test.content = b'{"test":"test"}'
    mocker.patch.object(requests, "get", return_value=test)
    client = Client("client_id","username", "pass")
    client.token = token
    client._get(path)
    
    assert (
        client.last_request
        == "{'accept': '*/*', 'Authorization': '1234567890'}\n"
    )

@pytest.mark.skip(reason="No way of currently testing this")
def test_client__post(mocker):
    path = "test_path"
    mocker.patch.object(Client, "check_login", return_value=True)
    token = "1234567890"
    test = mocker.Mock()
    test.headers = {"test": "test"}
    test.content = b'{"test":"test"}'
    mocker.patch.object(requests, "post", return_value=test)
    client = Client("client_id","username", "pass")
    client.token = token
    client._post(path, {})
    
    assert (
        client.last_request
        == "{'Content-Type': 'application/json', 'accept': 'application/json', 'Authorization': '1234567890'}\n"
    )

def test_client_coincident_streets(mocker):
    mocker.patch.object(Client, "check_login", return_value=True)
    token = "1234567890"
    name = "name"
    mocker.patch.object(
        Client, "_get",
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
    client = Client("client_id", "username", "pass", json.dumps({"token ": token}))
    assert type(client.get_coincident_streets(name)) == list
    assert type(client.get_coincident_streets(name)[0]) == dict 
    assert client.get_coincident_streets(name) == [
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
    assert type(client.get_coincident_streets(name)[0]["g12"]) == str
    assert type(client.get_coincident_streets(name)[0]["adressG12"]) == str
    assert type(client.get_coincident_streets(name)[0]["town"]) == str
    assert type(client.get_coincident_streets(name)[0]["province"]) == str
    assert type(client.get_coincident_streets(name)[0]["postalCode"]) == str

def test_client_coincident_number_streets(mocker):
    mocker.patch.object(Client, "check_login", return_value=True)
    token = "1234567890"
    name = "name"
    number = "1"
    mocker.patch.object(
        Client, "_get",
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
    client = Client("client_id", "username", "pass", json.dumps({"token ": token}))
    assert type(client.get_coincident_number_streets(name, number)) == list
    assert type(client.get_coincident_number_streets(name, number)[0]) == dict 
    assert client.get_coincident_number_streets(name, number) == [
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
    assert type(client.get_coincident_number_streets(name, number)[0]["g17"]) == str
    assert type(client.get_coincident_number_streets(name, number)[0]["adressG17"]) == str
    assert type(client.get_coincident_number_streets(name, number)[0]["town"]) == str
    assert type(client.get_coincident_number_streets(name, number)[0]["province"]) == str
    assert type(client.get_coincident_number_streets(name, number)[0]["postalCode"]) == str

def test_client_num_street_g12(mocker):
    mocker.patch.object(Client, "check_login", return_value=True)
    token = "1234567890"
    g12 = "1111111111"
    mocker.patch.object(
        Client, "_get",
        return_value=[
            {"g17":"1",
             "number": "11"},
            {"g17":"2",
             "number": "22"}
        ]
    )
    client = Client("client_id", "username", "pass", json.dumps({"token ": token}))
    assert type(client.num_street_g12(g12)) == list
    assert type(client.num_street_g12(g12)[0]) == dict 
    assert client.num_street_g12(g12) == [
            {"g17":"1",
             "number": "11"},
            {"g17":"2",
             "number": "22"}
    ]
    assert type(client.num_street_g12(g12)[0]["g17"]) == str
    assert type(client.num_street_g12(g12)[0]["number"]) == str

def test_client_get_homes_by_g17(mocker):
    mocker.patch.object(Client, "check_login", return_value=True)
    token = "1234567890"
    g17 = "1111111111"
    mocker.patch.object(
        Client, "_get",
        return_value=[
            {"adress":"adress1",
             "gescal37": "1",
             "homeId": "111111"},
            {"adress":"adress2",
             "gescal37": "2",
             "homeId": "222222"}
        ]
    )
    client = Client("client_id", "username", "pass", json.dumps({"token ": token}))
    assert type(client.get_homes_by_g17(g17)) == list
    assert type(client.get_homes_by_g17(g17)[0]) == dict 
    assert client.get_homes_by_g17(g17) == [
            {"adress":"adress1",
             "gescal37": "1",
             "homeId": "111111"},
            {"adress":"adress2",
             "gescal37": "2",
             "homeId": "222222"}
    ]
    assert type(client.get_homes_by_g17(g17)[0]["adress"]) == str
    assert type(client.get_homes_by_g17(g17)[0]["gescal37"]) == str
    assert type(client.get_homes_by_g17(g17)[0]["homeId"]) == str

