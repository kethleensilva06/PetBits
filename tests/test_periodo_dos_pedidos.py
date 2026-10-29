"""A lista de Pedidos da equipe por período (change `indices-e-paginacao`)."""

import asyncio
import unittest
from types import SimpleNamespace
from unittest import mock

from petbits import guardados, xano
from petbits.states.equipe_state import PERIODO_PADRAO, PERIODOS, EquipeState


def parametros(situacao="", dias=0):
    enviados = {}

    async def falso(metodo, caminho, **kw):
        enviados.update(kw.get("params") or {})
        return {"pedidos": [], "itens": []}

    with mock.patch.object(xano, "_requisitar", falso), \
            mock.patch.object(guardados, "ligado", False):
        asyncio.run(xano.pedidos_da_clinica(situacao, dias, token="t"))
    return enviados


class PeriodoDosPedidos(unittest.TestCase):
    def test_padrao_e_noventa_dias(self):
        self.assertEqual(PERIODO_PADRAO, "90")
        self.assertEqual(PERIODOS, ("90", "30", "0"))

    def test_dias_vai_ao_xano(self):
        self.assertEqual(parametros(dias=90), {"dias": 90})
        self.assertEqual(parametros("pendente", 30), {"situacao": "pendente", "dias": 30})

    def test_todo_o_periodo_nao_manda_dias(self):
        self.assertEqual(parametros(), {})

    def test_vindo_do_painel_e_todo_o_periodo(self):
        s = SimpleNamespace(filtro_pedidos="todos", periodo_pedidos="90")
        with mock.patch("reflex.redirect", lambda rota: rota):
            EquipeState.abrir_pedidos.fn(s, "pendente")
        self.assertEqual((s.filtro_pedidos, s.periodo_pedidos), ("pendente", "0"))


if __name__ == "__main__":
    unittest.main()
