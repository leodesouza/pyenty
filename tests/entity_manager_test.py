import unittest
from tornado.testing import gen_test, AsyncTestCase
from pyenty import EntityManager
from pyenty.entitymanager import EntityConnection
from tests.base_test import BaseTestFactory, ClientWithAddress, compare_objs, ClientWithManyProducts, \
    ClientWithManyProductsAndAddress, StoreWithThreeClientsOnly, SimpleClient, ClientWithOneAddress, Address


class BaseTest(AsyncTestCase):
    def setUp(self):
        super(BaseTest, self).setUp()
        EntityConnection.open(db="ym_db_test", io_loop=self.io_loop)


class SaveClientTest(BaseTest):
    def setUp(self):
        super(SaveClientTest, self).setUp()
        self.emanager = EntityManager(ClientWithAddress)
        self.client = BaseTestFactory.create_client_with_3_address()

    @gen_test
    def test_save_client(self):
        self.object_id = yield self.emanager.save(self.client)
        self.client_result = yield self.emanager.find_one(_id=self.object_id)
        # yield self.emanager.remove({'_id': self.object_id})
        self.assertTrue(compare_objs(self.client, self.client_result), "client was not properly saved")


class ClientWithManyProductsTest(BaseTest):
    def setUp(self):
        super(ClientWithManyProductsTest, self).setUp()
        self.emanager = EntityManager(ClientWithManyProducts)
        self.client = BaseTestFactory.create_clients_with_many_products()

    @gen_test
    def test_saved_client_with_many_products(self):
        self.object_id = yield self.emanager.save(self.client)
        self.client_result = yield self.emanager.find_one(_id=self.object_id)
        # yield self.emanager.remove({'_id': self.object_id})
        self.assertTrue(compare_objs(self.client, self.client_result), "client was not properly saved")


class ClientWithFewAddressTest(BaseTest):
    def setUp(self):
        super(ClientWithFewAddressTest, self).setUp()
        self.emanager = EntityManager(ClientWithAddress)
        self.client = BaseTestFactory.create_client_with_3_address()

    @gen_test
    def test_saved_client_with_address(self):
        self.object_id = yield self.emanager.save(self.client)
        self.client_result = yield self.emanager.find_one(_id=self.object_id)
        self.assertTrue(compare_objs(self.client, self.client_result), "client with 3 addresses was not properly saved")


class ClientWithManyProductsAndAdressTest(BaseTest):
    def setUp(self):
        super(ClientWithManyProductsAndAdressTest, self).setUp()
        self.emanager = EntityManager(ClientWithManyProductsAndAddress)
        self.client = BaseTestFactory.create_clients_with_many_products_and_addresses()


    @gen_test
    def test_saved_client_with_address(self):
        self.object_id = yield self.emanager.save(self.client)
        self.client_result = yield self.emanager.find_one(_id=self.object_id)
        self.assertTrue(compare_objs(self.client, self.client_result), "client with 3 addresses was not properly saved")


class StoreWithThreeClientsOnlyTest(BaseTest):
    def setUp(self):
        super(StoreWithThreeClientsOnlyTest, self).setUp()
        self.emanager = EntityManager(StoreWithThreeClientsOnly)
        self.client = BaseTestFactory.create_store_with_some_clients()

    @gen_test
    def test_saved_client_with_address(self):
        self.object_id = yield self.emanager.save(self.client)
        self.client_result = yield self.emanager.find_one(_id=self.object_id)
        self.assertTrue(compare_objs(self.client, self.client_result), "client with 3 addresses was not properly saved")


class DeletedClientTest(BaseTest):
    def setUp(self):
        super(DeletedClientTest, self).setUp()
        self.emanager = EntityManager(SimpleClient)

        self.client1 = BaseTestFactory.create_client_with_3_address()
        self.client2 = BaseTestFactory.create_client_with_3_address()
        self.client3 = BaseTestFactory.create_client_with_3_address()

    @gen_test
    def test_client2_was_successful_deleted(self):
        yield self.emanager.remove_all()
        self.objectid_1 = yield self.emanager.save(self.client1)
        self.objectid_2 = yield self.emanager.save(self.client2)
        self.objectid_3 = yield self.emanager.save(self.client3)

        yield self.emanager.remove(_id=self.objectid_2)
        self.clients = yield self.emanager.find()
        self.assertEqual(self.objectid_1, self.clients[0]._id)
        self.assertEqual(self.objectid_3, self.clients[1]._id)


class UpdatedClientTest(BaseTest):
    def setUp(self):
        super(UpdatedClientTest, self).setUp()
        self.emanager = EntityManager(SimpleClient)

        self.client1 = BaseTestFactory.create_client_with_3_address()
        self.client2 = BaseTestFactory.create_client_with_3_address()
        self.client3 = BaseTestFactory.create_client_with_3_address()

    @gen_test
    def test_client2_was_successful_updated(self):
        yield self.emanager.remove_all()
        self.objectid_1 = yield self.emanager.save(self.client1)
        self.objectid_2 = yield self.emanager.save(self.client2)
        self.objectid_3 = yield self.emanager.save(self.client3)

        self.client_to_update = yield self.emanager.find_one(_id=self.objectid_2)
        self.client_to_update.name = "updated_name"
        self.client_to_update.last_name = "updated_last_name"

        yield self.emanager.update(self.client_to_update)

        self.updated_client = yield self.emanager.find_one(_id=self.objectid_2)

        self.return_client1 = yield self.emanager.find_one(_id=self.objectid_1)
        self.return_client3 = yield self.emanager.find_one(_id=self.objectid_3)

        # check if client2 was updated
        self.assertEqual(self.client_to_update.name, self.updated_client.name)
        self.assertEqual(self.client_to_update.last_name, self.updated_client.last_name)

        # check if nothing changed in client1 and client3
        self.assertTrue(compare_objs(self.client1, self.return_client1))
        self.assertTrue(compare_objs(self.client3, self.return_client3))


class RemoveAllTest(BaseTest):
    def setUp(self):
        super(RemoveAllTest, self).setUp()
        self.emanager = EntityManager(SimpleClient)

    @gen_test
    def test_remove_all_documents(self):
        yield self.emanager.remove_all()
        for i in range(0, 100):
            yield self.emanager.save(SimpleClient(name="name" + str(i), last_name="last_name" + str(i)))
        count = yield self.emanager.find()
        self.assertEqual(len(count), 100, "Ops... something went wrong on save or find ")

        yield self.emanager.remove_all()
        count = yield self.emanager.find()
        self.assertEqual(len(count), 0, "Ops... something went wrong on remove or find ")


class ClientWithOneAddressTest(BaseTest):
        def setUp(self):
            super(ClientWithOneAddressTest, self).setUp()
            self.emanager = EntityManager(ClientWithOneAddress)
            self.client_with_address = ClientWithOneAddress('leo', 'sza')
            self.address = Address(city='MANILA', street='test', number=10)
            self.client_with_address.set_address(self.address)

        @gen_test
        def test_saved_client_with_ony_address(self):
            object_id = yield self.emanager.save(self.client_with_address)
            saved_client = yield self.emanager.find_one(_id=object_id)
            self.assertTrue(compare_objs(saved_client.address, self.address), "Address was not mapped")



if __name__ == '__main__':
    unittest.main()
