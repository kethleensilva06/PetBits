"""Publica no Xano só os arquivos pedidos, com prévia (change
`publicacao-por-script`).

Uso, na raiz do projeto:

    python scripts/publicar.py apis/pet_bits/pedido_create.xs tables/pedido.xs
    python scripts/publicar.py --publicar apis/pet_bits/pedido_create.xs
    python scripts/publicar.py --conferir

Sem `--publicar`, só mostra a prévia (`--dry-run`) do que mudaria. Com
`--publicar`, mostra a prévia de novo e publica. `--conferir` compara todos os
`.xs` do repositório com o workspace do Xano.

O caminho de cada arquivo no Xano CLI é deduzido do CONTEÚDO (D1) — não há
tabela mantida à mão. Nunca usa `--sync` nem `--delete` (D2): o que não foi
nomeado não é tocado.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PROJETO = Path(__file__).resolve().parent.parent
PASTAS = ("tables", "functions", "apis")

RE_TABELA = re.compile(r'^table\s+"?([\w]+)"?\s*\{', re.MULTILINE)
RE_FUNCAO = re.compile(r'^function\s+"([^"]+)"\s*\{', re.MULTILINE)
RE_QUERY = re.compile(r'^query\s+("?)([^"\s]+)\1\s+verb=(\w+)', re.MULTILINE)
RE_GRUPO = re.compile(r'^\s*api_group\s*=\s*"([^"]+)"', re.MULTILINE)
RE_DECL_GRUPO = re.compile(r'^api_group\s+(?:"([^"]+)"|(\w+))\s*\{', re.MULTILINE)


def grupo_cli(nome: str) -> str:
    """`PetBits` → `pet_bits`; `Quick Start` → `quick_start`; `Event Logs` → `event_logs`."""
    nome = nome.strip().replace(" ", "_")
    nome = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", nome)
    return re.sub(r"_+", "_", nome).lower()


def caminho_cli(texto: str) -> str | None:
    """O caminho que o Xano CLI usa para este documento, ou None se não for
    tabela, função, grupo de API nem endpoint."""
    if m := RE_DECL_GRUPO.search(texto):
        grupo = grupo_cli(m.group(1) or m.group(2))
        return f"api/{grupo}/{grupo}.xs"
    if m := RE_TABELA.search(texto):
        return f"table/{m.group(1)}.xs"
    if m := RE_FUNCAO.search(texto):
        grupo, _, nome = m.group(1).rpartition("/")
        return f"function/{grupo_cli(grupo)}/{nome}.xs" if grupo else f"function/{nome}.xs"
    if m := RE_QUERY.search(texto):
        grupo = RE_GRUPO.search(texto)
        if not grupo:
            return None
        rota = re.sub(r"\{(\w+)\}", r"\1", m.group(2))
        return f"api/{grupo_cli(grupo.group(1))}/{rota}_{m.group(3).upper()}.xs"
    return None


def normalizado(texto: str) -> list[str]:
    """O código sem o que a exportação do Xano muda: comentários, `guid`,
    `description`, linhas em branco e espaços nas pontas."""
    linhas = []
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("//"):
            continue
        if linha.startswith(("guid =", "description =")):
            continue
        linhas.append(linha)
    return linhas


def comando_xano() -> str:
    caminho = shutil.which("xano")
    if not caminho:
        sys.exit("Xano CLI não encontrado. Instale com `npm install -g @xano/cli` e rode `xano auth`.")
    return caminho


def rodar(argumentos: list[str], pasta: Path | None = None) -> str:
    r = subprocess.run(argumentos, cwd=pasta, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    saida = (r.stdout or "") + (r.stderr or "")
    if r.returncode != 0:
        print(saida)
        sys.exit(f"Falhou: xano {' '.join(argumentos[1:3])}")
    return saida


def puxar() -> Path:
    """Workspace inteiro numa pasta nova e de caminho curto (D2)."""
    pasta = Path(os.environ.get("TEMP", "/tmp")) / f"pbpub{time.strftime('%H%M%S')}"
    pasta.mkdir(parents=True)
    rodar([comando_xano(), "workspace", "pull", "-d", "."], pasta)
    return pasta


def validar(arquivos: list[Path]) -> None:
    node = shutil.which("node")
    if not node:
        sys.exit("Node não encontrado para validar os arquivos.")
    r = subprocess.run([node, str(PROJETO / "scripts" / "validar_xanoscript.mjs"),
                        *map(str, arquivos)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(r.stdout + r.stderr)
        sys.exit("Há arquivo inválido. Nada foi puxado nem publicado.")


def publicar(arquivos: list[Path], de_verdade: bool) -> None:
    validar(arquivos)
    destinos = {}
    for arquivo in arquivos:
        destino = caminho_cli(arquivo.read_text(encoding="utf-8"))
        if destino is None:
            sys.exit(f"{arquivo}: não é tabela, função nem endpoint.")
        destinos[arquivo] = destino
        print(f"  {arquivo.relative_to(PROJETO).as_posix():50} → {destino}")

    pasta = puxar()
    # O CLI compara texto cru: o arquivo exportado pelo Xano difere do
    # repositório em comentários, `guid` e `description` mesmo com o código
    # igual, e a prévia mostraria UPDATE. Arquivo cujo código normalizado é
    # igual ao do Xano fica FORA — foi assim que o `entrar POST` quase foi
    # republicado sem ninguém ter mexido nele.
    for arquivo, destino in list(destinos.items()):
        alvo = pasta / destino
        if alvo.exists() and normalizado(alvo.read_text(encoding="utf-8")) == \
                normalizado(arquivo.read_text(encoding="utf-8")):
            print(f"  igual ao Xano, fica fora: {arquivo.relative_to(PROJETO).as_posix()}")
            del destinos[arquivo]
            continue
        alvo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(arquivo, alvo)
    if not destinos:
        print("\nNenhum arquivo tem código diferente do que está no Xano. Nada a publicar.")
        return

    filtros = [x for d in destinos.values() for x in ("-i", d)]
    print("\nPrévia:")
    print(rodar([comando_xano(), "workspace", "push", "-d", ".", *filtros, "--dry-run"], pasta))
    if not de_verdade:
        print("Nada foi publicado. Para publicar: acrescente --publicar.")
        return
    print("Publicando...")
    print(rodar([comando_xano(), "workspace", "push", "-d", ".", *filtros, "--force"], pasta))


def conferir() -> int:
    pasta = puxar()
    no_xano = {p.relative_to(pasta).as_posix() for p in pasta.rglob("*.xs")
               if p.parts[len(pasta.parts)] in ("table", "function", "api")}
    no_repositorio = {}
    for raiz in PASTAS:
        for arquivo in (PROJETO / raiz).rglob("*.xs"):
            destino = caminho_cli(arquivo.read_text(encoding="utf-8"))
            if destino:
                no_repositorio[destino] = arquivo.relative_to(PROJETO).as_posix()
    so_repositorio = sorted(set(no_repositorio) - no_xano)
    so_xano = sorted(no_xano - set(no_repositorio))
    print(f"{len(set(no_repositorio) & no_xano)} documento(s) nos dois lados.\n")
    print("No repositório, não no Xano:")
    for d in so_repositorio:
        print(f"  {no_repositorio[d]}  ({d})")
    print("  (nenhum)" if not so_repositorio else "")
    print("No Xano, não no repositório:")
    for d in so_xano:
        print(f"  {d}")
    print("  (nenhum)" if not so_xano else "")
    return 1 if so_repositorio or so_xano else 0


def main() -> None:
    argumentos = sys.argv[1:]
    if argumentos == ["--conferir"]:
        raise SystemExit(conferir())
    de_verdade = "--publicar" in argumentos
    arquivos = [PROJETO / a for a in argumentos if a != "--publicar"]
    if not arquivos:
        sys.exit(__doc__)
    for arquivo in arquivos:
        if not arquivo.is_file():
            sys.exit(f"Arquivo não encontrado: {arquivo}")
    publicar(arquivos, de_verdade)


if __name__ == "__main__":
    main()
