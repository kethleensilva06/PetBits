"""Teste de duas contas: a prova de que a superfície da clínica recusa.

Por que ele existe, e por que não basta a guarda de repositório
(`verificar_equipe.py`): a guarda lê os arquivos `.xs` do repositório, e
**não alcança endpoint criado pela interface do Xano**. Quem criar um
endpoint pelo painel está fora de todas as redes de texto. O que pega esse
caso é exercitar o endpoint que está no ar, com duas credenciais.

A célula de cada endpoint de equipe é uma só, e as duas metades importam:

    token de tutor → 403      (recusa)
    token de admin → 200      (e não um 403 por defeito na prova)

Só a primeira metade não prova nada: um endpoint quebrado recusa todo mundo
e passaria. É o espelho do teste de duas contas que a change anterior já
exige do lado do tutor.

Uso:

    python scripts/teste_duas_contas.py

As credenciais saem de `contas-de-teste.local.txt`, que é ignorado pelo git.
O limite do plano é de 10 requisições a cada 20 segundos **por instância**,
então o roteiro faz pausas — e é por isso que ele demora.
"""

from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

PROJETO = Path(__file__).resolve().parent.parent
load_dotenv(PROJETO / ".env", override=True)

BASE = os.getenv("XANO_BASE_URL", "").strip().rstrip("/")
AUTH = os.getenv("XANO_AUTH_BASE_URL", "").strip().rstrip("/")
CREDENCIAIS = PROJETO / "contas-de-teste.local.txt"

# Folga sobre o limite de 10/20s. Duas requisições por segundo estouraria.
PAUSA = 2.2

# Cada endpoint de equipe, com o corpo mínimo que o faz chegar até a prova.
# A prova é a SEGUNDA instrução de todos eles, então um corpo inválido ainda
# assim bate na recusa — que é exatamente o que se quer medir.
SUPERFICIE_DA_EQUIPE = [
    ("GET", "/equipe/painel", None),
    ("GET", "/equipe/colaboradores", None),
    ("GET", "/equipe/colaboradores/1", None),
    ("POST", "/equipe/colaboradores", {"nome": "Sonda", "funcao": "atendente"}),
    ("PATCH", "/equipe/colaboradores/1", {"nome": "Sonda"}),
    ("GET", "/equipe/servicos", None),
    ("GET", "/equipe/servicos/1", None),
    ("POST", "/equipe/servicos", {"nome": "Sonda", "preco": 1, "duracao_minutos": 10}),
    ("PATCH", "/equipe/servicos/1", {"nome": "Sonda"}),
    ("GET", "/equipe/tutores", None),
    ("GET", "/equipe/animais", None),
]


def ler_credenciais() -> dict:
    if not CREDENCIAIS.exists():
        sys.exit(
            f"{CREDENCIAIS.name} não existe. Ele guarda as contas de teste e é "
            "ignorado pelo git — recrie-o semeando a base."
        )
    texto = CREDENCIAIS.read_text(encoding="utf-8")
    contas = {}
    atual = None
    for linha in texto.splitlines():
        if re.match(r"^[A-Z]", linha.strip()):
            atual = "tutor" if "TUTOR" in linha else "equipe" if "EQUIPE" in linha else None
            if atual:
                contas[atual] = {}
        elif atual and ":" in linha:
            chave, _, valor = linha.partition(":")
            chave = chave.strip().replace("-", "")
            if chave in ("email", "senha"):
                contas[atual][chave] = valor.strip()
    faltando = [p for p in ("tutor", "equipe") if not contas.get(p, {}).get("senha")]
    if faltando:
        sys.exit(f"credenciais incompletas em {CREDENCIAIS.name}: {faltando}")
    return contas


def entrar(email: str, senha: str) -> str:
    """Token de sessão. Usa o endpoint próprio, não o do template."""
    r = httpx.post(f"{BASE}/entrar", json={"email": email, "password": senha}, timeout=30)
    if r.status_code != 200:
        sys.exit(f"não entrou como {email}: HTTP {r.status_code} {r.text[:200]}")
    return r.json()["authToken"]


def chamar(metodo: str, caminho: str, token: str, corpo) -> httpx.Response:
    return httpx.request(
        metodo,
        f"{BASE}{caminho}",
        headers={"Authorization": f"Bearer {token}"},
        json=corpo,
        timeout=30,
    )


def main() -> int:
    if not BASE:
        sys.exit("XANO_BASE_URL não configurada no .env")

    contas = ler_credenciais()
    print("Entrando com as duas contas...")
    tok_tutor = entrar(contas["tutor"]["email"], contas["tutor"]["senha"])
    time.sleep(PAUSA)
    tok_equipe = entrar(contas["equipe"]["email"], contas["equipe"]["senha"])
    time.sleep(PAUSA)

    print(f"\n{'endpoint':<42} {'tutor':>10} {'equipe':>10}   veredito")
    print("-" * 78)

    acusacoes = []
    for metodo, caminho, corpo in SUPERFICIE_DA_EQUIPE:
        rotulo = f"{metodo} {caminho}"

        r_tutor = chamar(metodo, caminho, tok_tutor, corpo)
        time.sleep(PAUSA)
        r_equipe = chamar(metodo, caminho, tok_equipe, corpo)
        time.sleep(PAUSA)

        # O tutor TEM de ser recusado. 403 é o esperado; qualquer 2xx é o
        # defeito que este roteiro existe para achar.
        tutor_ok = r_tutor.status_code == 403
        # A equipe tem de PASSAR pela prova. 404 e 400 contam como passou: o
        # registro pedido pode não existir, ou o corpo da sonda ser inválido —
        # o que não pode acontecer é 403, que significaria prova quebrada.
        equipe_ok = r_equipe.status_code != 403

        if tutor_ok and equipe_ok:
            veredito = "ok"
        elif not tutor_ok:
            veredito = "VAZA — tutor não foi recusado"
            acusacoes.append((rotulo, veredito, r_tutor.status_code))
        else:
            veredito = "TRANCA — equipe recusada pela própria prova"
            acusacoes.append((rotulo, veredito, r_equipe.status_code))

        print(f"{rotulo:<42} {r_tutor.status_code:>10} {r_equipe.status_code:>10}   {veredito}")

    # O caminho do tutor continua intacto: o ponto do desenho é que ele não
    # mudou. Se esta linha quebrar, a separação de endpoints custou algo.
    print("\nO caminho do tutor não foi afetado:")
    r = chamar("GET", "/pet", tok_tutor, None)
    print(f"  GET /pet com token de tutor: HTTP {r.status_code} "
          f"({len(r.json()) if r.status_code == 200 else '?'} animais)")
    if r.status_code != 200:
        acusacoes.append(("GET /pet", "o tutor perdeu o acesso aos próprios animais",
                          r.status_code))

    print()
    if acusacoes:
        print(f"{len(acusacoes)} ACUSAÇÃO(ÕES):")
        for rotulo, veredito, status in acusacoes:
            print(f"  {rotulo} — {veredito} (HTTP {status})")
        return 1

    print(f"{len(SUPERFICIE_DA_EQUIPE)} endpoints de equipe: tutor recusado em todos, "
          "equipe passa em todos.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
