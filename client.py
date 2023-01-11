import requests
import json
import logging


logger = logging.getLogger(__name__)

class FTTH:
    _instance = None

    def __init__(self, home_id):
        self.home_id = home_id

class ImpulseFTTH(FTTH):
    _instance = None

    def __init__(self, home_id, gescal, product_package):
        self.home_id = super().__init__(home_id)
        self.gescal = gescal
        self.voip1_sip_username = None
        self.voip1_sip_password = None
        self.voip2_sip_username = None 
        self.voip2_sip_password = None 
        self.fixed_ip_mac = None 
        self.fixed_ip_adress = None 
        self.product_package = product_package
        self.additional_info = None 
    
class Mobile:
    _instance = None 

    def __init__(self, has_advertise, add_type, iccid, road_type, road, number,
    postal_code, city, province):

        self.has_advertise = has_advertise
        self.add_type = add_type
        self.current_phone_number = None 
        self.donor_operator = None 
        self.old_iccid = None 
        self.iccid = iccid 
        self.road_type = road_type 
        self.road = road 
        self.number = number 
        self.postal_code = postal_code 
        self.city = city 
        self.province = province 

class Place:
    _instance = None 

    def __init__(self, id):

        self.id = id

class ProductCharacts:
    _instance = None 

    def __init__(self, name, value):

        self.name = name 
        self.value = value 

class CustomerAccount: 
    _instance = None 

    def __init__(self, id, firstName, secondName, thirdName, birthDate, email,
    phone, phone2, documentType, documentNumber):

        self.id = id 
        self.firstName = firstName 
        self.secondName = secondName 
        self.thirdName = thirdName 
        self.birthDate = birthDate
        self.email = email 
        self.phone = phone 
        self.phone2 = phone2 
        self.documentType = documentType 
        self.documentNumber = documentNumber

class Product:
    _instance = None 

    def __init__(self, id, productCharacts: ProductCharacts, productOrderItems):

        self.id = id
        self.productCharacts = productCharacts 
        self.productOrderItems = productOrderItems
        self.customerAccount = None

class ProductOrderItem:
    _instance = None 

    def __init__(self, action, place: Place, product: Product):

        self.action = action
        self.place = place 
        self.product = product

class Order:
    _instance = None 

    def __init__(self, orderId, externalId, orderDate, requestStartDate, 
    productOrderItem: ProductOrderItem):

        self.orderId = orderId
        self.externalId = externalId 
        self.orderDate = orderDate
        self.requestStartDate = requestStartDate
        self.productOrderItem = productOrderItem

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

    def _get(self, path: str, auth=True) -> dict:
        
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

    
    
    

