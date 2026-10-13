"""Cria clientes de teste pelo cadastro público e os põe no Alt+2.

Uso, na raiz do projeto:

    python scripts/criar_clientes_de_teste.py 5

Cada cliente é criado pelo MESMO caminho da tela de cadastro
(`xano.cadastrar_tutor`, change `clientes-de-teste-por-script`, D1) e
acrescentado a `contas-de-teste.local.txt` como bloco `TUTOR` — que o `Alt+2`
da tela de entrada lista. O arquivo é ignorado pelo git.

**As contas são criadas na base de verdade.** Os dados são fictícios e fáceis
de achar depois: e-mail `cliente.teste.<carimbo>.<n>@exemplo.com` (D2).

A senha de cada cliente vai só para o arquivo local; a saída deste script
mostra nome e e-mail, nunca senha.
"""

from __future__ import annotations

import asyncio
import os
import random
import secrets
import string
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJETO))
load_dotenv(PROJETO / ".env", override=True)

from petbits import contas_de_teste, xano  # noqa: E402

# Folga sobre o limite de 10 requisições a cada 20 s da instância (D4), a
# mesma de `teste_duas_contas.py`.
PAUSA = 2.2

NOMES = [
    "Mariana Souza", "Pedro Almeida", "Juliana Costa", "Rafael Pereira",
    "Camila Oliveira", "Lucas Martins", "Beatriz Rocha", "Gabriel Santos",
    "Larissa Gomes", "Thiago Barbosa", "Fernanda Lima", "Diego Carvalho",
]
RUAS = ["Rua das Flores", "Av. Paulista", "Rua do Sol", "Rua das Palmeiras", "Av. Brasil"]


def cpf_ficticio() -> str:
    """11 dígitos com os dígitos verificadores certos (D2)."""
    while True:
        base = [random.randint(0, 9) for _ in range(9)]
        if len(set(base)) > 1:  # 111.111.111-xx é inválido por convenção
            break
    for tamanho in (9, 10):
        soma = sum(d * p for d, p in zip(base, range(tamanho + 1, 1, -1)))
        resto = (soma * 10) % 11
        base.append(0 if resto == 10 else resto)
    return "".join(map(str, base))


def cpf_valido(cpf: str) -> bool:
    if len(cpf) != 11 or not cpf.isdigit() or len(set(cpf)) == 1:
        return False
    numeros = [int(c) for c in cpf]
    for tamanho in (9, 10):
        soma = sum(d * p for d, p in zip(numeros[:tamanho], range(tamanho + 1, 1, -1)))
        if numeros[tamanho] != (0 if (soma * 10) % 11 == 10 else (soma * 10) % 11):
            return False
    return True


def senha_gerada() -> str:
    """12 caracteres, sempre com letra e dígito — a regra do cadastro."""
    alfabeto = string.ascii_letters + string.digits
    while True:
        senha = "".join(secrets.choice(alfabeto) for _ in range(12))
        if any(c.isalpha() for c in senha) and any(c.isdigit() for c in senha):
            return senha


def telefone_ficticio() -> str:
    return "119" + "".join(str(random.randint(0, 9)) for _ in range(8))


def gravar(nome: str, email: str, senha: str) -> None:
    """Acrescenta UM cliente ao arquivo, logo depois de criado (D3)."""
    arquivo = contas_de_teste.ARQUIVO
    novo = not arquivo.exists()
    with arquivo.open("a", encoding="utf-8") as saida:
        if novo:
            saida.write(
                "Contas de teste do PetBits. NUNCA versionar (está no .gitignore).\n"
            )
        saida.write(f"\nTUTOR — {nome}\n  email: {email}\n  senha: {senha}\n")


async def criar(quantidade: int) -> int:
    carimbo = time.strftime("%Y%m%d%H%M%S")
    criados = 0
    for n in range(1, quantidade + 1):
        nome = f"{random.choice(NOMES)} (teste)"
        email = f"cliente.teste.{carimbo}.{n}@exemplo.com"
        senha = senha_gerada()
        try:
            await xano.cadastrar_tutor(
                nome=nome,
                email=email,
                senha=senha,
                documento=cpf_ficticio(),
                telefone=telefone_ficticio(),
                endereco=f"{random.choice(RUAS)}, {random.randint(1, 999)}",
            )
        except xano.XanoError as erro:
            # Recusa genérica do cadastro (e-mail ou CPF em uso) ou limite:
            # não grava, segue com os demais.
            print(f"  recusado  {email}: {erro}")
        else:
            gravar(nome, email, senha)
            criados += 1
            print(f"  criado    {nome:<32} {email}")
        if n < quantidade:
            await asyncio.sleep(PAUSA)
    return criados


def main() -> None:
    if len(sys.argv) != 2 or not sys.argv[1].isdigit() or int(sys.argv[1]) < 1:
        sys.exit("Uso: python scripts/criar_clientes_de_teste.py <quantidade>")
    if not os.getenv("XANO_BASE_URL", "").strip():
        sys.exit(
            "XANO_BASE_URL não está no .env. Copie o .env.example para .env e "
            "preencha os endereços do Xano antes de rodar."
        )
    quantidade = int(sys.argv[1])
    print(f"Criando {quantidade} cliente(s) de teste pelo cadastro público...")
    criados = asyncio.run(criar(quantidade))
    print(
        f"\n{criados} de {quantidade} criado(s) e gravado(s) em "
        f"{contas_de_teste.ARQUIVO.name}. Abra a tela de entrada e aperte Alt+2."
    )


if __name__ == "__main__":
    main()
