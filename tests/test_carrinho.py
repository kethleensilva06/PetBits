"""O carrinho guardado no navegador (change `carrinho-guardado`)."""

import unittest

from petbits.carrinho import escrever, ler


class CarrinhoTest(unittest.TestCase):
    def test_ida_e_volta(self):
        self.assertEqual(ler(escrever({"3": 2, "7": 1})), {"3": 2, "7": 1})

    def test_vazio_e_quebrado(self):
        for texto in ("", "{", "null", "[1,2]", '"x"'):
            self.assertEqual(ler(texto), {}, texto)

    def test_descarta_o_que_nao_serve(self):
        texto = '{"3": 2, "abc": 1, "4": 0, "5": -1, "6": 1.5, "7": true, "8": "2", "9": 500}'
        self.assertEqual(ler(texto), {"3": 2})

    def test_escrever_tira_zeros(self):
        self.assertEqual(escrever({"3": 0, "4": 1}), '{"4":1}')


if __name__ == "__main__":
    unittest.main()
