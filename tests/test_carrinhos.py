"""Carrinhos da loja e do balcão (changes `loja` e `venda-no-balcao`).

O total que a tela soma é estimativa — o que vale é o que o servidor calcula —,
mas o carrinho não pode pedir mais do que o estoque nem oferecer produto que
não está à venda.
"""

import unittest
from types import SimpleNamespace

from petbits.states.equipe_state import EquipeState
from petbits.states.loja_state import LojaState, reais


class _LojaFalsa(SimpleNamespace):
    """O carrinho guardado no navegador e o derivado (change `carrinho-guardado`)."""

    carrinho = property(LojaState.computed_vars["carrinho"].fget)
    _gravar = LojaState._gravar


class CarrinhoDaLoja(unittest.TestCase):
    def setUp(self):
        self.s = _LojaFalsa(
            produtos=[
                {"id": 1, "nome": "Ração", "_preco": 49.9, "_estoque": 2},
                {"id": 2, "nome": "Bolinha", "_preco": 12.5, "_estoque": 10},
            ],
            carrinho_salvo="",
            aviso="",
        )

    def test_para_no_estoque(self):
        for _ in range(3):
            LojaState.adicionar.fn(self.s, 1)
        self.assertEqual(self.s.carrinho, {"1": 2})

    def test_mais_desabilita_no_limite(self):
        LojaState.adicionar.fn(self.s, 1)
        LojaState.adicionar.fn(self.s, 1)
        itens = {i["id"]: i for i in LojaState.itens_do_carrinho.fget(self.s)}
        self.assertFalse(itens["1"]["pode_mais"])

    def test_tirar_o_ultimo_remove_o_item(self):
        LojaState.adicionar.fn(self.s, 2)
        LojaState.tirar.fn(self.s, "2")
        self.assertEqual(self.s.carrinho, {})

    def test_total_estimado(self):
        LojaState.adicionar.fn(self.s, 1)
        LojaState.adicionar.fn(self.s, 1)
        LojaState.adicionar.fn(self.s, 2)
        self.assertEqual(LojaState.total_estimado.fget(self.s), "R$ 112,30")

    def test_fica_guardado(self):
        LojaState.adicionar.fn(self.s, 2)
        self.assertEqual(self.s.carrinho_salvo, '{"2":1}')


class CarrinhoDoBalcao(unittest.TestCase):
    def setUp(self):
        self.s = SimpleNamespace(
            produtos=[
                {"id": 1, "nome": "Ração", "ativo": True, "_estoque": "2", "_preco": "49.9"},
                {"id": 2, "nome": "Inativo", "ativo": False, "_estoque": "5", "_preco": "10"},
                {"id": 3, "nome": "Sem estoque", "ativo": True, "_estoque": "0", "_preco": "10"},
            ],
            balcao_carrinho={},
            balcao_aviso="",
        )

    def test_so_oferece_ativos_com_estoque(self):
        nomes = [p["nome"] for p in EquipeState.produtos_a_venda.fget(self.s)]
        self.assertEqual(nomes, ["Ração"])

    def test_para_no_estoque_e_soma(self):
        for _ in range(3):
            EquipeState.balcao_adicionar.fn(self.s, 1)
        self.assertEqual(self.s.balcao_carrinho, {"1": 2})
        self.assertEqual(EquipeState.total_balcao.fget(self.s), "R$ 99,80")


class Reais(unittest.TestCase):
    def test_formato(self):
        self.assertEqual(reais(1234.5), "R$ 1.234,50")
        self.assertEqual(reais(0), "R$ 0,00")
        self.assertEqual(reais(None), "-")


if __name__ == "__main__":
    unittest.main()
