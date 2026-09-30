"""Desvincula a conta do Xano da extensão do VS Code.

A extensão guarda o token em dois lugares, e os dois precisam sair:

1. **A credencial**, no SecretStorage do VS Code — uma linha no banco
   `state.vscdb`, sob a chave
   `secret://{"extensionId":"xano.xanoscript","key":"XanoApiToken"}`.
2. **A escolha de instância e workspace**, em `.xano/config.json` na raiz do
   projeto. Sem apagar isso, a extensão continua tentando abrir o workspace
   151959 da conta antiga mesmo depois de você entrar com a outra.

**O VS Code precisa estar fechado.** Ele mantém o `state.vscdb` aberto e
regrava o conteúdo que tem em memória ao sair — apagar a linha com ele aberto
não adianta, e escrever no banco em uso pode corrompê-lo. Por isso o script
se recusa a rodar enquanto houver processo do VS Code.

Uso:

    # feche o VS Code primeiro
    python scripts/desvincular_xano.py

Depois de reabrir o VS Code, a extensão vai pedir login de novo: use o painel
do Xano na barra lateral, ou a Command Palette -> "Xano: Login".
"""

import json
import os
import shutil
import sqlite3
import subprocess
import sys

CHAVE_SEGREDO = 'secret://{"extensionId":"xano.xanoscript","key":"XanoApiToken"}'

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def vscode_aberto() -> bool:
    """True se houver algum processo do VS Code rodando."""
    try:
        saida = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Code.exe", "/NH"],
            capture_output=True,
            text=True,
            timeout=30,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return "Code.exe" in saida


def bancos_de_estado() -> list[str]:
    """Os state.vscdb do VS Code estável e do Insiders, se existirem."""
    roaming = os.environ.get("APPDATA", "")
    candidatos = [
        os.path.join(roaming, "Code", "User", "globalStorage", "state.vscdb"),
        os.path.join(
            roaming, "Code - Insiders", "User", "globalStorage", "state.vscdb"
        ),
    ]
    return [c for c in candidatos if os.path.exists(c)]


def limpar_credencial(caminho: str) -> bool:
    """Apaga a linha do token. Devolve True se havia algo para apagar."""
    backup = caminho + ".antes-de-desvincular"
    shutil.copy2(caminho, backup)

    con = sqlite3.connect(caminho)
    try:
        existia = con.execute(
            "SELECT COUNT(*) FROM ItemTable WHERE key = ?", (CHAVE_SEGREDO,)
        ).fetchone()[0]
        if existia:
            con.execute("DELETE FROM ItemTable WHERE key = ?", (CHAVE_SEGREDO,))
            con.commit()
    finally:
        con.close()

    if existia:
        print(f"  credencial removida de {caminho}")
        print(f"  (cópia de segurança em {backup})")
    else:
        print(f"  nenhuma credencial do Xano em {caminho}")
        os.remove(backup)
    return bool(existia)


def limpar_config_do_projeto() -> bool:
    """Zera a instância e o workspace escolhidos, preservando os caminhos."""
    caminho = os.path.join(RAIZ, ".xano", "config.json")
    if not os.path.exists(caminho):
        print("  .xano/config.json não existe — nada a limpar")
        return False

    with open(caminho, encoding="utf-8") as f:
        config = json.load(f)

    antigo = config.get("workspaceName") or config.get("instanceName") or "?"
    # `paths` é convenção do projeto e vale para qualquer conta; só a
    # identificação da instância e do workspace é que pertence à conta antiga.
    limpo = {"paths": config.get("paths", {})}
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(limpo, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"  .xano/config.json zerado (era: {antigo})")
    return True


def main() -> int:
    if vscode_aberto():
        print(
            "O VS Code está aberto.\n\n"
            "Feche-o completamente antes de rodar este script. Ele mantém o\n"
            "banco de estado aberto e regrava o que tem em memória ao sair,\n"
            "então apagar a credencial agora não teria efeito."
        )
        return 1

    print("Desvinculando a conta do Xano:\n")

    bancos = bancos_de_estado()
    if not bancos:
        print("  não encontrei o state.vscdb do VS Code")
    for banco in bancos:
        limpar_credencial(banco)

    limpar_config_do_projeto()

    print(
        "\nPronto. Ao reabrir o VS Code, a extensão do Xano vai pedir login.\n"
        "Entre com a conta nova e escolha a instância e o workspace dela."
    )
    print(
        "\nLembre também de trocar no .env: XANO_BASE_URL, XANO_AUTH_BASE_URL\n"
        "e XANO_META_TOKEN apontam para a conta antiga."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
