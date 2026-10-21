"""A equipe edita o tutor (change `editar-tutor`)."""

import asyncio
import unittest
from types import SimpleNamespace
from unittest import mock

from petbits import xano
from petbits.states.equipe_state import EquipeState


class ClienteTest(unittest.TestCase):
    def test_caminho_e_inexistente(self):
        requisitar = mock.AsyncMock(return_value={"id": 48})
        with mock.patch.object(xano, "_requisitar", requisitar):
            asyncio.run(xano.alterar_tutor(48, {"telefone": "x"}, token="t"))
        self.assertEqual(requisitar.call_args.args[:2], ("PATCH", "/equipe/tutores/48"))
        with mock.patch.object(xano, "_requisitar", mock.AsyncMock(return_value=None)):
            with self.assertRaises(xano.NaoEncontrado):
                asyncio.run(xano.alterar_tutor(999, {"telefone": "x"}, token="t"))


class FormularioTest(unittest.TestCase):
    def _estado(self):
        s = SimpleNamespace(tut_erro="", tut_editando=None, tut_original={}, tut_dialogo=False,
                            tut_nome="", tut_documento="", tut_telefone="", tut_email="",
                            tut_endereco="")
        s._dados_do_form_tut = lambda: EquipeState._dados_do_form_tut(s)
        return s

    def test_editar_preenche_e_guarda_o_original(self):
        s = self._estado()
        EquipeState.editar_tutor.fn(s, {"id": 48, "nome": "Bia", "_documento": "787.126.426-57",
                                        "_telefone": "(11) 99547-3625", "_email": "b@x.com",
                                        "_endereco": "Rua A"})
        self.assertEqual(s.tut_editando, 48)
        self.assertTrue(s.tut_dialogo)
        self.assertEqual(s.tut_original["documento"], "78712642657")
        self.assertEqual(s.tut_original["email"], "b@x.com")


if __name__ == "__main__":
    unittest.main()
