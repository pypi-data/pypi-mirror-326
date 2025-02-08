# tests/test_input_utils.py

import unittest
from unittest.mock import patch
from nummyint.input_utils import obter_numero_inteiro

class TestInputUtils(unittest.TestCase):
    @patch('builtins.input', side_effect=['abc', '25'])
    def test_obter_numero_inteiro_valido(self, mock_input):
        resultado = obter_numero_inteiro("Digite um número: ")
        self.assertEqual(resultado, 25)

    @patch('builtins.input', side_effect=['-10'])
    def test_obter_numero_inteiro_negativo(self, mock_input):
        resultado = obter_numero_inteiro("Digite um número: ")
        self.assertEqual(resultado, -10)

if __name__ == '__main__':
    unittest.main()