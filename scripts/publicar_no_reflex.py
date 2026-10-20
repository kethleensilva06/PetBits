"""Publica o site no Reflex Cloud, sem segredo nem conta de teste (change
`publicacao-no-reflex-cloud`).

Uso, na raiz do projeto, depois de `reflex login` (no navegador):

    python scripts/publicar_no_reflex.py              # só a prévia
    python scripts/publicar_no_reflex.py --publicar   # publica

Por que existe: o `reflex deploy` empacota a pasta INTEIRA do projeto, menos o
que começa com ponto. Isso tira o `.env`, mas mandaria
`contas-de-teste.local.txt` (as senhas das contas de teste), o export do Xano
em `xano/` e pastas que não são do site. E `--envfile .env` mandaria também o
`XANO_META_TOKEN`, que publica no Xano.

Então este script inverte a regra (D1): só vai o que está em `PERMITIDOS`, e
das variáveis só as duas de `VARIAVEIS` (D3). Os valores nunca são impressos.
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

PROJETO = Path(__file__).resolve().parent.parent

# O que o site usa em produção (D1). Arquivo novo na raiz não sobe sem entrar aqui.
PERMITIDOS = ("petbits", "assets", "rxconfig.py", "requirements.txt")

# As únicas variáveis que o site lê (D3). O `XANO_META_TOKEN` fica de fora.
VARIAVEIS = ("XANO_BASE_URL", "XANO_AUTH_BASE_URL")

# O que nunca pode ir, conferido de novo antes de publicar (D4).
PROIBIDOS = (".env", "contas-de-teste.local.txt")
PASTAS_PROIBIDAS = ("xano", ".xano", "scripts", "tests")

NOME_DO_APP = "petbits"

# O prerender da página raiz (D6). O React Router dá 10 s para ele, e nesta
# máquina Windows só importar o `@radix-ui/themes` leva ~16 s (medido: o
# antivírus confere cada um dos centenas de arquivos pequenos que o Node abre).
# O `reflex deploy` compila AQUI antes de enviar, então o limite sobe para 60 s
# no `.web/`, que é gerado e não versionado — por isso o ajuste é refeito a cada
# publicação.
VITE_DO_REACT_ROUTER = Path(".web/node_modules/@react-router/dev/dist/vite.js")
LIMITE_ORIGINAL = "maxRedirects = 0, timeout = 1e4"
LIMITE_NOVO = "maxRedirects = 0, timeout = 6e4"


def tem_login() -> bool:
    """Há login no Reflex Cloud: o token no ambiente ou no arquivo do CLI."""
    if os.environ.get("REFLEX_ACCESS_TOKEN"):
        return True
    try:
        from reflex_cli.constants.hosting import Hosting
    except ImportError:
        return False
    return Path(Hosting.HOSTING_JSON).exists()


def ajustar_limite_do_prerender(arquivo: Path = VITE_DO_REACT_ROUTER) -> str:
    """Sobe o limite do prerender para 60 s (D6). Devolve o que foi feito."""
    if not arquivo.exists():
        return "o .web ainda não existe; o reflex deploy vai criá-lo com o limite de 10 s"
    texto = arquivo.read_text(encoding="utf-8")
    if LIMITE_NOVO in texto:
        return "já em 60 s"
    if LIMITE_ORIGINAL not in texto:
        return "trecho do limite não encontrado (o React Router mudou?); nada alterado"
    arquivo.write_text(texto.replace(LIMITE_ORIGINAL, LIMITE_NOVO), encoding="utf-8")
    return "ajustado de 10 s para 60 s"


def _parece_venv(pasta: Path) -> bool:
    return (pasta / "pyvenv.cfg").exists()


def excluidos(raiz: Path = PROJETO) -> list[Path]:
    """Tudo da raiz que não é oculto nem permitido, para `--exclude-from-backend`.

    O oculto o próprio `reflex deploy` já pula.
    """
    return sorted(item for item in raiz.iterdir()
                  if not item.name.startswith(".") and item.name not in PERMITIDOS)


def arquivos_do_pacote(raiz: Path = PROJETO) -> list[Path]:
    """O que iria no pacote, com as regras de `reflex/utils/build.py` (D2):
    pula oculto, `__pycache__`, venv e `.db`, e o que `excluidos` lista."""
    fora = {p.resolve() for p in excluidos(raiz)}
    arquivos = []
    for pasta, subpastas, nomes in os.walk(raiz, topdown=True):
        pasta = Path(pasta)
        subpastas[:] = [s for s in subpastas
                        if s != "__pycache__" and not s.startswith(".")
                        and not _parece_venv(pasta / s)
                        and (pasta / s).resolve() not in fora]
        for nome in nomes:
            caminho = pasta / nome
            if nome.startswith(".") or nome.endswith(".db") or caminho.resolve() in fora:
                continue
            arquivos.append(caminho.relative_to(raiz))
    return sorted(arquivos)


def problemas(arquivos: list[Path]) -> list[str]:
    """O que impede publicar (D4)."""
    achados = []
    for arquivo in arquivos:
        partes = arquivo.parts
        if arquivo.name in PROIBIDOS or (partes and partes[0] in PASTAS_PROIBIDAS):
            achados.append(f"{arquivo} não pode ir para o Reflex Cloud")
    return achados


def ler_variaveis(arquivo: Path = PROJETO / ".env") -> dict[str, str]:
    """Só as variáveis de `VARIAVEIS`, do `.env` (D3). O resto é ignorado."""
    valores = {}
    if arquivo.exists():
        for linha in arquivo.read_text(encoding="utf-8-sig").splitlines():
            nome, _, valor = linha.strip().partition("=")
            if nome.strip() in VARIAVEIS:
                valores[nome.strip()] = valor.strip().strip('"').strip("'")
    return valores


def comando(variaveis: dict[str, str], raiz: Path = PROJETO) -> list[str]:
    """O `reflex deploy`, com as exclusões e só as duas variáveis."""
    cmd = ["reflex", "deploy", "--app-name", NOME_DO_APP, "--no-interactive", "--no-ssr"]
    for nome in VARIAVEIS:
        cmd += ["--env", f"{nome}={variaveis[nome]}"]
    for item in excluidos(raiz):
        cmd += ["--exclude-from-backend", item.name]
    return cmd


def _sem_valores(cmd: list[str]) -> str:
    """O comando para mostrar, com os valores das variáveis escondidos."""
    return " ".join(p.split("=", 1)[0] + "=…" if "=" in p else p for p in cmd)


def main(argv: list[str]) -> int:
    os.chdir(PROJETO)
    arquivos = arquivos_do_pacote()
    por_pasta = Counter(a.parts[0] if len(a.parts) > 1 else a.name for a in arquivos)
    print("Iriam para o Reflex Cloud (o servidor do site):")
    for nome, quantos in sorted(por_pasta.items()):
        print(f"   {nome:<22} {quantos} arquivo(s)")
    print(f"Ficam de fora: {', '.join(p.name for p in excluidos())}")
    print("Ocultos (.env, .git, .venv...) o reflex deploy já deixa de fora.")

    variaveis = ler_variaveis()
    faltando = [v for v in VARIAVEIS if not variaveis.get(v)]
    print(f"Variáveis enviadas: {', '.join(VARIAVEIS)} (valores não mostrados)")

    erros = problemas(arquivos) + [f"{v} não está no .env" for v in faltando]
    if erros:
        print("\nNão dá para publicar:")
        for erro in erros:
            print(f"   - {erro}")
        return 1

    cmd = comando(variaveis)
    print(f"\nComando: {_sem_valores(cmd)}")
    if "--publicar" not in argv:
        print("\nNada foi enviado. Para publicar: acrescente --publicar.")
        return 0

    # Sem login, o `reflex deploy` sai com erro e sem mensagem (medido). O login
    # tem de ser o do Reflex do projeto, que guarda o token em hosting_v1.json.
    if not tem_login():
        print("\nSem login no Reflex Cloud neste computador. Rode, na raiz do projeto:\n"
              "   .venv\\Scripts\\reflex login\n"
              "e depois este script de novo. Nada foi enviado.")
        return 1

    print(f"Limite do prerender: {ajustar_limite_do_prerender()}")

    executavel = PROJETO / ".venv" / ("Scripts" if os.name == "nt" else "bin") / "reflex"
    if executavel.with_suffix(".exe").exists():
        executavel = executavel.with_suffix(".exe")
    if executavel.exists():
        cmd[0] = str(executavel)
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
