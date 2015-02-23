import unittest
from tests.base_test import Product, ClientWithAddress, compare_objs, \
    ClientWithManyProducts, BaseTestFactory


class MapProductTest(unittest.TestCase):
    def setUp(self):
        self.product = Product('prod01', 'test product', 20.2)
        self.dict_produto = self.product.as_dict()

        self.mapped_product = Product()
        self.mapped_product.map_dict(self.dict_produto)

    def test_mapping_product_name(self):
        self.assertEqual(self.product.name, self.dict_produto['name'], "attribute name was not mapped properly ")

    def test_mapping_product_description(self):
        self.assertEqual(self.product.description, self.dict_produto['description'],
                         "attribute description was not mapped properly ")

    def test_mapping_product_price(self):
        self.assertEqual(self.product.price, self.dict_produto['price'], "attribute price was not mapped properly ")

    def test_mapping_return_product_name(self):
        self.assertEqual(self.product.name, self.mapped_product.name,
                         "attribute return_p.name was not mapped properly ")

    def test_mapping_return_product_description(self):
        self.assertEqual(self.product.description, self.mapped_product.description,
                         "attribute return_p.description was not mapped properly ")

    def test_mapping_return_product_price(self):
        self.assertEqual(self.product.price, self.mapped_product.price,
                         "attribute return_p.price was not mapped properly ")


class ClientWithFewAddressTest(unittest.TestCase):
    def setUp(self):
        super(ClientWithFewAddressTest, self).setUp()
        self.client = BaseTestFactory.create_client_with_3_address()
        self.dict_client = self.client.as_dict()

        self.return_client = ClientWithAddress()
        self.return_client.map_dict(self.dict_client)

    def test_client_name_mapping(self):
        self.assertEqual(self.client.name, self.return_client.name, " name not mapped")

    def test_client_last_name_mapping(self):
        self.assertEqual(self.client.last_name, self.return_client.last_name, " last_name not mapped")

    def test_client_address1_mapping(self):
        cl_addr_1 = self.client.address[0]
        rt_addr_1 = self.return_client.address[0]
        self.assertTrue(compare_objs(cl_addr_1, rt_addr_1), "cl_addr_1 and rt_addr_1 are diferent")

    def test_client_address2_mapping(self):
        cl_addr_2 = self.client.address[1]
        rt_addr_2 = self.return_client.address[1]
        self.assertTrue(compare_objs(cl_addr_2, rt_addr_2), "cl_addr_2 and rt_addr_2 are diferent")

    def test_client_address3_mapping(self):
        cl_addr_3 = self.client.address[2]
        rt_addr_3 = self.return_client.address[2]
        self.assertTrue(compare_objs(cl_addr_3, rt_addr_3), "cl_addr_3 and rt_addr_3 are diferent")


class ClientWithManyProductsTest(unittest.TestCase):
    def setUp(self):
        super(ClientWithManyProductsTest, self).setUp()
        self.client = BaseTestFactory.create_clients_with_many_products()
        self.dict_client = self.client.as_dict()
        self.return_client = ClientWithManyProducts()
        self.return_client.map_dict(self.dict_client)

    def test_client_name_mapping(self):
        self.assertEqual(self.client.name, self.return_client.name, " name not mapped")

    def test_client_name_mapping(self):
        self.assertEqual(self.client.name, self.return_client.name, " name not mapped")

    def test_client_products_id_count(self):
        self.assertCountEqual(self.client.products_id, self.return_client.products_id,
                              "count of cl.products_id and cl.products_id are not the same")
