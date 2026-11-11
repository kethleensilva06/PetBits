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
        self.assertEqual(destino(PetState), "/")
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


class FimDaSessao(unittest.TestCase):
    """A validade de 12 horas e o "Manter conectado" (change
    `sessao-lembrada`, D3)."""

    def fim(self, token="t", expira_em="1000", lembrar="1", aberto="", agora=500):
        from petbits.states.auth_state import fim_da_sessao
        return fim_da_sessao(token, expira_em, lembrar, aberto, agora)

    def test_mantendo_conectado_vale_mesmo_sem_o_cookie(self):
        self.assertEqual(self.fim(), "")

    def test_passou_da_validade(self):
        self.assertEqual(self.fim(agora=1000), "venceu")
        self.assertEqual(self.fim(lembrar="", aberto="1", agora=2000), "venceu")

    def test_sem_manter_vale_enquanto_o_navegador_esta_aberto(self):
        self.assertEqual(self.fim(lembrar="", aberto="1"), "")

    def test_sem_manter_navegador_fechado(self):
        self.assertEqual(self.fim(lembrar="", aberto=""), "fechou")

    def test_sessao_antiga_sem_validade(self):
        self.assertEqual(self.fim(expira_em=""), "fechou")
        self.assertEqual(self.fim(expira_em="lixo"), "fechou")

    def test_sem_token_nada_a_encerrar(self):
        self.assertEqual(self.fim(token="", expira_em=""), "")

    def test_doze_horas(self):
        from petbits.states.auth_state import DURACAO_DA_SESSAO
        self.assertEqual(DURACAO_DA_SESSAO, 12 * 60 * 60)
