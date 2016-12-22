import unittest

import paka.funcreg


class NameRegistryTest(unittest.TestCase):

    def make_reg(self, *args, **kwargs):
        return paka.funcreg.NameRegistry(*args, **kwargs)

    def test_decorator_with_name(self):
        name = "other_func"
        reg = self.make_reg()
        @reg.register(name)
        def tst_me():
            return 123
        self.assertIs(reg[name], tst_me)

    def test_decorator_without_name(self):
        reg = self.make_reg()
        @reg.register
        def tst_me():
            return 123
        self.assertIs(reg["tst_me"], tst_me)

    def test_functional_with_name(self):
        name = "do_something"
        reg = self.make_reg()
        def _some_func():
            return 321
        reg.register(_some_func, name)
        self.assertIs(reg[name], _some_func)

    def test_functional_without_name(self):
        reg = self.make_reg()
        def _other_func():
            return 321
        reg.register(_other_func)
        self.assertIs(reg["_other_func"], _other_func)

    def test_multiple_registries(self):
        reg1 = self.make_reg()
        reg2 = self.make_reg()
        reg3 = self.make_reg()
        @reg2.register
        def func_for_second():
            return 321 + 2
        @reg1.register
        def func_for_first():
            return 321 + 1
        @reg3.register("wtf")
        def func_for_third():
            return 321 + 3
        self.assertIs(reg1["func_for_first"], func_for_first)
        self.assertIs(reg2["func_for_second"], func_for_second)
        self.assertIs(reg3["wtf"], func_for_third)
        with self.assertRaises(KeyError):
            reg2["wtf"]()
        with self.assertRaises(KeyError):
            reg1["wtf"]()
        with self.assertRaises(KeyError):
            reg2["func_for_first"]()
        with self.assertRaises(KeyError):
            reg3["func_for_first"]()
        with self.assertRaises(KeyError):
            reg1["func_for_second"]()
        with self.assertRaises(KeyError):
            reg3["func_for_second"]()

    def test_default(self):
        def func_one():
            return 1
        def func_two():
            return 2
        reg = self.make_reg(default=func_two)
        reg.register(func_one)
        self.assertIs(reg["func_one"], func_one)
        self.assertIs(reg["random thing here"], func_two)
        self.assertIs(reg[""], func_two)
