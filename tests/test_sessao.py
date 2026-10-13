"""A guarda de sessão da área de cliente (change `acabamentos`, D1).

Uma função só (`sessao.token_de_cliente`) no lugar de três cópias: sem sessão
leva à entrada (ou à página inicial, na casa do cliente), sessão expirada
sempre à entrada com o aviso, e conta de equipe à gerência — sempre antes de
qualquer requisição.
"""

import asyncio
import unittest
from types import SimpleNamespace

from petbits.states.agenda_state import AgendaState
from petbits.states.loja_state import LojaState
from petbits.states.pet_state import PetState
from petbits.states.sessao import SemSessao


def destino(State, token="", expirou=False, papel=""):
    auth = SimpleNamespace(token=token, sessao_expirou=expirou, usuario_papel=papel)

    async def get_state(_):
        return auth

    async def rodar():
        try:
            await State._token(SimpleNamespace(get_state=get_state))
        except SemSessao as erro:
            return erro.destino
        return "segue"

    return asyncio.run(rodar())


class GuardaDeCliente(unittest.TestCase):
    def test_visitante(self):
        self.assertEqual(destino(PetState), "/boas-vindas")
        self.assertEqual(destino(AgendaState), "/entrar")
        self.assertEqual(destino(LojaState), "/entrar")

    def test_sessao_expirada_vai_para_a_entrada_com_aviso(self):
        for State in (PetState, AgendaState, LojaState):
            self.assertEqual(destino(State, expirou=True), "/entrar")

    def test_equipe_vai_para_a_gerencia(self):
        for State in (PetState, AgendaState, LojaState):
            for papel in ("admin", "staff"):
                self.assertEqual(destino(State, "t", papel=papel), "/equipe")

    def test_cliente_segue(self):
        for State in (PetState, AgendaState, LojaState):
            self.assertEqual(destino(State, "t", papel="member"), "segue")


class Saudacao(unittest.TestCase):
    def nome(self, completo):
        from petbits.states.auth_state import AuthState
        return AuthState.primeiro_nome.fget(SimpleNamespace(usuario_nome=completo))

    def test_nome_com_titulo(self):
        self.assertEqual(self.nome("Dr. Otavio Lins"), "Otavio")
        self.assertEqual(self.nome("Dra. Helena Marques"), "Helena")

    def test_nome_sem_titulo(self):
        self.assertEqual(self.nome("Ana Ribeiro"), "Ana")

    def test_so_o_titulo_ou_vazio(self):
        self.assertEqual(self.nome("Dr."), "Dr.")
        self.assertEqual(self.nome(""), "")


if __name__ == "__main__":
    unittest.main()
