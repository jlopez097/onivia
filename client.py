import requests
import json
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class FTTH:
    home_id: str

@dataclass
class ImpulseFTTH:

    home_id: str
    gescal: str 
    product_package: str
    
@dataclass
class Mobile:

    has_advertise: bool
    add_type: str
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
    firstName: str 
    secondName: str 
    thirdName: str 
    birthDate: str 
    email: str 
    phone: str 
    phone2: str 
    documentType: str 
    documentNumber: str 

@dataclass
class Product:

    id: str 
    productCharacts: ProductCharacts 
    productOrderItems: list 

@dataclass
class ProductOrderItem:

    action: str 
    place: Place 
    product: Product

@dataclass
class Order:

    orderId: str 
    externalId: str 
    orderDate: str 
    requestStartDate: str 
    productOrderItem: ProductOrderItem 

class Client:
    _instance = None

    def __init__(self, url: str, id: str, username: str, password: str):
        self.base_url = url
        self.id = id 
        self.username = username 
        self.password = password

        self.fiber = None
        self.mobile = None

        self.last_request = None
        self.last_response = None

    def _post(self, path: str, data, auth=True) -> dict:

        headers = {
            'Authorization': '',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        if auth:
            headers.update({"Authorization": "{}".format(self.token)})

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
        
        self.last_response = r.json()

        return r.json()

    def _get(self, path: str, auth=True) -> dict|list:
        
        headers = {"accept": "*/*"} 
        
        if auth:
            headers.update({"Authorization": "{}".format(self.token)})

        r = requests.get(
            url="{}/{}".format(self.base_url, path),
            headers=headers,
            verify=False,
        )

        self.last_request = {
            "headers": headers,
            "url": "{}{}".format(self.base_url, path),
        }  

        self.last_response = r.json()

        return r.json()

    def check_login(self) -> bool:
        response = self._post(
            "/auth/realms/onivia/protocol/openid-connect/token", 
            f'client_id={self.id}&grant_type=password&username={self.username}&password={self.password}', 
            auth=False
        )
        self.token = response.get("access_token")

        return True

    ## Coverage methods ##

    def get_coincident_streets(self, name: str) -> list:

        self.check_login()

        return self._get("/coverage/v1/streets?name={}".format(name))

    def get_coincident_number_streets(self, name: str, number: str) -> list:

        self.check_login()

        return self._get("/coverage/v1/sites/numbers?name={} {}".format(name, number))

    def get_num_street_g12(self, g12: str) -> list:

        self.check_login()

        return self._get("/coverage/v1/streetNumbers?g12={}".format(g12))

    def get_homes_by_g17(self, g17: str) -> list:

        self.check_login()

        return self._get("/coverage/v1/homes?g17={}".format(g17))

    ## Product Ordering methods ##
    
    def productOrder_create(self, data: Order) -> dict:

        return self._post("/productOrderingManagement/productOrder", data=data)

    def productOrder_cancel(self, orderId: str, requestedCancellationDate: str,
    cancellationReason: str) -> dict:

        data = {
            "orderId": orderId,
            "requestedCancellationDate": requestedCancellationDate,
            "cancellationReason": cancellationReason
        }

        return self._post("/productOrderingManagement/productOrder/cancel", 
        data=data)

    def get_productOrder(self, id: str) -> dict:

        return self._get("/productOrderingManagement/productOrder/{}".format(id))
    
    def get_commercial_catalog(self) -> list:

        return self._get("/productOrderingManagement/catalog")

    def get_street_types(self) -> list:
    
        return self._get("/productOrderingManagement/catalog")

    def get_provinces(self) -> list:

        return self._get("/productOrderingManagement/mobile/provinces")

    def get_donor_operators(self) -> list:

        return self._get("/productOrderingManagement/mobile/")

    def get_reasons(self) -> list:

        return self._get("/productOrderingManagement/mobile/reasons")

    def get_additional_info(self) -> list:

        return self._get("/productOrderingManagement/ftth/additional-info")