"""A regra de entrada depois do merge da `papeis-e-abas` com a `porta-de-entrada`.

Cada página de entrada define a aba no `on_load`; a aba só vale DEPOIS de a
senha ser confirmada. Equipe pela entrada de clientes, ou cliente pela
entrada da equipe, é recusado sem guardar a sessão; conta sem papel também.
"""

import asyncio
import unittest
from types import SimpleNamespace
from unittest import mock

from petbits import xano
from petbits.states.auth_state import AuthState


def entrar(aba: str, papel: str, senha_certa: bool = True) -> SimpleNamespace:
    s = SimpleNamespace(
        aba=aba, login_email="a@b.com", login_senha="x", erro="", enviando=False,
        token="", usuario_nome="", usuario_papel="", sessao_validada=False,
        sessao_expirou=False, redirecionou=None,
    )
    s._guardar = lambda token, perfil: AuthState._guardar(s, token, perfil)

    async def falso_entrar(email, senha):
        if not senha_certa:
            raise xano.CredenciaisInvalidas("E-mail ou senha incorretos.")
        return {"authToken": "t"}

    async def falso_perfil(token):
        return {"name": "Fulano", "role": papel}

    async def rodar():
        with mock.patch.object(xano, "entrar", falso_entrar), \
                mock.patch.object(xano, "usuario_atual", falso_perfil), \
                mock.patch("reflex.redirect", lambda rota: ("redirect", rota)):
            async for evento in AuthState.entrar.fn(s):
                if isinstance(evento, tuple) and evento[0] == "redirect":
                    s.redirecionou = evento[1]

    asyncio.run(rodar())
    return s


class Entrada(unittest.TestCase):
    def test_cliente_pela_entrada_de_clientes(self):
        s = entrar("cliente", "member")
        self.assertEqual((s.token, s.redirecionou), ("t", "/"))

    def test_gerencia_e_equipe_pela_entrada_da_equipe(self):
        for papel in ("admin", "staff"):
            s = entrar("colaborador", papel)
            self.assertEqual((s.token, s.redirecionou), ("t", "/equipe"), papel)

    def test_equipe_pela_entrada_de_clientes_e_recusada(self):
        s = entrar("cliente", "staff")
        self.assertEqual(s.token, "")
        self.assertIn("entrada da equipe", s.erro)

    def test_cliente_pela_entrada_da_equipe_e_recusado(self):
        s = entrar("colaborador", "member")
        self.assertEqual(s.token, "")
        self.assertIn("entrada de clientes", s.erro)

    def test_conta_sem_papel_e_recusada(self):
        s = entrar("cliente", "")
        self.assertEqual(s.token, "")
        self.assertIn("sem perfil", s.erro)

    def test_senha_errada_tem_a_mesma_recusa_nas_duas_entradas(self):
        a = entrar("cliente", "staff", senha_certa=False).erro
        b = entrar("colaborador", "staff", senha_certa=False).erro
        self.assertEqual(a, b)

    def test_cada_pagina_define_a_aba(self):
        s = SimpleNamespace(aba="", enviando=True, token="", usuario_papel="")
        s.redirecionar_se_logado = lambda: AuthState.redirecionar_se_logado.fn(s)
        AuthState.abrir_entrada_da_equipe.fn(s)
        self.assertEqual(s.aba, "colaborador")
        AuthState.abrir_entrada_de_clientes.fn(s)
        self.assertEqual(s.aba, "cliente")


if __name__ == "__main__":
    unittest.main()
