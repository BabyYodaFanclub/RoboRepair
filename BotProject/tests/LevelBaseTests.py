import unittest

from LevelBase import LevelBase


class TestLevelBase(unittest.TestCase):
    def test_param_list(self):
        val_dict: dict = LevelBase.extract_line_params('[w=abc,de] [i=2] [b] ADF W$TQ §$TV§$')
        self.assertTrue('w' in val_dict)
        self.assertTrue('i' in val_dict)
        self.assertTrue('b' in val_dict)
        self.assertEqual(['abc', 'de'], val_dict['w'])
        self.assertEqual(['2'], val_dict['i'])
        self.assertEqual(None, val_dict['b'])

    def test_no_params(self):
        val_dict: dict = LevelBase.extract_line_params('[i]')
        self.assertTrue('i' in val_dict)
        self.assertEqual(None, val_dict['i'])

    def test_multichar_params(self):
        val_dict: dict = LevelBase.extract_line_params('[it]')
        self.assertTrue('it' in val_dict)
        self.assertEqual(None, val_dict['it'])


if __name__ == '__main__':
    unittest.main()
