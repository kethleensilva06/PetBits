"""O cliente cancela o próprio pedido (change `cliente-cancela-pedido`)."""

import asyncio
import unittest
from unittest import mock

from petbits import xano


class CancelarPedidoTest(unittest.TestCase):
    def test_alheio_ou_inexistente_vira_nao_encontrado(self):
        """O 404 chega como None; a tela não pode mostrar como cancelado."""
        with mock.patch.object(xano, "_requisitar", mock.AsyncMock(return_value=None)):
            with self.assertRaises(xano.NaoEncontrado):
                asyncio.run(xano.cancelar_pedido(19, token="t"))

    def test_caminho_do_endpoint(self):
        requisitar = mock.AsyncMock(return_value={"id": 20, "situacao": "cancelado"})
        with mock.patch.object(xano, "_requisitar", requisitar):
            asyncio.run(xano.cancelar_pedido(20, token="t"))
        self.assertEqual(requisitar.call_args.args[:2], ("POST", "/pedido/20/cancelar"))


if __name__ == "__main__":
    unittest.main()
