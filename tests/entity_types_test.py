import unittest
from pyenty.types import Str, Entity, Int, Float, List


class Descriptors(Entity):
    int_field = Int()
    string_field = Str()
    float_field = Float()
    list_int_field = List(typeof=int)
    list_string_field = List(str)
    list_float_field = List(float)
    list_entity_field = List(Entity)

    def __init__(self,
                 int_value=0,
                 string_value="",
                 float_value=0.0,
                 list_int_value=List(typeof=int),
                 list_string_value=List(typeof=str),
                 list_float_value=List(typeof=float),
                 list_entity_value=List(typeof=Entity)):
        self.int_field = int_value
        self.string_field = string_value
        self.float_field = float_value
        self.list_int_field = list_int_value
        self.list_string_field = list_string_value
        self.list_float_field = list_float_value
        self.list_entity_field = list_entity_value


class BaseTest(unittest.TestCase):
    def set_attribute(self, instance, field, value):
        try:
            setattr(instance, field, value)
        except TypeError:
            raise TypeError

    def try_append_exception(self, obj, field, value):
        try:
            lst = getattr(obj, field)
            lst.append(value)
        except TypeError:
            raise TypeError


class SetAttributeTest(BaseTest):
    def test_set_str(self):
        self.set_attribute(Descriptors(), 'string_value', "test value")

    def test_set_int(self):
        self.set_attribute(Descriptors(), 'int_value', 2)

    def test_set_float(self):
        self.set_attribute(Descriptors(), 'float_value', 1.3)

    def test_set_empty_typed_list(self):
        descriptor = Descriptors()
        self.set_attribute(descriptor, 'list_float_field', List(typeof=float))
        self.set_attribute(descriptor, 'list_int_field', List(typeof=int))
        self.set_attribute(descriptor, 'list_string_field', List(typeof=str))

    def test_set_simple_list_to_typed_list_raise_error(self):
        self.assertRaises(TypeError, lambda: self.set_attribute(Descriptors(), 'list_int_field', []))
        self.assertRaises(TypeError, lambda: self.set_attribute(Descriptors(), 'list_float_field', []))
        self.assertRaises(TypeError, lambda: self.set_attribute(Descriptors(), 'list_string_field', []))

    def test_set_not_accepted_int_list_raise_error(self):
        list_test_int = [2.5, "aaa", 1]
        for item in list_test_int:
            self.assertRaises(TypeError, lambda: self.set_attribute(Descriptors(), 'list_int_field', item))

    def test_set_not_accepted_string_list_raise_error(self):
        list_test_string = [1, 3.5]
        for item in list_test_string:
            self.assertRaises(TypeError, lambda: self.set_attribute(Descriptors(), 'list_string_field', item))

    def test_set_not_accepted_float_list_raise_error(self):
        list_test_float = [1, "aaa"]
        for item in list_test_float:
            self.assertRaises(TypeError, lambda: self.set_attribute(Descriptors(), 'list_float_field', item))


class AppendExpectedTypeTest(BaseTest):

    def test_set_int_list_with_some_values(self):
        descriptors = Descriptors()
        lst = List(typeof=int)
        lst.append(1)
        lst.append(2)
        lst.append(3)
        self.set_attribute(descriptors, 'list_int_field', lst)
        for item in lst:
            self.assertIn(item, descriptors.list_int_field)

    def test_set_string_list_with_some_values(self):
        descriptors = Descriptors()
        lst = List(typeof=str)
        lst.append("a")
        lst.append("b")
        lst.append("c")
        self.set_attribute(descriptors, 'list_string_field', lst)
        for item in lst:
            self.assertIn(item, descriptors.list_string_field)

    def test_set_float_list_with_some_values(self):
        descriptors = Descriptors()
        lst = List(typeof=float)
        lst.append(1.0)
        lst.append(2.3)
        lst.append(3.5)
        self.set_attribute(descriptors, 'list_float_field', lst)
        for item in lst:
            self.assertIn(item, descriptors.list_float_field)


class AppendNotExpectedTypeTest(BaseTest):
    def test_try_append_not_expected_on_stringlist_raise_error(self):
        lst = [1, 1.2]
        descriptor = Descriptors()
        for item in lst:
            self.assertRaises(TypeError, lambda: self.try_append_exception(descriptor, 'list_string_field', item))

    def test_try_append_not_expected_on_intlist_raise_error(self):
        lst = ["sdf", 1.2]
        descriptor = Descriptors()
        for item in lst:
            self.assertRaises(TypeError, lambda: self.try_append_exception(descriptor, 'list_int_field', item))

    def test_try_append_not_expected_on_floatlist_raise_error(self):
        lst = [1, "6548"]
        descriptor = Descriptors()
        for item in lst:
            self.assertRaises(TypeError, lambda: self.try_append_exception(descriptor, 'list_float_field', item))


if __name__ == "__main__":
    unittest.main()


