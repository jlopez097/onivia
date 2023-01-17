import pytest 
from client import OniviaCoverageClient, OniviaProductOrderingClient, Order, ProductOrderItem, Place, Product, ProductCharacts, CustomerAccount, CTO, Data, OutputParam, VoipAttributes
import requests
from requests import Response

@pytest.fixture
def onivia_coverage_client():
    client = OniviaCoverageClient("http://auth-test.onivia.es","client_id","username", "pass")
    client._token = "12345"
    client._token_type = "bearer"
    return client

@pytest.fixture
def onivia_product_ordering_client():
    client = OniviaProductOrderingClient("http://auth-test.onivia.es","client_id","username", "pass")
    client._token = "12345"
    client._token_type = "bearer"
    return client

## Tests for Onivia Coverage Client ##

def test_rubik_owner_oniviav2_client__get_token(mocker, onivia_coverage_client):

    mocker.patch.object(
        requests, "post",
        return_value={
            "access_token": "12345",
            "expires_in": 1800,
            "refresh_expires_in": 1800,
            "refresh_token": "67890",
            "token_type": "bearer",
            "not-before-policy": 0,
            "session_state": "b6fc44ba-1bee-41a1-bf33-a54d42280965",
            "scope": "openid email profile",
        }
    )

    get_token_response = onivia_coverage_client._get_token()

    assert type(get_token_response) == dict 
    assert get_token_response == {
        "access_token": "12345",
        "expires_in": 1800,
        "refresh_expires_in": 1800,
        "refresh_token": "67890",
        "token_type": "bearer",
        "not-before-policy": 0,
        "session_state": "b6fc44ba-1bee-41a1-bf33-a54d42280965",
        "scope": "openid email profile",
    }

def test_rubik_owner_oniviav2_client__check_login(mocker,onivia_coverage_client):
    mocker.patch.object(
        onivia_coverage_client, 
        "_get_token", 
        return_value={"access_token":"123", "token_type":"bearer"})
    onivia_coverage_client._check_login()
    assert onivia_coverage_client._token == "12345"
    assert onivia_coverage_client._token_type == "bearer"

def test_rubik_owner_oniviav2_client__get(mocker, onivia_coverage_client):
    
    r = Response()
    r.code = "expired"
    r.error_type = "expired"
    r.status_code = 400
    r._content = b'{ "key" : "some_test_response" }'
    r = r.json()
    
    path = "test_path"
    
    token = onivia_coverage_client._token
    token_type = onivia_coverage_client._token_type
    
    auth = "{} {}".format(token_type, token)
    headers = {
        "accept": "application/json", 
        "Authorization": auth
    } 

    mocker.patch.object(requests, "get", 
        return_value=r
    )
    
    g = onivia_coverage_client._get(path)

    assert onivia_coverage_client.last_request == {
        "headers": headers,
        "url": "{}{}".format(onivia_coverage_client.base_url, path)
    }
    assert onivia_coverage_client.last_response == r
    assert g == r
    assert type(onivia_coverage_client.last_request) == dict
    assert type(onivia_coverage_client.last_response) == dict
    assert type(g) == dict

def test_rubik_owner_oniviav2_client__post(mocker, onivia_coverage_client):
    
    r = Response()
    r.code = "expired"
    r.error_type = "expired"
    r.status_code = 400
    r._content = b'{ "key" : "some_test_response" }'
    r = r.json()
    
    path = "test_path"

    data = {"id": "1"}
    
    token = onivia_coverage_client._token
    token_type = onivia_coverage_client._token_type
    
    auth = "{} {}".format(token_type, token)
    headers = {
        'Content-Type': 'application/json',
        "accept": "application/json", 
        "Authorization": auth, 
    } 

    mocker.patch.object(requests, "post", 
        return_value=r
    )
    
    p = onivia_coverage_client._post(path, data)

    assert onivia_coverage_client.last_request == {
        "headers": headers,
        "content": data,
        "url": "{}{}".format(onivia_coverage_client.base_url, path)
    }
    assert onivia_coverage_client.last_response == r
    assert p == r 
    assert type(onivia_coverage_client.last_request) == dict
    assert type(onivia_coverage_client.last_response) == dict
    assert type(p) == dict

