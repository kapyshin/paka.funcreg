import types
import unittest

import paka.funcreg

from testutils import Some


class TypeRegistryTest(unittest.TestCase):

    def make_reg(self, *args, **kwargs):
        return paka.funcreg.TypeRegistry(*args, **kwargs)

    def test_decorator_with_class(self):
        obj = Some(8)
        reg = self.make_reg()
        @reg.register(Some)
        def tst_me():
            return 123
        self.assertIs(reg[obj], tst_me)

    def test_decorator_with_class_explicit_key(self):
        obj = Some(6)
        reg = self.make_reg()
        reg.add_key(Some)
        @reg.register(Some)
        def tst_me():
            return 123
        self.assertIs(reg[obj], tst_me)

    def test_decorator_with_function_fail(self):
        def object_():
            return 3
        reg = self.make_reg()
        with self.assertRaises(TypeError):
            @reg.register(object_)
            def tst_me():
                return 123

    def test_decorator_with_function_success(self):
        reg = self.make_reg()
        @reg.add_key
        def object_():
            return 3
        @reg.register(types.FunctionType)
        def tst_me():
            return 123
        self.assertIs(reg[object_], tst_me)

    def test_decorator_without_class(self):
        reg = self.make_reg()
        @reg.register
        def tst_me():
            return 123
        self.assertIs(reg[tst_me], tst_me)

    def test_functional_with_class(self):
        obj = Some(5)
        reg = self.make_reg()
        def _some_func():
            return 432
        reg.register(_some_func, Some)
        self.assertIs(reg[obj], _some_func)

    def test_functional_without_class(self):
        reg = self.make_reg()
        def _other_func():
            return 321
        reg.register(_other_func)
        self.assertIs(reg[_other_func], _other_func)

    def test_multiple_registries(self):
        obj = Some(7)
        reg1 = self.make_reg()
        reg2 = self.make_reg()
        reg3 = self.make_reg()
        @reg2.register
        def func_for_second():
            return 321 + 2
        @reg1.register
        def func_for_first():
            return 321 + 1
        @reg3.register(Some)
        def func_for_third():
            return 321 + 3
        self.assertIs(reg1[func_for_first], func_for_first)
        self.assertIs(reg2[func_for_second], func_for_second)
        self.assertIs(reg3[obj], func_for_third)
        with self.assertRaises(KeyError):
            reg2[obj]()
        with self.assertRaises(KeyError):
            reg1[obj]()
        self.assertIs(reg2[func_for_first], func_for_second)
        with self.assertRaises(KeyError):
            reg3[func_for_first]()
        self.assertIs(reg1[func_for_second], func_for_first)
        with self.assertRaises(KeyError):
            reg3[func_for_second]()

    def test_default(self):
        def func_one():
            return 1
        def func_two():
            return 2
        def func_three():
            return 3
        reg = self.make_reg(default=func_two)
        reg.register(func_one)
        self.assertIs(reg[func_one], func_one)
        self.assertIs(reg[func_three], func_one)
        self.assertIs(reg["random thing here"], func_two)
        self.assertIs(reg[""], func_two)
