"""O carrinho guardado no navegador (change `carrinho-guardado`)."""

import unittest

from petbits.carrinho import ajustar_ao_estoque, escrever, ler, somar


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



class ComprarDeNovoTest(unittest.TestCase):
    def test_soma_ao_que_ja_esta(self):
        itens = [{"id_produto": 11, "quantidade": 2}, {"id_produto": 9, "quantidade": 1},
                 {"id_produto": 0, "quantidade": 3}]
        self.assertEqual(somar({"11": 1}, itens), {"11": 3, "9": 1})

    def test_soma_respeita_o_maximo(self):
        self.assertEqual(somar({"11": 98}, [{"id_produto": 11, "quantidade": 5}]), {"11": 99})

    def test_ajuste_sem_mudanca(self):
        self.assertEqual(ajustar_ao_estoque({"1": 2}, {"1": 5}), ({"1": 2}, ""))

    def test_ajuste_com_aviso(self):
        carrinho, aviso = ajustar_ao_estoque({"1": 5, "2": 1, "3": 1}, {"1": 3, "2": 0})
        self.assertEqual(carrinho, {"1": 3})
        self.assertEqual(aviso, "2 itens saíram do carrinho e 1 item teve a quantidade "
                                "reduzida: sem estoque ou fora da loja.")


if __name__ == "__main__":
    unittest.main()
