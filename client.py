import requests
import json
import logging
from dataclasses import dataclass, asdict
from typing import Union, List

## TODO: Implementar refresh_method para controlar expiracion de token

logger = logging.getLogger(__name__)

@dataclass
class FTTH:
    home_id: str

@dataclass
class ImpulseFTTH:

    home_id: str
    gescal: str 
    voip1_sip_username: str 
    voip1_sip_password: str 
    voip2_sip_username: str 
    voip2_sip_password: str 
    fixed_ip_mac: str 
    fixed_ip_adress: str 
    product_package: str
    additional_info: str
    
@dataclass
class Mobile:

    has_advertise: bool
    add_type: str
    current_phone_number: str 
    donor_operator: str 
    old_iccid: str
    iccid: str 
    road_type: str
    road: str
    number: str 
    postal_code: str
    city: str
    province: str

@dataclass
class Place:

    id: str

@dataclass
class ProductCharacts:

    name: str
    value: str

@dataclass
class CustomerAccount: 

    id: str 
    first_name: str 
    second_name: str 
    third_name: str 
    birth_date: str 
    email: str 
    phone: str 
    phone2: str 
    document_type: str 
    document_number: str 

@dataclass
class Product:

    id: str 
    product_characts: List[ProductCharacts]
    product_order_items: list 
    customer_account: CustomerAccount

@dataclass
class ProductOrderItem:

    action: str 
    place: Place 
    product: Product

@dataclass
class Order:

    order_id: str 
    external_id: str 
    order_date: str 
    request_start_date: str 
    product_order_item: ProductOrderItem 

@dataclass
class CTO:

    codigo_cto: str
    codigo_sp1: str
    codigo_sp2: str
    estado_puerto: str
    puerto_cto: str
    puerto_sp2: str

@dataclass 
class OutputParam:

    key: str 
    value: str

@dataclass 
class Data: 

    output_param: List[OutputParam]

@dataclass
class VoipAttributes:

    voip_1_cli: str 
    voip_1_manual_sip_credentials_active: bool
    voip_1_username: str
    voip_1_password: str
    voip_1_additional_info: str 
    voip_2_cli: str 
    voip_2_manual_sip_credentials_active: bool
    voip_2_username: str
    voip_2_password: str
    voip_2_additional_info: str 

class OniviaBaseClient:
    
    def __init__(self, url: str, client_id: str, username: str, password: str):
        self.base_url = url
        self.client_id = client_id 
        self.username = username 
        self.password = password
        self._token = None
        self._token_type = None

        self.last_request = None
        self.last_response = None

    def _post(self, path: str, data) -> dict:

        headers = {
            'Content-Type': 'application/json',
            "accept": "application/json",
        }

        if self._token:
            headers.update({"Authorization": "{} {}".format(self._token_type, self._token)})

        r = requests.post(
            url="{}/{}".format(self.base_url, path),
            data=data,
            headers=headers,
            verify=False,
        )

        self.last_request = {
            "headers": headers,
            "content": data,
            "url": "{}{}".format(self.base_url, path),
        }
        
        self.last_response = r

        return r

    def _get(self, path: str) -> Union[dict, list]:
        
        headers = {"accept": "application/json"} 
        
        if self._token:
            headers.update({"Authorization": "{} {}".format(self._token_type, self._token)})

        r = requests.get(
            url="{}/{}".format(self.base_url, path),
            headers=headers,
            verify=False,
        )

        self.last_request = {
            "headers": headers,
            "url": "{}{}".format(self.base_url, path),
        }  

        self.last_response = r

        return r

    def _get_token(self) -> dict:

        data = {
            "client_id": self.client_id, 
            "grant_type": "password",
            "username": self.username,
            "password": self.password
        }

        headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(
            "{}/auth/realms/onivia/protocol/openid-connect/token".format(self.base_url), 
            data = data, 
            headers = headers
        )

        return response
    
    def _check_login(self) -> bool:
        
        if self._token: ##Y el token no ha expirado
            return True

        r = self._get_token()

        self._token = r.get("access_token")
        self._token_type = r.get("token_type")

        return True

