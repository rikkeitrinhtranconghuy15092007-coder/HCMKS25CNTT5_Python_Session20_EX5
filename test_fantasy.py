import unittest
from main import calc_actual_withdrawal

class TestCalcActualWithdrawal(unittest.TestCase):

    def test_normal_withdrawal(self):
        self.assertEqual(calc_actual_withdrawal(100), 90.0)
        self.assertEqual(calc_actual_withdrawal(500), 450.0)

    def test_negative_amount_raises_error(self):
        with self.assertRaises(ValueError):
            calc_actual_withdrawal(-50)

    def test_zero_amount(self):
        self.assertEqual(calc_actual_withdrawal(0), 0.0)


if __name__ == '__main__':
    unittest.main()