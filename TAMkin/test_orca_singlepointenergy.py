import unittest


class TestOrcaSPE(unittest.TestCase):

    def test_orca_spe(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_spe_zpe(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()

