"""Cadastra 15 produtos de exemplo na loja.

Uso, na raiz do projeto:

    python scripts/criar_produtos_de_exemplo.py

Entra com a PRIMEIRA conta de equipe com senha do `contas-de-teste.local.txt`
(a lista do `Alt+1`) e cadastra pelo mesmo `POST equipe/produtos` da tela
(change `produtos-de-exemplo-por-script`, D1). Produto cujo nome já exista no
catálogo é pulado (D3), então rodar de novo não duplica.

A senha não aparece na saída: só o e-mail da conta usada.
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJETO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJETO))
load_dotenv(PROJETO / ".env", override=True)

from petbits import contas_de_teste, xano  # noqa: E402

PAUSA = 2.2  # folga sobre o limite de 10 requisições a cada 20 s (D4)

PRODUTOS = [
    # nome, categoria, marca, unidade, preço, estoque, descrição
    ("Ração cães adultos 10 kg", "racao", "Golden", "pacote 10 kg", 189.90, 12,
     "Ração premium especial para cães adultos de porte médio."),
    ("Ração cães filhotes 3 kg", "racao", "Premier", "pacote 3 kg", 94.90, 15,
     "Para filhotes de até 12 meses."),
    ("Ração gatos castrados 1 kg", "racao", "Whiskas", "pacote 1 kg", 42.50, 20,
     "Controle de peso para gatos castrados."),
    ("Sachê gatos sabor salmão", "racao", "Whiskas", "sachê 85 g", 3.49, 60,
     "Alimento úmido completo."),
    ("Bifinho de frango", "petisco", "Keldog", "pacote 65 g", 9.90, 40,
     "Petisco mastigável para cães."),
    ("Ossinho de couro", "petisco", "Pet Bone", "un", 7.50, 35,
     "Ajuda na limpeza dos dentes."),
    ("Bolinha com guizo", "brinquedo", "Chalesco", "un", 12.90, 25,
     "Brinquedo para gatos e cães pequenos."),
    ("Corda para morder", "brinquedo", "Jambo", "un", 24.90, 18,
     "Corda de algodão trançado."),
    ("Arranhador de papelão", "brinquedo", "Furacão Pet", "un", 39.90, 10,
     "Com erva-de-gato inclusa."),
    ("Shampoo neutro", "higiene", "Sanol", "frasco 500 ml", 19.90, 22,
     "Para cães e gatos de pele sensível."),
    ("Areia higiênica", "higiene", "Pipicat", "pacote 4 kg", 24.90, 30,
     "Areia granulada com controle de odor."),
    ("Tapete higiênico (30 un)", "higiene", "Super Secão", "pacote 30 un", 59.90, 14,
     "Tapetes absorventes para cães."),
    ("Coleira ajustável média", "acessorio", "Zee.Dog", "un", 49.90, 16,
     "Coleira de nylon com fecho de segurança."),
    ("Comedouro inox", "acessorio", "Chalesco", "un", 29.90, 20,
     "Comedouro de aço inox antiderrapante, 500 ml."),
    ("Vermífugo para cães até 10 kg", "medicamento", "Drontal", "caixa 2 comprimidos",
     45.90, 18, "Use conforme orientação do veterinário."),
]


def conta_de_equipe() -> dict | None:
    contas = contas_de_teste.do_grupo(contas_de_teste.EQUIPE)
    return contas[0] if contas else None


async def cadastrar() -> int:
    conta = conta_de_equipe()
    if conta is None:
        sys.exit(
            "Nenhuma conta de equipe com senha em contas-de-teste.local.txt. "
            "Preencha a senha de uma conta EQUIPE antes de rodar."
        )
    print(f"Entrando com {conta['email']}...")
    sessao = await xano.entrar(conta["email"], conta["senha"])
    token = sessao["authToken"]

    perfil = await xano.usuario_atual(token)
    if not xano.eh_equipe((perfil or {}).get("role") or ""):
        sys.exit(
            f"A conta {conta['email']} não é de equipe (papel "
            f"'{(perfil or {}).get('role') or 'vazio'}'). Nada foi cadastrado."
        )

    existentes = {
        (p.get("nome") or "").strip().lower()
        for p in await xano.listar_produtos(token=token)
    }
    criados = 0
    for nome, categoria, marca, unidade, preco, estoque, descricao in PRODUTOS:
        if nome.lower() in existentes:
            print(f"  já existe  {nome}")
            continue
        await asyncio.sleep(PAUSA)
        try:
            await xano.criar_produto(
                {
                    "nome": nome,
                    "categoria": categoria,
                    "marca": marca,
                    "unidade": unidade,
                    "preco": preco,
                    "estoque": estoque,
                    "descricao": descricao,
                },
                token=token,
            )
        except xano.XanoError as erro:
            print(f"  recusado   {nome}: {erro}")
        else:
            criados += 1
            print(f"  criado     {nome}")
    return criados


def main() -> None:
    if not os.getenv("XANO_BASE_URL", "").strip():
        sys.exit("XANO_BASE_URL não está no .env. Preencha o .env antes de rodar.")
    criados = asyncio.run(cadastrar())
    print(f"\n{criados} produto(s) cadastrado(s). Veja em Equipe → Produtos, e na Loja.")


if __name__ == "__main__":
    main()
