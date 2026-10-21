"""Foto do produto no cadastro e removível (change `foto-do-produto-na-mao`)."""

import asyncio
import unittest
from unittest import mock

from petbits import xano


class RemoverFotoTest(unittest.TestCase):
    def test_caminho_e_inexistente(self):
        requisitar = mock.AsyncMock(return_value={"id": 11, "foto": None})
        with mock.patch.object(xano, "_requisitar", requisitar):
            asyncio.run(xano.remover_foto_do_produto(11, token="t"))
        self.assertEqual(requisitar.call_args.args[:2], ("DELETE", "/equipe/produtos/11/foto"))
        with mock.patch.object(xano, "_requisitar", mock.AsyncMock(return_value=None)):
            with self.assertRaises(xano.NaoEncontrado):
                asyncio.run(xano.remover_foto_do_produto(999, token="t"))


if __name__ == "__main__":
    unittest.main()


class CadastroComFotoTest(unittest.TestCase):
    """A foto escolhida no cadastro vai com o id do produto novo (D2)."""

    def _estado(self):
        from types import SimpleNamespace
        from petbits.states.equipe_state import EquipeState

        s = SimpleNamespace(prd_nome="Bolinha", prd_preco="12,50", prd_estoque="3",
                            prd_descricao="", prd_categoria="brinquedo", prd_marca="",
                            prd_unidade="", prd_editando=None, prd_erro="", salvando=False,
                            prd_dialogo=True, _foto_pendente=b"imagem", _extensao_pendente="webp")

        async def token():
            return "t"

        async def carregar():
            return None

        s._token_de_equipe = token
        s.carregar_produtos = carregar
        return s, EquipeState

    def _rodar(self, s, EquipeState):
        async def tudo():
            async for _ in EquipeState.salvar_produto.fn(s):
                pass
        asyncio.run(tudo())

    def test_envia_a_foto_com_o_id_novo(self):
        s, EquipeState = self._estado()
        criar = mock.AsyncMock(return_value={"id": 77})
        enviar = mock.AsyncMock(return_value={"url": "https://x"})
        with mock.patch.object(xano, "criar_produto", criar), \
                mock.patch.object(xano, "enviar_foto_do_produto", enviar):
            self._rodar(s, EquipeState)
        self.assertEqual(enviar.call_args.args[:3], (77, b"imagem", "webp"))
        self.assertEqual(s._foto_pendente, b"")
        self.assertFalse(s.prd_dialogo)

    def test_sem_foto_nao_envia(self):
        s, EquipeState = self._estado()
        s._foto_pendente = b""
        enviar = mock.AsyncMock()
        with mock.patch.object(xano, "criar_produto", mock.AsyncMock(return_value={"id": 78})), \
                mock.patch.object(xano, "enviar_foto_do_produto", enviar):
            self._rodar(s, EquipeState)
        enviar.assert_not_called()
