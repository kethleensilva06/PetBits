"""Resumo e exportação dos pedidos (change `resumo-dos-pedidos`)."""

import csv
import io
import unittest

from petbits.relatorio import COLUNAS, csv_de_pedidos, resumo_de_pedidos

PEDIDOS = [
    {"id": 14, "quando": "Ter, 13/10/2026", "_cliente_nome": "Ana Ribeiro", "situacao": "Pago",
     "entrega": "Retirada", "pagamento": "Na loja", "origem": "Site", "_total": 39.9,
     "_cancelado": False, "cliente": "Ana Ribeiro · (11) 98888-7777",
     "itens": [{"texto": "1 × Arranhador"}, {"texto": "2 × Bolinha; azul"}]},
    {"id": 20, "quando": "Ter, 20/10/2026", "_cliente_nome": "Ana Ribeiro",
     "situacao": "Cancelado", "_total": 24.9, "_cancelado": True, "itens": []},
]


class ResumoTest(unittest.TestCase):
    def test_cancelado_nao_soma(self):
        self.assertEqual(resumo_de_pedidos(PEDIDOS),
                         "2 pedidos · R$ 39,90 (cancelados não entram no total)")

    def test_um_e_nenhum(self):
        self.assertEqual(resumo_de_pedidos(PEDIDOS[:1]), "1 pedido · R$ 39,90")
        self.assertEqual(resumo_de_pedidos([]), "")


class CsvTest(unittest.TestCase):
    def setUp(self):
        self.texto = csv_de_pedidos(PEDIDOS)
        self.linhas = list(csv.reader(io.StringIO(self.texto.lstrip("\ufeff")), delimiter=";"))

    def test_bom_cabecalho_e_linhas(self):
        self.assertTrue(self.texto.startswith("\ufeff"))
        self.assertEqual(tuple(self.linhas[0]), COLUNAS)
        self.assertEqual(len(self.linhas), 3)

    def test_valores_e_escape(self):
        self.assertEqual(self.linhas[1][-1], "39,90")
        self.assertEqual(self.linhas[1][7], "1 × Arranhador | 2 × Bolinha; azul")

    def test_sem_telefone(self):
        self.assertNotIn("98888", self.texto)


if __name__ == "__main__":
    unittest.main()
