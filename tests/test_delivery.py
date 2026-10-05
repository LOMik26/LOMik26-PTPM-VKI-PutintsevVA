import unittest
#c:/python314/python.exe -m unittest discover -s tests -p "test_*.py" -v
from Delivery import calculate_delivery_cost


class TestDeliveryCalculator(unittest.TestCase):
    def test_invalid_weight_is_rejected(self):
        result = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_invalid_distance_is_rejected(self):
        result = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_invalid_package_type_is_rejected(self):
        result = calculate_delivery_cost(1.0, 100, "неизвестный")
        self.assertEqual(result, (-1, "0000-00-00"))

    def test_normal_package_cost_and_delivery_date(self):
        result = calculate_delivery_cost(2.0, 1000, "обычный")
        self.assertEqual(result[0], 5200)
        self.assertEqual(result[1], "2026-09-05")

    def test_fragile_package_has_surcharge(self):
        result = calculate_delivery_cost(2.0, 1000, "хрупкий")
        self.assertEqual(result[0], 5500)

    def test_dangerous_package_has_large_surcharge(self):
        result = calculate_delivery_cost(2.0, 1000, "опасный")
        self.assertEqual(result[0], 6200)

    def test_express_discount_reduces_cost(self):
        result = calculate_delivery_cost(2.0, 1000, "обычный", is_express=True)
        self.assertEqual(result[0], 2600)

    def test_weight_5_to_20_gets_20_percent_increase(self):
        result = calculate_delivery_cost(10.0, 1000, "обычный")
        self.assertEqual(result[0], 6240)

    def test_weight_20_or_more_gets_50_percent_increase(self):
        result = calculate_delivery_cost(20.0, 1000, "обычный")
        self.assertEqual(result[0], 7800)

    def test_express_distance_uses_half_the_delivery_days(self):
        result = calculate_delivery_cost(2.0, 1500, "обычный", is_express=True)
        self.assertEqual(result[1], "2026-09-04")

    def test_minimum_delivery_day_is_one(self):
        result = calculate_delivery_cost(1.0, 1, "обычный")
        self.assertEqual(result[1], "2026-09-04")


if __name__ == "__main__":
    unittest.main()
