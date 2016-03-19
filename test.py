import unittest

from safe_eval import safe_eval

math_namespace = {}
math_namespace.update(__import__("math").__dict__)

class TestSafeEval_Secure(unittest.TestCase):
    """
    Every one of these tests must evaluate and evaluate to a correct value.
    """

    def test_logic_01(self):
        self.assertEqual(safe_eval("bool(2)"), True)

    def test_logic_02(self):
        self.assertEqual(safe_eval("True is not False"), True)

    def test_math_01(self):
        self.assertEqual(safe_eval("1 + 1"), 2)

    def test_math_02(self):
        self.assertEqual(safe_eval("2 ** 13 // 4"), 2048)

    def test_math_module_01(self):
        self.assertEqual(safe_eval("sqrt(9)", globals=math_namespace), 3)


class TestSafeEval_Insecure(unittest.TestCase):
    """
    Every one of these tests must raise a runtime error
    and should _never_ execute.

    Note that these tests shouldn't break the system if they _do_ execute.
    """

    def _expr_fails(self, expr):
        with self.assertRaises(RuntimeError):
            safe_eval(expr)

    def test_open_01(self):
        self._expr_fails("open()")

    def test_open_02(self):
        self._expr_fails("open('test', 'r')")

    def test_import_01(self):
        self._expr_fails("__import__('os')")

    def test_attr_01(self):
        self._expr_fails("''.__class__")


if __name__ == '__main__':
    unittest.main()

