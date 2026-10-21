"""Não compareceu (change `nao-compareceu`)."""

import asyncio
import unittest
from unittest import mock

from petbits import rotulos, xano


class NaoCompareceuTest(unittest.TestCase):
    def test_rotulo(self):
        self.assertEqual(rotulos.SITUACOES_AGENDAMENTO["faltou"], "Não compareceu")

    def test_inexistente_vira_nao_encontrado(self):
        with mock.patch.object(xano, "_requisitar", mock.AsyncMock(return_value=None)):
            with self.assertRaises(xano.NaoEncontrado):
                asyncio.run(xano.marcar_falta(999, token="t"))

    def test_caminho(self):
        requisitar = mock.AsyncMock(return_value={"id": 1, "situacao": "faltou"})
        with mock.patch.object(xano, "_requisitar", requisitar):
            asyncio.run(xano.marcar_falta(1, token="t"))
        self.assertEqual(requisitar.call_args.args[:2], ("POST", "/equipe/agendamentos/1/falta"))


if __name__ == "__main__":
    unittest.main()