def test_rubik_owner_oniviav2_client_coincident_streets(mocker, onivia_coverage_client):
    name = "name"
    mocker.patch.object(
        onivia_coverage_client, "_get",
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
    name = "name"
    number = "1"
    mocker.patch.object(
        onivia_coverage_client, "_get",
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
    g12 = "1111111111"
    mocker.patch.object(
        onivia_coverage_client, "_get",
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
    g17 = "1111111111"
    mocker.patch.object(
        onivia_coverage_client, "_get",
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

    order = Order(
        None,
        "12312314",
        None,
        "",
        [
            ProductOrderItem(
                Place("P0800076000000000000000000000000010543"),
                "add",
                Product(
                    "Fibra 600 MB",
                    [
                        ProductCharacts("gescal", "08000180234300002 0012"),
                        ProductCharacts("home_id", "P0800018000000000000000000000000092267"),
                        ProductCharacts("product_package", "FIBRA")
                    ],
                    CustomerAccount(
                        None,
                        "Manuel",
                        "Perez",
                        "Gonzalez",
                        None,
                        "manuel@correo.com",
                        "666889955",
                        None,
                        "DNI",
                        "61186091L"
                    )
                )
            )
        ]
    )
    
    expected_order_dict = {
        "requestStartDate": "",
        "externalId": "12312314",
        "productOrderItem": [
            {
                "place": {
                    "id": "P0800076000000000000000000000000010543"
                },
                "action": "add",
                "product": {
                    "name": "Fibra 600 MB",
                    "productCharacteristics": [
                        {
                            "name": "gescal", 
                            "value": "08000180234300002 0012"
                        },
                        {
                            "name": "home_id", 
                            "value": "P0800018000000000000000000000000092267"
                        },
                        {
                            "name": "product_package", 
                            "value": "FIBRA"
                        }
                    ],
                    "customerAccount": {
                        "firstName": "Manuel",
                        "secondName": "Perez",
                        "thirdName": "Gonzalez",
                        "email": "manuel@correo.com",
                        "phone": "666889955",
                        "documentType": "DNI",
                        "documentNumber": "61186091L"
                    }
                }
            }
        ]
    }
    
    mocked = mocker.patch.object(onivia_product_ordering_client, "_post",
        return_value={"orderId": "1"}
    )

    product_order_response = onivia_product_ordering_client.product_order_create(order)

    mocked.assert_called_with('/productOrderingManagement/productOrder', data=expected_order_dict)
    assert type(product_order_response) == dict 
    assert product_order_response["orderId"] == "1"

def test_rubik_owner_oniviav2_client_product_order_cancel(mocker, onivia_product_ordering_client):
    
    order_id = "1"
    requested_cancellation_date = "1"
    cancellation_reason = "Customer Declined Offer"

    mocker.patch.object(onivia_product_ordering_client, "_post",
        return_value={"orderId": "1"}
    )

    product_order_cancel = onivia_product_ordering_client.product_order_cancel(order_id, requested_cancellation_date, cancellation_reason)

    assert type(product_order_cancel) == dict 
    assert product_order_cancel == {"orderId": "1"}
    assert type(product_order_cancel['orderId']) == str

def test_rubik_owner_oniviav2_client_get_product_order(mocker, onivia_product_ordering_client):
    
    id = "1"

    test_res = {
        "orderId": "123", 
        "externalId": "321", 
        "orderDate": "",
        "requestStartDate": "",
        "productOrderItem": [],
    }

    mocker.patch.object(onivia_product_ordering_client, "_get",
        return_value=test_res
    )

    get_product_order_response = onivia_product_ordering_client.get_product_order(id) 

    assert type(get_product_order_response) == Order
    assert get_product_order_response == Order(
        test_res["orderId"],
        test_res["externalId"],
        test_res["orderDate"],
        test_res["requestStartDate"],
        test_res["productOrderItem"]
    )

def test_rubik_owner_oniviav2_client_get_commercial_catalog(mocker, onivia_product_ordering_client): 
    
    mocker.patch.object(onivia_product_ordering_client, "_get",
        return_value=[
            {
                "namingId": "1", 
                "name": "Fibra 600 MB",
                "description": "Fibra 600 MB",
                "isBundle": False,
                "contains": [],
            }, 
            {
                "namingId": "2", 
                "name": "Fibra 300 MB",
                "description": "Fibra 300 MB",
                "isBundle": False,
                "contains": [],
            }
        ]
    )

    get_commercial_catalog_response = onivia_product_ordering_client.get_commercial_catalog()

    assert type(get_commercial_catalog_response) == list 
    assert type(get_commercial_catalog_response[0]) == dict 
    assert get_commercial_catalog_response == [
        {
            "namingId": "1", 
            "name": "Fibra 600 MB",
            "description": "Fibra 600 MB",
            "isBundle": False,
            "contains": [],
        }, 
        {
            "namingId": "2", 
            "name": "Fibra 300 MB",
            "description": "Fibra 300 MB",
            "isBundle": False,
            "contains": [],
        }
    ]
    assert type(get_commercial_catalog_response[0]["namingId"]) == str 
    assert type(get_commercial_catalog_response[0]["name"]) == str 
    assert type(get_commercial_catalog_response[0]["description"]) == str 
    assert type(get_commercial_catalog_response[0]["isBundle"]) == bool 
    assert type(get_commercial_catalog_response[0]["contains"]) == list 

def test_rubik_owner_oniviav2_client_get_street_types(mocker, onivia_product_ordering_client):
    
    mocker.patch.object(onivia_product_ordering_client, "_get",
        return_value=[
            {
                "id": "1",
                "name": "Alameda",
            },
            {
                "id": "2",
                "name": "Aldea",
            }
        ]
    )

    get_street_types_response = onivia_product_ordering_client.get_street_types()

    assert type(get_street_types_response) == list 
    assert type(get_street_types_response[0]) == dict 
    assert get_street_types_response == [
        {
            "id": "1",
            "name": "Alameda",
        },
        {
            "id": "2",
            "name": "Aldea",
        }
    ]
    assert type(get_street_types_response[0]["id"]) == str 
    assert type(get_street_types_response[0]["name"]) == str 

def test_rubik_owner_oniviav2_client_get_provinces(mocker, onivia_product_ordering_client):
    
    mocker.patch.object(onivia_product_ordering_client, "_get",
        return_value=[
            {
                "id": "47",
                "name": "A CORUÑA",
            },
            {
                "id": "51",
                "name": "ALAVA",
            }
        ]
    )

    get_provinces_response = onivia_product_ordering_client.get_provinces() 

    assert type(get_provinces_response) == list 
    assert type(get_provinces_response[0]) == dict 
    assert get_provinces_response == [
        {
            "id": "47",
            "name": "A CORUÑA",
        },
        {
            "id": "51",
            "name": "ALAVA",
        }
    ]
    assert type(get_provinces_response[0]["id"]) == str 
    assert type(get_provinces_response[0]["name"]) == str

def test_rubik_owner_oniviav2_client_get_donor_operators(mocker, onivia_product_ordering_client):
    
    mocker.patch.object(onivia_product_ordering_client, "_get",
        return_value=[
            {
                "id": "1",
                "name": "MOVISTAR",
                "isEnabled": "true"
            },
            {
                "id": "2",
                "name": "VODAFONE",
                "isEnabled": "true"
            }
        ]
    )

    get_donor_operators_response = onivia_product_ordering_client.get_donor_operators() 

    assert type(get_donor_operators_response) == list 
    assert type(get_donor_operators_response[0]) == dict 
    assert get_donor_operators_response == [
        {
            "id": "1",
            "name": "MOVISTAR",
            "isEnabled": "true"
        },
        {
            "id": "2",
            "name": "VODAFONE",
            "isEnabled": "true"
        }
    ]
    assert type(get_donor_operators_response[0]["id"]) == str 
    assert type(get_donor_operators_response[0]["name"]) == str
    assert type(get_donor_operators_response[0]["isEnabled"]) == str

def test_rubik_owner_oniviav2_client_get_reasons(mocker, onivia_product_ordering_client):
    
    mocker.patch.object(onivia_product_ordering_client, "_get",
        return_value=[
            {
                "id": "1",
                "name": "Defunción",
                "isEnabled": "true"
            },
            {
                "id": "2",
                "name": "Falta de uso",
                "isEnabled": "true"
            }
        ]
    )

    get_reasons_response = onivia_product_ordering_client.get_reasons() 

    assert type(get_reasons_response) == list 
    assert type(get_reasons_response[0]) == dict 
    assert get_reasons_response == [
        {
            "id": "1",
            "name": "Defunción",
            "isEnabled": "true"
        },
        {
            "id": "2",
            "name": "Falta de uso",
            "isEnabled": "true"
        }
    ]
    assert type(get_reasons_response[0]["id"]) == str 
    assert type(get_reasons_response[0]["name"]) == str
    assert type(get_reasons_response[0]["isEnabled"]) == str

def test_rubik_owner_oniviav2_client_get_additional_info(mocker, onivia_product_ordering_client):
    
    mocker.patch.object(onivia_product_ordering_client, "_get",
        return_value=[
            {
                "id": "1",
                "additional_info": []
            },
            {
                "id": "2",
                "additional_info": []
            }
        ]
    )

    get_additional_info_response = onivia_product_ordering_client.get_additional_info() 

    assert type(get_additional_info_response) == list 
    assert type(get_additional_info_response[0]) == dict 
    assert get_additional_info_response == [
        {
            "id": "1",
            "additional_info": []
        },
        {
            "id": "2",
            "additional_info": []
        }
    ]
    assert type(get_additional_info_response[0]["id"]) == str 
    assert type(get_additional_info_response[0]["additional_info"]) == list

def test_rubik_owner_oniviav2_client_cto_query(mocker, onivia_product_ordering_client):
    
    product_id = "123"
    cto_code = "COD_CTO_XXX"
    
    mocker.patch.object(onivia_product_ordering_client, "_post",
        return_value={
            "codResultado": "000",
            "descResultado": "Proceso ejecutado correctamente",
            "listactos": {
                "cto": [
                    CTO(
                        cto_code,
                        "COD_SCP1_XXX",
                        "COD_SCP2_XXX",
                        "NO CONECTADO",
                        "XXX",
                        "XX"
                    )
                ]
            }
        }
    )

    cto_query_response = onivia_product_ordering_client.cto_query(product_id,cto_code) 

    assert type(cto_query_response) == dict
    assert cto_query_response == {
        "codResultado": "000",
        "descResultado": "Proceso ejecutado correctamente",
        "listactos": {
            "cto": [
                CTO(
                    cto_code,
                    "COD_SCP1_XXX",
                    "COD_SCP2_XXX",
                    "NO CONECTADO",
                    "XXX",
                    "XX"
                )
            ]
        }
    }
    assert type(cto_query_response["codResultado"]) == str 
    assert type(cto_query_response["descResultado"]) == str
    assert type(cto_query_response["listactos"]) == dict 
    assert type(cto_query_response["listactos"]["cto"]) == list 
    assert type(cto_query_response["listactos"]["cto"][0]) == CTO

def test_rubik_owner_oniviav2_client_cto_change(mocker, onivia_product_ordering_client):

    product_id = "12345"
    cto_final_code = "COD_CTO_XXX"
    cto_final_port = "XXX"
    sp2_final_code = "COD_SP2" 
    sp2_final_port = "XXX_SP2" 
    reason = ""

    mocker.patch.object(onivia_product_ordering_client, "_post",
        return_value={
            "codResultado": "123",
            "descResultado": "XXX",
            "idadministrativo": "",
            "codigoctofinal": "",
            "puertoctofinal": "", 
            "codigosp2final": "", 
            "olt": "",
            "tarjeta": "", 
            "puertopon": "",
            "ontid": "",
            "gestorvertical": ""
        }
    )

    cto_change_response = onivia_product_ordering_client.cto_change(product_id, cto_final_code,
    cto_final_port, sp2_final_code, sp2_final_port, reason)

    assert type(cto_change_response) == dict
    assert cto_change_response == {
        "codResultado": "123",
        "descResultado": "XXX",
        "idadministrativo": "",
        "codigoctofinal": "",
        "puertoctofinal": "", 
        "codigosp2final": "", 
        "olt": "",
        "tarjeta": "", 
        "puertopon": "",
        "ontid": "",
        "gestorvertical": ""
    }
    assert type(cto_change_response["codResultado"]) == str 
    assert type(cto_change_response["descResultado"]) == str
    assert type(cto_change_response["idadministrativo"]) == str
    assert type(cto_change_response["codigoctofinal"]) == str
    assert type(cto_change_response["puertoctofinal"]) == str
    assert type(cto_change_response["codigosp2final"]) == str
    assert type(cto_change_response["olt"]) == str
    assert type(cto_change_response["tarjeta"]) == str
    assert type(cto_change_response["puertopon"]) == str
    assert type(cto_change_response["ontid"]) == str
    assert type(cto_change_response["gestorvertical"]) == str

def test_rubik_owner_oniviav2_client_exec_test(mocker, onivia_product_ordering_client):

    product_id = "12345"
    test_id = "TST_FTTH_DATOS"

    output_param1 = OutputParam("PuertoGPON", "1")
    output_param2 = OutputParam("IUA", "M32904ULY7GH")

    data_i = Data([output_param1, output_param2])

    mocker.patch.object(onivia_product_ordering_client, "_get",
        return_value={
            "conclusion": "OK",
            "codigo": "000",
            "descripcion": "Test ejecutado correctamente",
            "fecha": "2022-11-21-11.03.28.000953",
            "resultado": {
                "datos": data_i,
                "datosCliente": None,
                "datosConsulta": None,
            }
        }
    )

    exec_test_response = onivia_product_ordering_client.exec_test(product_id, test_id)

    assert type(exec_test_response) == dict
    assert exec_test_response == {
        "conclusion": "OK",
        "codigo": "000",
        "descripcion": "Test ejecutado correctamente",
        "fecha": "2022-11-21-11.03.28.000953",
        "resultado": {
            "datos": data_i,
            "datosCliente": None,
            "datosConsulta": None,
        }
    }
    assert type(exec_test_response["conclusion"]) == str 
    assert type(exec_test_response["codigo"]) == str 
    assert type(exec_test_response["descripcion"]) == str 
    assert type(exec_test_response["fecha"]) == str 
    assert type(exec_test_response["resultado"]) == dict 
    assert type(exec_test_response["resultado"]["datos"]) == Data

def test_rubik_owner_oniviav2_client_voip_mod(mocker, onivia_product_ordering_client):

    product_id = "123"
    product_package = "FIBRA" 
    voipAttributes = VoipAttributes("",True,"","","","",True,"","","")

    ## Onivia no especifica los campos de salida de este método. 
    ## Hay que preguntarles para poder hacer las comprobaciones del test.
    assert True

def test_rubik_owner_oniviav2_client_fixed_ip_change(mocker, onivia_product_ordering_client):

    product_id = "123"
    ipEnable = "" 
    ipAdress = ""
    ipMac = ""

    ## Onivia no especifica los campos de salida de este método. 
    ## Hay que preguntarles para poder hacer las comprobaciones del test.
    assert True
