"""O painel da clínica (change `painel-do-dia`)."""

import unittest
from datetime import date

from petbits import agenda
from petbits.painel import (agenda_do_dia, estoque_baixo, estoque_do_painel, nivel_do_estoque,
                            pedidos_esperando)

NOVE = agenda.inicio_do_dia_ms(date(2026, 10, 21)) + 9 * 3600 * 1000
QUINZE = NOVE + 6 * 3600 * 1000


class AgendaDoDiaTest(unittest.TestCase):
    REGISTROS = [
        {"id": 2, "inicio": QUINZE, "situacao": "concluido", "pet_nome": "Nina",
         "pet_especie": "Gato", "tutor_nome": "Ana", "servico_nome": "Consulta",
         "profissional_nome": "Dr. Caio"},
        {"id": 1, "inicio": NOVE, "situacao": "marcado", "pet_nome": "Mel",
         "pet_especie": "", "tutor_nome": None, "servico_nome": "Banho",
         "profissional_nome": "Juliana"},
    ]

    def test_ordem_de_horario(self):
        self.assertEqual([i["id"] for i in agenda_do_dia(self.REGISTROS)], [1, 2])

    def test_linha(self):
        nove, quinze = agenda_do_dia(self.REGISTROS)
        self.assertEqual(nove["horario"], "09:00")
        self.assertEqual(nove["animal"], "Mel")
        self.assertEqual(nove["tutor"], "-")
        self.assertEqual(nove["situacao"], "Marcado")
        self.assertFalse(nove["concluido"])
        self.assertEqual(quinze["animal"], "Nina · Gato")
        self.assertTrue(quinze["concluido"])

    def test_resposta_estranha(self):
        self.assertEqual(agenda_do_dia(None), [])
        self.assertEqual(agenda_do_dia([]), [])


class PedidosEsperandoTest(unittest.TestCase):
    def test_tres_situacoes(self):
        self.assertEqual(pedidos_esperando({"pedidos_pendentes": 2, "pedidos_pagos": 1}),
                         {"pendente": 2, "pago": 1, "pronto_retirada": 0})

    def test_sem_dados(self):
        self.assertEqual(pedidos_esperando(None),
                         {"pendente": 0, "pago": 0, "pronto_retirada": 0})



class EstoqueTest(unittest.TestCase):
    """Estoque baixo (change `estoque-baixo`)."""

    PRODUTOS = [
        {"nome": "Ração", "ativo": True, "_estoque": "40"},
        {"nome": "Arranhador", "ativo": True, "_estoque": "4"},
        {"nome": "Coleira", "ativo": True, "_estoque": "0"},
        {"nome": "Inativo", "ativo": False, "_estoque": "0"},
        {"nome": "Bolinha", "ativo": True, "_estoque": "5"},
    ]

    def test_so_ativos_ate_5_esgotados_primeiro(self):
        self.assertEqual([p["nome"] for p in estoque_baixo(self.PRODUTOS)],
                         ["Coleira", "Arranhador", "Bolinha"])

    def test_nivel(self):
        self.assertEqual([nivel_do_estoque(n) for n in (0, 1, 5, 6)],
                         ["esgotado", "baixo", "baixo", "ok"])

    def test_contagens_do_painel(self):
        self.assertEqual(estoque_do_painel({"produtos_esgotados": 2, "produtos_acabando": 3}),
                         {"esgotados": 2, "acabando": 3})
        self.assertEqual(estoque_do_painel(None), {"esgotados": 0, "acabando": 0})


if __name__ == "__main__":
    unittest.main()
