"""O script de ponta a ponta contra um Xano simulado (change `ampliar-ponta-a-ponta`, D3).

O simulador aplica as regras das specs em memória, sem rede. Ele só existe
para testar o script: com o backend certo tudo passa; com uma regra quebrada
de propósito, o script acusa e sai 1. Quem confere o Xano de verdade é a
rodada real do script.
"""

import asyncio
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from petbits import agenda, contas_de_teste, rotulos, xano
from petbits.pedidos import proximas

RAIZ = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "verificar_ponta_a_ponta", RAIZ / "scripts" / "verificar_ponta_a_ponta.py")
v = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(v)

SEGREDO = "SenhaUltraSecreta9"
CATEGORIAS_PRODUTO = set(rotulos.CATEGORIAS_PRODUTO)
CATEGORIAS_SERVICO = set(rotulos.CATEGORIAS_SERVICO)


def recusar(msg="recusado"):
    raise xano.DadosInvalidos(msg, status=400)


class XanoSimulado:
    """As regras das specs, em memória. `quebrar` desliga uma delas."""

    def __init__(self, papel_equipe="staff", quebrar="", endereco="Rua das Flores, 10"):
        self.papel = {"eq": papel_equipe, "cl": "member", "cl2": "member"}
        self.fichas = {"cl": {"id": 7, "endereco": endereco}, "cl2": {"id": 8, "endereco": ""}}
        self.pets = {1: "cl", 2: "cl2"}
        self.produtos, self.pedidos, self.ag = {}, {}, {}
        self.quebrar = quebrar
        self.n = 100

    def _id(self):
        self.n += 1
        return self.n

    def _so_equipe(self, t):
        if not xano.eh_equipe(self.papel[t]):
            raise xano.SemPermissao("Acesso restrito à equipe", status=403)

    # sessão
    async def entrar(self, email, senha):
        assert senha == SEGREDO
        return {"authToken": email.split("@")[0]}

    async def usuario_atual(self, t):
        return {"role": self.papel[t]}

    # equipe
    async def agenda_da_clinica(self, dia, *, token):
        self._so_equipe(token)
        return []

    async def painel_equipe(self, *, token):
        self._so_equipe(token)
        return {}

    async def listar_tutores_da_clinica(self, *, token):
        self._so_equipe(token)
        return []

    async def pedidos_da_clinica(self, situacao="", *, token):
        self._so_equipe(token)
        return {"pedidos": list(self.pedidos.values()), "itens": []}

    async def criar_colaborador(self, dados, *, token):
        self._so_equipe(token)
        if not xano.eh_gerencia(self.papel[token]) and self.quebrar != "gerencia":
            raise xano.SemPermissao("Só a gerência", status=403)
        return {"id": self._id(), **dados}

    async def listar_servicos(self, *, token):
        self._so_equipe(token)
        return [{"id": 9, "categoria": "banho_tosa", "duracao_minutos": 60}]

    async def atualizar_servico(self, i, dados, *, token):
        self._so_equipe(token)
        if "categoria" in dados and dados["categoria"] not in CATEGORIAS_SERVICO:
            recusar("Categoria inválida")
        return {"id": i, **dados}

    # catálogo
    def _confere_produto(self, d):
        if "preco" in d and d["preco"] <= 0:
            recusar("Preço deve ser maior que zero")
        if "estoque" in d and d["estoque"] < 0:
            recusar("Estoque não pode ser negativo")
        if "categoria" in d and d["categoria"] not in CATEGORIAS_PRODUTO:
            recusar("Categoria inválida")

    async def criar_produto(self, d, *, token):
        self._so_equipe(token)
        self._confere_produto(d)
        i = self._id()
        self.produtos[i] = {"id": i, **d, "ativo": True}
        return self.produtos[i]

    async def listar_produtos(self, *, token):
        self._so_equipe(token)
        return [dict(p) for p in self.produtos.values()]

    async def atualizar_produto(self, i, d, *, token):
        self._so_equipe(token)
        self._confere_produto(d)
        self.produtos[i].update(d)
        return self.produtos[i]

    async def produtos_da_loja(self, *, token):
        return [p for p in self.produtos.values() if p["ativo"] and p["estoque"] > 0]

    # pedidos
    def _registrar(self, dono, itens, entrega, forma, origem):
        if not itens:
            recusar("O pedido precisa de ao menos um item")
        for it in itens:
            p = self.produtos[it["produto_id"]]
            if not p["ativo"]:
                recusar("Produto indisponível")
            if p["estoque"] < it["quantidade"]:
                recusar("Estoque insuficiente")
        endereco = ""
        if entrega == "endereco":
            endereco = self.fichas[dono]["endereco"]
            if not endereco:
                recusar("Cadastre um endereço")
        total = 0
        for it in itens:
            p = self.produtos[it["produto_id"]]
            if self.quebrar != "estoque":
                p["estoque"] -= it["quantidade"]
            total += p["preco"] * it["quantidade"]
        i = self._id()
        sit = "pago" if forma == "online" else "pendente"
        self.pedidos[i] = {"id": i, "dono": dono, "situacao": sit, "total": total,
                           "entrega": entrega, "endereco_entrega": endereco, "itens": itens,
                           "pago_em": 1 if sit == "pago" else None, "origem": origem}
        return self.pedidos[i]

    async def fazer_pedido(self, itens, entrega, forma, *, token):
        p = self._registrar(token, itens, entrega, forma, "site")
        return {"id": p["id"], "total": p["total"], "situacao": p["situacao"]}

    async def meus_pedidos(self, *, token):
        return {"pedidos": [p for p in self.pedidos.values() if p["dono"] == token], "itens": []}

    async def mudar_situacao_do_pedido(self, i, nova, *, token):
        self._so_equipe(token)
        p = self.pedidos[i]
        if nova not in proximas(p["situacao"], p["entrega"]):
            recusar("Caminho de situação inválido")
        if nova == "cancelado":
            for it in p["itens"]:
                self.produtos[it["produto_id"]]["estoque"] += it["quantidade"]
        if nova in ("pago", "entregue") and not p["pago_em"]:
            p["pago_em"] = 1
        p["situacao"] = nova
        return p

    async def minha_ficha(self, t):
        return self.fichas.get(t)

    async def vender_no_balcao(self, tutor, itens, *, token):
        self._so_equipe(token)
        dono = next(t for t, f in self.fichas.items() if f["id"] == tutor)
        p = self._registrar(dono, itens, "retirada", "na_loja", "balcao")
        p.update(situacao="entregue", pago_em=1)
        return p

    # agenda
    async def listar_animais(self, *, token):
        return [{"id": i} for i, dono in self.pets.items() if dono == token]

    async def listar_servicos_agendaveis(self, *, token):
        return [{"id": 9, "categoria": "banho_tosa", "duracao_minutos": 60}]

    async def ocupacao_do_dia(self, s, dia, *, token):
        oc = [{"id_colaborador": 5, "inicio": a["inicio"], "fim": a["fim"]}
              for a in self.ag.values() if a["situacao"] != "cancelado"]
        if self.quebrar == "privacidade":
            return {"profissionais": [{"id": 5, "nome": "Ana"}], "ocupados": oc}
        return {"profissionais": [{"id": 5}], "ocupados": oc}

    async def criar_agendamento(self, d, *, token):
        if self.pets.get(d["pet_id"]) != token:
            recusar("Animal não encontrado")
        inicio, fim = d["inicio"], d["inicio"] + 3_600_000
        local = agenda._local(inicio)
        dia = local.date()
        if inicio <= agenda.agora_ms():
            recusar("Horário no passado")
        if not agenda.abre(dia):
            recusar("A clínica não abre neste dia")
        if inicio % (agenda.PASSO_MINUTOS * 60_000):
            recusar("Fora da grade")
        abertura, fechamento = agenda.EXPEDIENTE[dia.weekday()]
        meia_noite = agenda.inicio_do_dia_ms(dia)
        if inicio < meia_noite + abertura * 60_000 or fim > meia_noite + fechamento * 60_000:
            recusar("Fora do expediente")
        for a in self.ag.values():
            if a["situacao"] != "cancelado" and a["inicio"] < fim and a["fim"] > inicio:
                recusar("Horário ocupado")
        i = self._id()
        self.ag[i] = {"id": i, "dono": token, "inicio": inicio, "fim": fim,
                      "situacao": "marcado"}
        return self.ag[i]

    async def listar_agendamentos(self, *, token):
        return [a for a in self.ag.values() if a["dono"] == token]

    async def cancelar_agendamento(self, i, *, token):
        a = self.ag.get(i)
        if a is None or a["dono"] != token:
            raise xano.NaoEncontrado("Agendamento não encontrado", status=404)
        if a["situacao"] != "marcado":
            recusar("Já cancelado")
        a["situacao"] = "cancelado"
        return a


