"""Promove uma conta do PetBits a administradora da clínica.

Por que isto é um script e não uma tela: o cadastro pelo site cria sempre
`role: "member"`, e é essa a razão de ele poder ser público. Se existisse um
jeito de virar admin pela aplicação, existiria um jeito de invadi-la — foi
exatamente esse o buraco que o template do Xano trazia, em que qualquer membro
virava administrador com duas requisições.

Então quem promove é alguém que já tem a chave do workspace, fora da
aplicação. São dois caminhos, e o segundo não precisa deste script:

1. Este script, com o `XANO_META_TOKEN` no `.env`:

       python scripts/promover_admin.py voce@email.com

2. O painel do Xano: Database -> tabela `user` -> a sua linha -> trocar
   `role` de `member` para `admin`. A coluna é `private`, o que a esconde da
   API, não do painel.

O token de metadados vence (7 dias por padrão). Se este script disser que não
tem autorização, gere outro em Settings -> Metadata API no painel do Xano, ou
use o caminho 2.
"""

import os
import sys

import httpx
from dotenv import load_dotenv

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(RAIZ, ".env"))

INSTANCIA = "https://x8ki-letl-twmt.n7.xano.io/api:meta"
WORKSPACE = 151959
TABELA_USER = 770882


def main() -> int:
    if len(sys.argv) != 2:
        print("uso: python scripts/promover_admin.py <email>")
        return 2
    email = sys.argv[1].strip().lower()

    token = os.getenv("XANO_META_TOKEN", "").strip()
    if not token:
        print(
            "XANO_META_TOKEN não está no .env.\n"
            "Gere um em Settings -> Metadata API no painel do Xano, ou troque a\n"
            "coluna `role` direto na tabela `user` pelo painel."
        )
        return 1

    cabecalhos = {"Authorization": f"Bearer {token}"}
    base = f"{INSTANCIA}/workspace/{WORKSPACE}/table/{TABELA_USER}/content"

    resposta = httpx.get(
        base, headers=cabecalhos, params={"page": 1, "per_page": 200}, timeout=60
    )
    if resposta.status_code == 401:
        print("O token de metadados não vale mais. Gere outro no painel do Xano.")
        return 1
    if resposta.status_code != 200:
        print(f"Não consegui ler a tabela user: {resposta.status_code}")
        return 1

    corpo = resposta.json()
    usuarios = corpo.get("items", corpo) if isinstance(corpo, dict) else corpo
    alvo = next((u for u in usuarios if (u.get("email") or "").lower() == email), None)

    if alvo is None:
        print(f"Não existe conta com o e-mail {email}.")
        if usuarios:
            print("Contas cadastradas:")
            for u in usuarios:
                print(f"  {u.get('email')}  ({u.get('role')})")
        else:
            print("Não há nenhuma conta ainda — cadastre-se em /cadastro primeiro.")
        return 1

    if alvo.get("role") == "admin":
        print(f"{email} já é administradora.")
        return 0

    troca = httpx.put(
        f"{base}/{alvo['id']}",
        headers=cabecalhos,
        json={"role": "admin"},
        timeout=60,
    )
    if troca.status_code != 200:
        print(f"Falhou ao promover: {troca.status_code} {troca.text[:200]}")
        return 1

    print(f"{email} agora é administradora. Saia e entre de novo no site.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
