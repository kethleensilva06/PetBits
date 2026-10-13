"""Verificação de ponta a ponta no Xano de verdade (changes
`ferramentas-de-verificacao` e `ampliar-ponta-a-ponta`).

Uso, na raiz do projeto:

    python scripts/verificar_ponta_a_ponta.py

Entra com a primeira conta de EQUIPE e as duas primeiras de CLIENTE com senha
do `contas-de-teste.local.txt` e confere os cenários das specs — o caminho
feliz e as recusas — pelas mesmas funções do cliente HTTP que as telas usam.
Cada cenário sai como `passou`, `FALHOU` ou `pulado` (com o motivo); o código
de saída é 1 se algum falhar. Nenhuma senha ou token aparece na saída.

Deixa dados de teste reconhecíveis no Xano: um "Produto de verificação …"
(desativado no fim), pedidos (entregues ou cancelados), uma venda no balcão e
um agendamento cancelado.
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


async def estoque_de(pid: int, equipe: str):
    return next((p.get("estoque") for p in await chamar(xano.listar_produtos(token=equipe))
                 if p.get("id") == pid), None)


# --- separação e gerência ---------------------------------------------------------


async def separacao(equipe: str, cliente: str, papel_equipe: str) -> None:
    print("\nSeparação entre equipe e cliente")
    registrar("Cliente pede a agenda da clínica e é recusado",
              await recusa(xano.agenda_da_clinica(agenda.inicio_do_dia_ms(agenda.hoje()),
                                                  token=cliente)) is not None)
    registrar("Cliente tenta alterar o catálogo e é recusado",
              await recusa(xano.criar_produto({"nome": "x", "categoria": "racao",
                                               "preco": 1, "estoque": 1}, token=cliente))
              is not None)
    registrar("Cliente pede a lista de clientes da clínica e é recusado",
              await recusa(xano.listar_tutores_da_clinica(token=cliente)) is not None)
    registrar("Cliente pede os pedidos da clínica e é recusado",
              await recusa(xano.pedidos_da_clinica(token=cliente)) is not None)
    registrar("Cliente tenta registrar venda no balcão e é recusado",
              await recusa(xano.vender_no_balcao(1, [{"produto_id": 1, "quantidade": 1}],
                                                 token=cliente)) is not None)
    registrar("Equipe abre o painel",
              await recusa(xano.painel_equipe(token=equipe)) is None)

    if papel_equipe == "staff":
        registrar("Equipe comum (staff) não cadastra colaborador",
                  await recusa(xano.criar_colaborador({"nome": "Verificação",
                                                       "funcao": "atendente"},
                                                      token=equipe)) is not None)
    else:
        registrar("Equipe comum (staff) não cadastra colaborador", None,
                  "a conta de equipe é gerência; o teste criaria um colaborador de verdade")

    servicos = await chamar(xano.listar_servicos(token=equipe))
    if servicos:
        msg = await recusa(xano.atualizar_servico(servicos[0]["id"],
                                                  {"categoria": "hospedagem"}, token=equipe))
        registrar("Categoria de serviço fora do conjunto é recusada", msg is not None, msg or "")
    else:
        registrar("Categoria de serviço fora do conjunto é recusada", None, "nenhum serviço")


# --- loja, pedidos e balcão -------------------------------------------------------


async def loja(equipe: str, cliente: str, cliente2: str | None) -> None:
    print("\nLoja, pedidos e balcão")
    nome = f"Produto de verificação {time.strftime('%Y%m%d%H%M%S')}"
    produto = await chamar(xano.criar_produto(
        {"nome": nome, "categoria": "acessorio", "preco": 10.0, "estoque": 3}, token=equipe))
    pid = produto["id"]
    registrar("Equipe cadastra produto", bool(pid))

    msg = await recusa(xano.criar_produto({"nome": "x", "categoria": "racao", "preco": 0,
                                           "estoque": 1}, token=equipe))
    registrar("Preço zero é recusado", msg is not None, msg or "")
    msg = await recusa(xano.criar_produto({"nome": "x", "categoria": "racao", "preco": 1,
                                           "estoque": -1}, token=equipe))
    registrar("Estoque negativo é recusado no cadastro", msg is not None, msg or "")
    msg = await recusa(xano.criar_produto({"nome": "x", "categoria": "hospedagem", "preco": 1,
                                           "estoque": 1}, token=equipe))
    registrar("Categoria de produto fora do conjunto é recusada", msg is not None, msg or "")
    msg = await recusa(xano.atualizar_produto(pid, {"estoque": -1}, token=equipe))
    registrar("Estoque negativo é recusado na alteração", msg is not None, msg or "")

    await chamar(xano.atualizar_produto(pid, {"preco": 12.5}, token=equipe))
    depois = next((p for p in await chamar(xano.listar_produtos(token=equipe))
                   if p.get("id") == pid), {})
    registrar("Alterar só o preço mantém o resto",
              float(depois.get("preco") or 0) == 12.5 and depois.get("estoque") == 3
              and depois.get("nome") == nome)
    await chamar(xano.atualizar_produto(pid, {"preco": 10.0}, token=equipe))

    vitrine = await chamar(xano.produtos_da_loja(token=cliente))
    registrar("Produto ativo com estoque aparece na loja",
              any(p.get("id") == pid for p in vitrine))

    msg = await recusa(xano.fazer_pedido([], "retirada", "na_loja", token=cliente))
    registrar("Pedido sem itens é recusado", msg is not None, msg or "")
    msg = await recusa(xano.fazer_pedido([{"produto_id": pid, "quantidade": 4}],
                                         "retirada", "na_loja", token=cliente))
    registrar("Estoque insuficiente recusa o pedido", msg is not None, msg or "")
    registrar("A recusa não mudou o estoque", await estoque_de(pid, equipe) == 3)

    pedido = await chamar(xano.fazer_pedido([{"produto_id": pid, "quantidade": 1}],
                                            "retirada", "na_loja", token=cliente))
    registrar("Pedido com retirada e pagamento na loja nasce pendente",
              pedido.get("situacao") == "pendente" and float(pedido.get("total") or 0) == 10.0,
              f"situação {pedido.get('situacao')}, total {pedido.get('total')}")

    meus = await chamar(xano.meus_pedidos(token=cliente))
    meu = next((p for p in meus.get("pedidos") or [] if p.get("id") == pedido["id"]), None)
    registrar("O pedido aparece em Meus pedidos", meu is not None)
    registrar("Pedido pelo site tem origem site", (meu or {}).get("origem") == "site")
    registrar("O estoque baixou de 3 para 2", await estoque_de(pid, equipe) == 2)

    if cliente2:
        dele = await chamar(xano.meus_pedidos(token=cliente2))
        registrar("Outro cliente não vê o pedido",
                  all(p.get("id") != pedido["id"] for p in dele.get("pedidos") or []))
    else:
        registrar("Outro cliente não vê o pedido", None, "só há uma conta de cliente com senha")

    msg = await recusa(xano.mudar_situacao_do_pedido(pedido["id"], "enviado", token=equipe))
    registrar("Marcar como enviado um pedido de retirada é recusado", msg is not None)
    await chamar(xano.mudar_situacao_do_pedido(pedido["id"], "pronto_retirada", token=equipe))
    feito = await chamar(xano.mudar_situacao_do_pedido(pedido["id"], "entregue", token=equipe))
    registrar("Entregar registra o pagamento na retirada",
              feito.get("situacao") == "entregue" and bool(feito.get("pago_em")))
    msg = await recusa(xano.mudar_situacao_do_pedido(pedido["id"], "pendente", token=equipe))
    registrar("Pedido entregue não volta a pendente", msg is not None)

    outro = await chamar(xano.fazer_pedido([{"produto_id": pid, "quantidade": 1}],
                                           "retirada", "online", token=cliente))
    registrar("Pagamento online simulado nasce pago", outro.get("situacao") == "pago")
    await chamar(xano.mudar_situacao_do_pedido(outro["id"], "cancelado", token=equipe))
    registrar("Cancelar devolve o estoque", await estoque_de(pid, equipe) == 2)

    ficha = await chamar(xano.minha_ficha(cliente)) or {}
    if ficha.get("endereco"):
        endereco = await chamar(xano.fazer_pedido([{"produto_id": pid, "quantidade": 1}],
                                                  "endereco", "na_loja", token=cliente))
        meus = await chamar(xano.meus_pedidos(token=cliente))
        guardado = next((p.get("endereco_entrega") for p in meus.get("pedidos") or []
                         if p.get("id") == endereco.get("id")), "")
        registrar("Entrega no endereço guarda o endereço do cadastro",
                  bool(guardado) and guardado == ficha.get("endereco"))
        await chamar(xano.mudar_situacao_do_pedido(endereco["id"], "cancelado", token=equipe))
    else:
        msg = await recusa(xano.fazer_pedido([{"produto_id": pid, "quantidade": 1}],
                                             "endereco", "na_loja", token=cliente))
        registrar("Entrega no endereço sem endereço cadastrado é recusada", msg is not None,
                  msg or "")

    if ficha.get("id"):
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
    msg = await recusa(xano.fazer_pedido([{"produto_id": pid, "quantidade": 1}],
                                         "retirada", "na_loja", token=cliente))
    registrar("Pedido com produto inativo é recusado", msg is not None, msg or "")


# --- agenda ------------------------------------------------------------------------


def as_ms(dia, h, m=0) -> int:
    return agenda.inicio_do_dia_ms(dia) + (h * 60 + m) * 60_000


async def agendamentos(cliente: str, cliente2: str | None) -> None:
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
    duracao = int(servico.get("duracao_minutos") or 0)
    pet = animais[0]["id"]

    def pedido(inicio, animal=pet):
        return {"pet_id": animal, "servico_id": servico["id"], "inicio": inicio}

    dia = agenda.hoje() + timedelta(days=2)
    while not agenda.abre(dia) or dia.weekday() == 5:
        dia += timedelta(days=1)  # dia útil, a pelo menos dois dias (prazo de 24 h)
    ocupacao = await chamar(xano.ocupacao_do_dia(servico["id"], agenda.inicio_do_dia_ms(dia),
                                                 token=cliente))
    chaves = {k for p in ocupacao.get("profissionais") or [] for k in p} | \
             {k for o in ocupacao.get("ocupados") or [] for k in o}
    registrar("A ocupação não traz nome nem contato de profissional",
              chaves <= {"id", "id_colaborador", "inicio", "fim"}, f"chaves: {sorted(chaves)}")

    profissionais = [int(p["id"]) for p in ocupacao.get("profissionais") or []]
    livres = agenda.horarios_livres(dia, duracao, profissionais, ocupacao.get("ocupados") or [],
                                    agenda.agora_ms())
    if not livres:
        registrar("Agenda", None, f"nenhum horário livre em {dia.isoformat()}")
        return

    domingo = dia + timedelta(days=(6 - dia.weekday()) % 7 or 7)
    sabado = domingo - timedelta(days=1)
    ontem = agenda.hoje() - timedelta(days=1)
    for nome, inicio in (
        ("Domingo é recusado", as_ms(domingo, 9)),
        ("Antes das 8h é recusado", as_ms(dia, 7, 30)),
        # 11:30 está na grade; com mais de 30 min o fim passa do meio-dia de sábado
        ("Atendimento que passa do fechamento do sábado é recusado",
         as_ms(sabado, 11, 30) if duracao > 30 else None),
        ("Horário no passado é recusado", as_ms(ontem, 9)),
        ("Horário fora da grade de 30 minutos é recusado", livres[0] + 15 * 60_000),
    ):
        if inicio is None:
            registrar(nome, None, "o serviço dura até 30 min e cabe antes do fechamento")
            continue
        msg = await recusa(xano.criar_agendamento(pedido(inicio), token=cliente))
        registrar(nome, msg is not None, msg or "")

    marcado = await chamar(xano.criar_agendamento(pedido(livres[0]), token=cliente))
    registrar("Agendamento num horário livre é aceito", marcado.get("situacao") == "marcado",
              f"{dia.isoformat()} {agenda.hora(livres[0])}")

    if len(profissionais) == 1:
        msg = await recusa(xano.criar_agendamento(pedido(livres[0]), token=cliente))
        registrar("O mesmo horário com o único profissional ocupado é recusado",
                  msg is not None, msg or "")
    else:
        registrar("Sobreposição", None, "há mais de um profissional para o serviço")

    lista = await chamar(xano.listar_agendamentos(token=cliente))
    registrar("O agendamento aparece em Meus agendamentos",
              any(a.get("id") == marcado.get("id") for a in lista))

    if cliente2:
        dele = await chamar(xano.listar_agendamentos(token=cliente2))
        registrar("Outro cliente não vê o agendamento",
                  all(a.get("id") != marcado.get("id") for a in dele))
        msg = await recusa(xano.cancelar_agendamento(marcado["id"], token=cliente2))
        registrar("Outro cliente não cancela o agendamento", msg is not None, msg or "")
        livre = next(iter(livres[1:]), None)
        if livre:
            msg = await recusa(xano.criar_agendamento(pedido(livre), token=cliente2))
            registrar("Outro cliente não marca com o animal de quem não é dele",
                      msg is not None, msg or "")
    else:
        for nome in ("Outro cliente não vê o agendamento", "Outro cliente não cancela o agendamento",
                     "Outro cliente não marca com o animal de quem não é dele"):
            registrar(nome, None, "só há uma conta de cliente com senha")

    cancelado = await chamar(xano.cancelar_agendamento(marcado["id"], token=cliente))
    registrar("Cancelar com mais de 24 h", cancelado.get("situacao") == "cancelado")
    msg = await recusa(xano.cancelar_agendamento(marcado["id"], token=cliente))
    registrar("Cancelar de novo é recusado", msg is not None)
    registrar("Cancelar com menos de 24 h é recusado", None,
              "deixaria um agendamento que ninguém consegue cancelar; coberto pelo teste local "
              "e pela leitura do endpoint")


# --- principal ---------------------------------------------------------------------


async def principal() -> int:
    equipe_conta = next(iter(contas_de_teste.do_grupo(contas_de_teste.EQUIPE)), None)
    clientes = contas_de_teste.do_grupo(contas_de_teste.CLIENTES)
    if equipe_conta is None or not clientes:
        falta = "de equipe" if equipe_conta is None else "de cliente"
        sys.exit(f"Falta uma conta {falta} com senha em contas-de-teste.local.txt.")

    print(f"Equipe:  {equipe_conta['email']}\nCliente: {clientes[0]['email']}")
    if len(clientes) > 1:
        print(f"Cliente 2: {clientes[1]['email']}")
    try:
        equipe, papel_equipe = await entrar(equipe_conta)
        cliente, papel_cliente = await entrar(clientes[0])
        cliente2 = (await entrar(clientes[1]))[0] if len(clientes) > 1 else None
    except xano.XanoError as erro:
        registrar("Entrar com as contas de teste", False, str(erro))
        print("\nSem as entradas, nada mais roda.")
        return 1
    registrar("A conta de equipe tem papel de equipe", xano.eh_equipe(papel_equipe),
              f"papel '{papel_equipe or 'vazio'}'")
    registrar("A conta de cliente tem papel de cliente", xano.eh_tutor(papel_cliente),
              f"papel '{papel_cliente or 'vazio'}'")
    if not xano.eh_equipe(papel_equipe):
        print("\nSem conta de equipe válida, o resto não tem como rodar.")
    else:
        for etapa in (separacao(equipe, cliente, papel_equipe), loja(equipe, cliente, cliente2),
                      agendamentos(cliente, cliente2)):
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
