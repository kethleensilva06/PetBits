"""Verificação de ponta a ponta no Xano de verdade (change
`ferramentas-de-verificacao`, D3).

Uso, na raiz do projeto:

    python scripts/verificar_ponta_a_ponta.py

Entra com a primeira conta de EQUIPE e a primeira de CLIENTE com senha do
`contas-de-teste.local.txt` e confere os cenários principais das specs pelas
mesmas funções do cliente HTTP que as telas usam. Cada cenário sai como
`passou`, `FALHOU` ou `pulado` (com o motivo); o código de saída é 1 se algum
falhar. Nenhuma senha ou token aparece na saída.

Deixa dados de teste reconhecíveis no Xano: um "Produto de verificação …"
(desativado no fim), dois pedidos (um entregue, um cancelado), uma venda no
balcão e um agendamento cancelado.
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJETO))
load_dotenv(PROJETO / ".env", override=True)

from petbits import agenda, contas_de_teste, xano  # noqa: E402

PAUSA = 2.2  # limite de 10 requisições a cada 20 s da instância

resultados: list[tuple[str, str, str]] = []


def registrar(cenario: str, ok: bool | None, detalhe: str = "") -> None:
    situacao = "pulado" if ok is None else ("passou" if ok else "FALHOU")
    resultados.append((situacao, cenario, detalhe))
    print(f"  {situacao:7} {cenario}" + (f" — {detalhe}" if detalhe else ""))


async def chamar(coro):
    """Uma requisição, com a pausa do orçamento antes."""
    await asyncio.sleep(PAUSA)
    return await coro


async def recusa(coro) -> str | None:
    """A mensagem da recusa, ou None se a chamada passou."""
    try:
        await chamar(coro)
    except xano.XanoError as erro:
        return str(erro) or erro.__class__.__name__
    return None


async def entrar(conta: dict) -> tuple[str, str]:
    sessao = await chamar(xano.entrar(conta["email"], conta["senha"]))
    perfil = await chamar(xano.usuario_atual(sessao["authToken"]))
    return sessao["authToken"], (perfil or {}).get("role") or ""


async def separacao(equipe: str, cliente: str) -> None:
    print("\nSeparação entre equipe e cliente")
    registrar("Cliente pede a agenda da clínica e é recusado",
              await recusa(xano.agenda_da_clinica(agenda.inicio_do_dia_ms(agenda.hoje()),
                                                  token=cliente)) is not None)
    registrar("Cliente tenta alterar o catálogo e é recusado",
              await recusa(xano.criar_produto({"nome": "x", "categoria": "racao",
                                               "preco": 1, "estoque": 1}, token=cliente))
              is not None)
    registrar("Equipe abre o painel",
              await recusa(xano.painel_equipe(token=equipe)) is None)


async def loja(equipe: str, cliente: str) -> None:
    print("\nLoja, pedidos e balcão")
    nome = f"Produto de verificação {time.strftime('%Y%m%d%H%M%S')}"
    produto = await chamar(xano.criar_produto(
        {"nome": nome, "categoria": "acessorio", "preco": 10.0, "estoque": 2}, token=equipe))
    pid = produto["id"]
    registrar("Equipe cadastra produto", bool(pid))

    msg = await recusa(xano.criar_produto({"nome": "x", "categoria": "racao", "preco": 0,
                                           "estoque": 1}, token=equipe))
    registrar("Preço zero é recusado", msg is not None, msg or "")

    vitrine = await chamar(xano.produtos_da_loja(token=cliente))
    registrar("Produto ativo com estoque aparece na loja",
              any(p.get("id") == pid for p in vitrine))

    msg = await recusa(xano.fazer_pedido([{"produto_id": pid, "quantidade": 3}],
                                         "retirada", "na_loja", token=cliente))
    registrar("Estoque insuficiente recusa o pedido", msg is not None, msg or "")

    pedido = await chamar(xano.fazer_pedido([{"produto_id": pid, "quantidade": 1}],
                                            "retirada", "na_loja", token=cliente))
    registrar("Pedido com retirada e pagamento na loja nasce pendente",
              pedido.get("situacao") == "pendente" and float(pedido.get("total") or 0) == 10.0,
              f"situação {pedido.get('situacao')}, total {pedido.get('total')}")

    meus = await chamar(xano.meus_pedidos(token=cliente))
    registrar("O pedido aparece em Meus pedidos",
              any(p.get("id") == pedido["id"] for p in meus.get("pedidos") or []))

    estoque = next((p.get("estoque") for p in await chamar(xano.listar_produtos(token=equipe))
                    if p.get("id") == pid), None)
    registrar("O estoque baixou de 2 para 1", estoque == 1, f"estoque {estoque}")

    msg = await recusa(xano.mudar_situacao_do_pedido(pedido["id"], "enviado", token=equipe))
    registrar("Marcar como enviado um pedido de retirada é recusado", msg is not None)

    await chamar(xano.mudar_situacao_do_pedido(pedido["id"], "pronto_retirada", token=equipe))
    feito = await chamar(xano.mudar_situacao_do_pedido(pedido["id"], "entregue", token=equipe))
    registrar("Entregar registra o pagamento na retirada",
              feito.get("situacao") == "entregue" and bool(feito.get("pago_em")))

    outro = await chamar(xano.fazer_pedido([{"produto_id": pid, "quantidade": 1}],
                                           "retirada", "online", token=cliente))
    registrar("Pagamento online simulado nasce pago", outro.get("situacao") == "pago")
    await chamar(xano.mudar_situacao_do_pedido(outro["id"], "cancelado", token=equipe))
    estoque = next((p.get("estoque") for p in await chamar(xano.listar_produtos(token=equipe))
                    if p.get("id") == pid), None)
    registrar("Cancelar devolve o estoque", estoque == 1, f"estoque {estoque}")

    ficha = await chamar(xano.minha_ficha(cliente))
    if ficha and ficha.get("id"):
        venda = await chamar(xano.vender_no_balcao(ficha["id"], [{"produto_id": pid,
                                                                  "quantidade": 1}],
                                                   token=equipe))
        registrar("Venda no balcão nasce entregue", venda.get("situacao") == "entregue")
        meus = await chamar(xano.meus_pedidos(token=cliente))
        origem = next((p.get("origem") for p in meus.get("pedidos") or []
                       if p.get("id") == venda.get("id")), None)
        registrar("A venda aparece na conta do cliente com origem balcão", origem == "balcao")
    else:
        registrar("Venda no balcão", None, "a conta de cliente não tem ficha")

    await chamar(xano.atualizar_produto(pid, {"ativo": False}, token=equipe))
    vitrine = await chamar(xano.produtos_da_loja(token=cliente))
    registrar("Produto desativado some da loja", all(p.get("id") != pid for p in vitrine))


async def agendamentos(cliente: str) -> None:
    print("\nAgenda")
    animais = await chamar(xano.listar_animais(token=cliente))
    if not animais:
        registrar("Agenda", None, "a conta de cliente não tem animal cadastrado")
        return
    servicos = [s for s in await chamar(xano.listar_servicos_agendaveis(token=cliente))
                if s.get("categoria") == "banho_tosa"]
    if not servicos:
        registrar("Agenda", None, "não há serviço de banho e tosa com categoria")
        return
    servico = servicos[0]

    dia = agenda.hoje() + timedelta(days=2)
    while not agenda.abre(dia) or dia.weekday() == 5:
        dia += timedelta(days=1)  # dia útil, a pelo menos dois dias (prazo de 24 h)
    ocupacao = await chamar(xano.ocupacao_do_dia(servico["id"], agenda.inicio_do_dia_ms(dia),
                                                 token=cliente))
    profissionais = [int(p["id"]) for p in ocupacao.get("profissionais") or []]
    livres = agenda.horarios_livres(dia, int(servico.get("duracao_minutos") or 0),
                                    profissionais, ocupacao.get("ocupados") or [],
                                    agenda.agora_ms())
    if not livres:
        registrar("Agenda", None, f"nenhum horário livre em {dia.isoformat()}")
        return

    msg = await recusa(xano.criar_agendamento({"pet_id": animais[0]["id"],
                                               "servico_id": servico["id"],
                                               "inicio": livres[0] + 15 * 60_000},
                                              token=cliente))
    registrar("Horário fora da grade de 30 minutos é recusado", msg is not None, msg or "")

    marcado = await chamar(xano.criar_agendamento({"pet_id": animais[0]["id"],
                                                   "servico_id": servico["id"],
                                                   "inicio": livres[0]}, token=cliente))
    registrar("Agendamento num horário livre é aceito", marcado.get("situacao") == "marcado",
              f"{dia.isoformat()} {agenda.hora(livres[0])}")

    if len(profissionais) == 1:
        msg = await recusa(xano.criar_agendamento({"pet_id": animais[0]["id"],
                                                   "servico_id": servico["id"],
                                                   "inicio": livres[0]}, token=cliente))
        registrar("O mesmo horário com o único profissional ocupado é recusado",
                  msg is not None, msg or "")
    else:
        registrar("Sobreposição", None, "há mais de um profissional para o serviço")

    lista = await chamar(xano.listar_agendamentos(token=cliente))
    registrar("O agendamento aparece em Meus agendamentos",
              any(a.get("id") == marcado.get("id") for a in lista))

    cancelado = await chamar(xano.cancelar_agendamento(marcado["id"], token=cliente))
    registrar("Cancelar com mais de 24 h", cancelado.get("situacao") == "cancelado")
    msg = await recusa(xano.cancelar_agendamento(marcado["id"], token=cliente))
    registrar("Cancelar de novo é recusado", msg is not None)


async def principal() -> int:
    equipe_conta = next(iter(contas_de_teste.do_grupo(contas_de_teste.EQUIPE)), None)
    cliente_conta = next(iter(contas_de_teste.do_grupo(contas_de_teste.CLIENTES)), None)
    if equipe_conta is None or cliente_conta is None:
        falta = "de equipe" if equipe_conta is None else "de cliente"
        sys.exit(f"Falta uma conta {falta} com senha em contas-de-teste.local.txt.")

    print(f"Equipe:  {equipe_conta['email']}\nCliente: {cliente_conta['email']}")
    try:
        equipe, papel_equipe = await entrar(equipe_conta)
        cliente, papel_cliente = await entrar(cliente_conta)
    except xano.XanoError as erro:
        registrar("Entrar com as contas de teste", False, str(erro))
        print("\nSem as duas entradas, nada mais roda.")
        return 1
    registrar("A conta de equipe tem papel de equipe", xano.eh_equipe(papel_equipe),
              f"papel '{papel_equipe or 'vazio'}'")
    registrar("A conta de cliente tem papel de cliente", xano.eh_tutor(papel_cliente),
              f"papel '{papel_cliente or 'vazio'}'")
    if not xano.eh_equipe(papel_equipe):
        print("\nSem conta de equipe válida, o resto não tem como rodar.")
    else:
        for etapa in (separacao(equipe, cliente), loja(equipe, cliente), agendamentos(cliente)):
            try:
                await etapa
            except xano.XanoError as erro:
                registrar("Etapa interrompida por erro inesperado", False, str(erro))

    falhas = sum(1 for r in resultados if r[0] == "FALHOU")
    passou = sum(1 for r in resultados if r[0] == "passou")
    pulados = sum(1 for r in resultados if r[0] == "pulado")
    print(f"\n{passou} passaram, {falhas} falharam, {pulados} pulados.")
    return 1 if falhas else 0


def main() -> None:
    if not os.getenv("XANO_BASE_URL", "").strip():
        sys.exit("XANO_BASE_URL não está no .env.")
    raise SystemExit(asyncio.run(principal()))


if __name__ == "__main__":
    main()
