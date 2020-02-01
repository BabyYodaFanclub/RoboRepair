import unittest

from LevelBase import LevelBase


class TestLevelBase(unittest.TestCase):
    def test_param_list(self):
        val_dict: dict = LevelBase.extract_line_params('[i=2] [d] *Calculating*')
        self.assertTrue('w' in val_dict)
        self.assertEqual(['abc', 'de'], val_dict['w'])

    def test_no_params(self):
        val_dict: dict = LevelBase.extract_line_params('[i]')
        self.assertTrue('i' in val_dict)
        self.assertEqual(None, val_dict['i'])


if __name__ == '__main__':
    unittest.main()
