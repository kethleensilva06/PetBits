"""Publica a parte visual do site no GitHub Pages, ligada ao servidor do Reflex
Cloud (change `site-no-github-pages`).

Uso, na raiz do projeto, com o servidor de desenvolvimento PARADO (os dois usam
`.web/`):

    python scripts/publicar_no_github_pages.py              # compila e mostra o plano
    python scripts/publicar_no_github_pages.py --publicar   # e envia a branch gh-pages

O GitHub Pages só serve arquivos; o servidor do PetBits continua no Reflex
Cloud (`publicar_no_reflex.py`). Esta versão é compilada com:
- `REFLEX_FRONTEND_PATH=/PetBits`, porque o Pages do repositório mora em
  https://kethleensilva06.github.io/PetBits/;
- `REFLEX_API_URL` apontando para o servidor do Reflex Cloud.

Só vai o que o navegador recebe de qualquer jeito: HTML, JS, CSS, imagens e o
endereço do servidor. Nada do `.env`.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PROJETO = Path(__file__).resolve().parent.parent
PREFIXO = "/PetBits"
SERVIDOR = "https://8429d463-9a17-4b75-9643-2e4c6811247b.fly.dev"
ENDERECO = "https://kethleensilva06.github.io/PetBits"
REPOSITORIO = "https://github.com/kethleensilva06/PetBits.git"
BRANCH = "gh-pages"
BUILD = PROJETO / ".web" / "build" / "client"


def compilar() -> None:
    """`reflex export` com o prefixo e o servidor.

    MEDIDO: no Windows o Reflex 0.9.10 quebra no último passo, que move os
    arquivos para uma subpasta com o nome do prefixo (`PosixPath` não existe no
    Windows). Esse passo não serve ao Pages, então a falha é aceita se o build
    estiver completo.
    """
    env = {**os.environ, "REFLEX_FRONTEND_PATH": PREFIXO, "REFLEX_API_URL": SERVIDOR,
           "REFLEX_DEPLOY_URL": ENDERECO, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    reflex = PROJETO / ".venv" / ("Scripts/reflex.exe" if os.name == "nt" else "bin/reflex")
    subprocess.call([str(reflex), "export", "--frontend-only", "--no-zip"], cwd=PROJETO, env=env)


def conferir_build(build: Path = BUILD) -> list[str]:
    """O que falta no build para publicar."""
    faltas = []
    for exigido in ("assets", "fotos", f"{PREFIXO.strip('/')}/index.html", "404.html"):
        if not (build / exigido).exists():
            faltas.append(f"{exigido} não está no build")
    ambiente = list((build / "assets").glob("reflex-env-*.js"))
    if not ambiente or SERVIDOR not in ambiente[0].read_text(encoding="utf-8"):
        faltas.append("o build não aponta para o servidor do Reflex Cloud")
    return faltas


def montar(destino: Path, build: Path = BUILD) -> int:
    """A pasta do Pages: a raiz da branch já é servida em /PetBits/, então as
    páginas prerenderizadas em `PetBits/` sobem para a raiz. Sem os `.gz` (o
    Pages comprime sozinho), e com `.nojekyll` para ele não esconder `_*`."""
    pasta_prefixo = build / PREFIXO.strip("/")
    for item in build.iterdir():
        if item == pasta_prefixo or item.name.startswith(PREFIXO.strip("/") + "."):
            continue
        _copiar(item, destino / item.name)
    for item in pasta_prefixo.iterdir():
        _copiar(item, destino / item.name)
    (destino / ".nojekyll").write_text("", encoding="utf-8")
    return sum(1 for _ in destino.rglob("*") if _.is_file())


def _copiar(origem: Path, destino: Path) -> None:
    if origem.is_dir():
        shutil.copytree(origem, destino, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns("*.gz"))
    elif not origem.name.endswith(".gz"):
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, destino)


def enviar(pasta: Path) -> int:
    """Um commit novo na branch gh-pages, com o conteúdo inteiro da pasta."""
    git = ["git", "-C", str(pasta)]
    passos = [
        git + ["init", "-q", "-b", BRANCH],
        git + ["-c", "core.autocrlf=false", "add", "-A"],
        git + ["commit", "-q", "-m", "GitHub Pages: parte visual do PetBits ligada ao Reflex Cloud"],
        git + ["push", "-q", "--force", REPOSITORIO, f"{BRANCH}:{BRANCH}"],
    ]
    for passo in passos:
        codigo = subprocess.call(passo)
        if codigo:
            return codigo
    return 0


def main(argv: list[str]) -> int:
    if "--sem-compilar" not in argv:
        compilar()
    faltas = conferir_build()
    if faltas:
        print("Não dá para publicar:")
        for falta in faltas:
            print(f"   - {falta}")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        pasta = Path(tmp) / "pages"
        pasta.mkdir()
        total = montar(pasta)
        print(f"Pasta do Pages: {total} arquivos; servidor {SERVIDOR}; endereço {ENDERECO}/")
        if "--publicar" not in argv:
            print("Nada foi enviado. Para publicar: acrescente --publicar.")
            return 0
        return enviar(pasta)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
