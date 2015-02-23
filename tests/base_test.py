from pyenty.types import Entity, Str, Float, Int, List, Type


class Product(Entity):
    name = Str()
    description = Str()
    price = Float()

    def __init__(self, name="", description="", price=0.0):
        self.name = name
        self.description = description
        self.price = price


class Address(Entity):
    city = Str()
    street = Str()
    number = Int()

    def __init__(self, city="", street="", number=357):
        self.city = city
        self.street = street
        self.number = number


class SimpleClient(Entity):
    name = Str()
    last_name = Str()

    def __init__(self, name="", last_name=""):
        self.name = name
        self.last_name = last_name


class ClientWithAddress(Entity):
    name = Str()
    last_name = Str()
    address = List(typeof=Address)

    def __init__(self, name=" ", last_name=" "):
        self.name = name
        self.last_name = last_name

    def add_address(self, address):
        self.address.append(address)


class ClientWithOneAddress(Entity):
    name = Str()
    last_name = Str()
    address = Type(Address)

    def __init__(self, name=" ", last_name=" "):
        self.name = name
        self.last_name = last_name

    def set_address(self, address):
        self.address = address


class ClientWithManyProducts(Entity):
    name = Str()
    last_name = Str()
    products_id = List(typeof=int)

    def __init__(self, name="", last_name=""):
        self.name = name
        self.last_name = last_name

    def add_product_id(self, product_id):
        self.products_id.append(product_id)


class ClientWithManyProductsAndAddress(Entity):
    name = Str()
    last_name = Str()
    products_id = List(typeof=int)
    addresses = List(typeof=Address)

    def __init__(self, name="", last_name=""):
        self.name = name
        self.last_name = last_name

    def add_product_id(self, product_id):
        self.products_id.append(product_id)

    def add_address(self, address):
        self.addresses.append(address)


class StoreWithThreeClientsOnly(Entity):
    name = Str()
    clients = List(typeof=ClientWithManyProductsAndAddress)

    def __init__(self, name=""):
        self.name = name

    def add_clients(self, client):
        self.clients.append(client)


class BaseTestFactory():

    @staticmethod
    def create_client_with_3_address():
        c = ClientWithAddress('nick', 'souza')

        c.address.clear()
        address1 = Address('Rio de Janeiro', 'Av Brasil', 1209)
        address2 = Address('Sao Paulo', 'Av Paulista', 300)
        address3 = Address('Floripa', 'Av ---', 122)
        c.add_address(address1)
        c.add_address(address2)
        c.add_address(address3)
        return c

    @staticmethod
    def create_clients_with_many_products():
            cl = ClientWithManyProducts('nick', 'souza')
            cl.products_id.clear()
            for x in range(1, 100):
                cl.add_product_id(x)
            return cl

    @staticmethod
    def create_clients_with_many_products_and_addresses():
            cl = ClientWithManyProductsAndAddress('nick', 'souza')
            cl.products_id.clear()
            cl.addresses.clear()
            for x in range(1, 100):
                cl.add_product_id(x)

            cl.add_address(Address('Rio de Janeiro', 'Av Brasil', 1209))
            cl.add_address(Address('Sao Paulo', 'Av Paulista', 300))
            cl.add_address(Address('Floripa', 'Av ---', 122))
            return cl

    @staticmethod
    def create_store_with_some_clients():
        store = StoreWithThreeClientsOnly('pet_shop')
        store.add_clients(BaseTestFactory.create_clients_with_many_products_and_addresses())
        return store


def compare_obj_dict(client, dict_client):
        for key, value in dict_client.items():
            if not isinstance(value, list):
                if key != '_id':
                    attr_value = getattr(client, key)
                    if attr_value != value:
                        return False
        return True


def compare_objs(left_obj, right_obj):
        equal = None
        for left_key, left_value in left_obj.as_dict().items():
            right_attr = getattr(right_obj, left_key)
            if isinstance(left_value, list):
                count = 0
                right_item = right_attr[count]
                if isinstance(right_item, Entity):
                    equal = compare_obj_dict(right_item, left_value[0])
                else:
                    equal = right_item in left_value
                if not equal:
                    return False
                count += 1
            else:
                if left_value != right_attr:
                    return False

        return True