class OniviaCoverageClient(OniviaBaseClient):

    _instance = None

    def __new__(cls, *args, **kwargs):
        if OniviaCoverageClient._instance is None:
            OniviaCoverageClient._instance = object.__new__(cls)
        return OniviaCoverageClient._instance
    
    def get_coincident_streets(self, name: str) -> list:

        self._check_login()

        return self._get("/coverage/v1/streets?name={}".format(name))

    def get_coincident_number_streets(self, name: str, number: str) -> list:

        self._check_login()

        return self._get("/coverage/v1/sites/numbers?name={} {}".format(name, number))

    def get_num_street_g12(self, g12: str) -> list:

        self._check_login()

        return self._get("/coverage/v1/streetNumbers?g12={}".format(g12))

    def get_homes_by_g17(self, g17: str) -> list:

        self._check_login()

        return self._get("/coverage/v1/homes?g17={}".format(g17))

class OniviaProductOrderingClient(OniviaBaseClient):
    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if OniviaProductOrderingClient._instance is None:
            OniviaProductOrderingClient._instance = object.__new__(cls)
        return OniviaProductOrderingClient._instance

    def product_order_create(self, order: Order) -> dict:

        self._check_login()

        return self._post("/productOrderingManagement/productOrder", data=asdict(order))

    def product_order_cancel(self, order_id: str, requested_cancellation_date: str,
    cancellation_reason: str) -> dict:

        self._check_login()
        
        data = {
            "orderId": order_id,
            "requestedCancellationDate": requested_cancellation_date,
            "cancellationReason": cancellation_reason
        }

        return self._post("/productOrderingManagement/productOrder/cancel", 
        data=data)

    def get_product_order(self, id: str) -> dict:

        self._check_login()

        return self._get("/productOrderingManagement/productOrder/{}".format(id))
    
    def get_commercial_catalog(self) -> list:

        self._check_login()

        return self._get("/productOrderingManagement/catalog")

    def get_street_types(self) -> list:
    
        self._check_login()

        return self._get("/productOrderingManagement/catalog")

    def get_provinces(self) -> list:

        self._check_login()
        
        return self._get("/productOrderingManagement/mobile/provinces")

    def get_donor_operators(self) -> list:

        self._check_login()
        
        return self._get("/productOrderingManagement/mobile/")

    def get_reasons(self) -> list:

        self._check_login()

        return self._get("/productOrderingManagement/mobile/reasons")

    def get_additional_info(self) -> list:

        self._check_login()

        return self._get("/productOrderingManagement/ftth/additional-info")

    def cto_query(self, product_id: str, cto_code=None) -> dict:

        self._check_login()
        
        data = {"ctoCode": cto_code}

        return self._post("/productOrderingManagement/ftth/{}/queryCto".format(product_id), data=data)

    def cto_change(self, product_id: str, cto_final_code: str, cto_final_port: str, sp2_final_code: str, sp2_final_port: str, reason: str) -> dict:

        self._check_login()

        data = {
            "ctoFinalCode": cto_final_code, 
            "ctoFinalPort": cto_final_port, 
            "sp2FinalCode": sp2_final_code, 
            "sp2FinalPort": sp2_final_port, 
            "reason": reason
        }

        return self._post("/productOrderingManagement/ftth/{}/changeCto".format(product_id), data=data)

    def exec_test(self, product_id: str, test_id: str) -> dict:
        
        self._check_login()
        
        return self._get("/productOrderingManagement/ftth/{}/test/{}".format(product_id, test_id))

    def voip_mod(self, product_id: str, product_package: str, voip_attributes: VoipAttributes) -> dict:

        self._check_login()
        
        data = {
            "product_package": product_package,
            "voipAttributes": asdict(voip_attributes)
        }
        
        return self._post("/productOrderingManagement/ftth/{}/voipChange".format(product_id), data=data)
    
    def fixed_ip_change(self, product_id: str, ip_enable: str, ip_adress: str, ip_mac: str):

        self._check_login()
        
        data = {
            "ipEnable": ip_enable,
            "ipAdress": ip_adress, 
            "ipMac": ip_mac 
        }    

        return self._post("/productOrderingManagement/ftth/{}/fixedIpChange".format(product_id), data=data)