FUNCOES = [n for n in vars(XanoSimulado) if not n.startswith("_")]


def conta(rotulo, email):
    return f"{rotulo} — X\n  email: {email}\n  senha: {SEGREDO}\n"


DUAS = conta("EQUIPE", "eq@x.com") + conta("TUTOR", "cl@x.com") + conta("TUTOR", "cl2@x.com")
UMA = conta("EQUIPE", "eq@x.com") + conta("TUTOR", "cl@x.com")


def rodar(simulado, contas=DUAS):
    with tempfile.TemporaryDirectory() as pasta:
        arquivo = Path(pasta) / "contas.txt"
        arquivo.write_text(contas, encoding="utf-8")
        saida = io.StringIO()
        with mock.patch.multiple(xano, **{n: getattr(simulado, n) for n in FUNCOES}), \
                mock.patch.object(contas_de_teste, "ARQUIVO", arquivo), \
                mock.patch.object(v, "PAUSA", 0), \
                contextlib.redirect_stdout(saida):
            v.resultados.clear()
            codigo = asyncio.run(v.principal())
    return codigo, saida.getvalue(), list(v.resultados)


def falhas(resultados):
    return [c for s, c, _ in resultados if s == "FALHOU"]


class PontaAPonta(unittest.TestCase):
    def test_backend_certo_tudo_passa(self):
        codigo, saida, res = rodar(XanoSimulado())
        self.assertEqual(falhas(res), [])
        self.assertEqual(codigo, 0)
        self.assertGreaterEqual(sum(1 for s, *_ in res if s == "passou"), 45)
        self.assertNotIn(SEGREDO, saida)

    def test_pulados_tem_motivo(self):
        _, _, res = rodar(XanoSimulado())
        pulados = {c: d for s, c, d in res if s == "pulado"}
        self.assertIn("Cancelar com menos de 24 h é recusado", pulados)
        self.assertTrue(all(pulados.values()))

    def test_estoque_quebrado_acusa_e_sai_1(self):
        codigo, _, res = rodar(XanoSimulado(quebrar="estoque"))
        self.assertIn("O estoque baixou de 3 para 2", falhas(res))
        self.assertEqual(codigo, 1)

    def test_gerencia_quebrada_acusa(self):
        codigo, _, res = rodar(XanoSimulado(quebrar="gerencia"))
        self.assertIn("Equipe comum (staff) não cadastra colaborador", falhas(res))
        self.assertEqual(codigo, 1)

    def test_ocupacao_com_nome_acusa(self):
        _, _, res = rodar(XanoSimulado(quebrar="privacidade"))
        self.assertIn("A ocupação não traz nome nem contato de profissional", falhas(res))

    def test_uma_conta_de_cliente_pula_as_de_duas(self):
        codigo, _, res = rodar(XanoSimulado(), UMA)
        self.assertEqual(codigo, 0)
        pulados = [c for s, c, _ in res if s == "pulado"]
        for cenario in ("Outro cliente não vê o pedido", "Outro cliente não vê o agendamento",
                        "Outro cliente não cancela o agendamento"):
            self.assertIn(cenario, pulados)

    def test_conta_de_gerencia_pula_o_teste_de_staff(self):
        codigo, _, res = rodar(XanoSimulado(papel_equipe="admin"))
        self.assertEqual(codigo, 0)
        self.assertIn("Equipe comum (staff) não cadastra colaborador",
                      [c for s, c, _ in res if s == "pulado"])

    def test_sem_endereco_confere_a_recusa(self):
        codigo, _, res = rodar(XanoSimulado(endereco=""))
        self.assertEqual(codigo, 0)
        self.assertIn("Entrega no endereço sem endereço cadastrado é recusada",
                      [c for s, c, _ in res if s == "passou"])


if __name__ == "__main__":
    unittest.main()
