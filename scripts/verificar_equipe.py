"""A guarda dos endpoints de equipe.

Por que isto existe: `colaborador` e `servico` não têm coluna de dono. Na
superfície do tutor a prova de posse **é** o `where` da consulta — se ela
sumir, a listagem devolve dado alheio e o teste de duas contas acusa na hora.
Aqui não há `where` para esquecer: a chamada a `PetBits/exige_equipe` é o
único mecanismo de recusa, e um endpoint de equipe sem ela devolve a clínica
inteira para qualquer conta autenticada — isto é, para qualquer visitante que
se cadastrou.

E **o parser aprova o arquivo com e sem a prova**. Reparar na *ausência* de
uma linha é muito mais difícil do que reparar numa linha errada; esta guarda
transforma isso numa pergunta que um script responde (design.md, D9).

Três conferências:

1. **A prova em todo endpoint de equipe.** Cada `apis/pet_bits/equipe_*.xs`
   tem `auth = "user"`, `precondition ($auth.id > 0)` e
   `function.run "PetBits/exige_equipe"` — e a prova vem **antes** do primeiro
   `db.*`, porque nada é lido antes de o direito de ler estar estabelecido.
   E vem **solta na `stack`**, não dentro de um ramo: prova que só roda em
   alguns caminhos está ausente nos outros, e a conferência de ordem sozinha
   não repara nisso — um `function.run` dentro de um `conditional` está
   presente e está antes do `db.*`, e ainda assim pode nunca rodar.
2. **A regra inversa.** Nenhum arquivo fora de `equipe_*` chama a prova. Um
   `equipe_*.xs` renomeado some do olhar da conferência 1 sem erro nenhum; e
   uma prova de papel numa superfície de tutor é o ramo por papel que o D1
   existe para impedir.
3. **Definir não é chamar.** `functions/pet_bits/exige_equipe.xs` *declara* a
   prova. A conferência 2 não pode confundir o arquivo da função com um
   endpoint que a chama.

O que esta guarda **não** alcança, e precisa estar escrito: endpoint criado
pela interface do Xano não passa pelo repositório, e portanto não passa por
aqui. Para esse caso só existe o teste de duas contas — token de tutor dá 403,
token de admin dá 200.

Uso:

    python scripts/verificar_equipe.py

Sai com código 1 quando acusa e 0 quando passa limpa, para servir em CI.
"""

import re
import subprocess
from pathlib import Path

PROJETO = Path(__file__).resolve().parent.parent

PASTA_ENDPOINTS = PROJETO / "apis" / "pet_bits"
GLOB_EQUIPE = "equipe_*.xs"

PROVA = "PetBits/exige_equipe"
ARQUIVO_DA_FUNCAO = PROJETO / "functions" / "pet_bits" / "exige_equipe.xs"

# A prova de GERÊNCIA, um degrau acima. Desde a change `papeis-e-abas`, manter
# o quadro de colaboradores é da gerência; ler continua sendo de toda a equipe.
PROVA_GERENCIA = "PetBits/exige_gerencia"
ARQUIVO_DA_GERENCIA = PROJETO / "functions" / "pet_bits" / "exige_gerencia.xs"

# Exatamente os dois arquivos que mantêm o quadro — nem um a mais, nem um a
# menos. Trocar uma prova pela outra é a alteração que não se vê num diff: as
# duas linhas têm o mesmo formato e quase o mesmo tamanho. O efeito é
# silencioso — o endpoint continua recusando tutor, continua passando no teste
# de duas contas, e passa a aceitar equipe comum onde devia exigir gerência.
ESCRITAS_DE_COLABORADOR = {
    "equipe_colaborador_create.xs",
    "equipe_colaborador_update.xs",
}

# `auth` precisa ser exatamente "user": a captura existe para a mensagem poder
# dizer *qual* valor está lá, em vez de só "faltou".
RE_AUTH = re.compile(r'^[ \t]*auth[ \t]*=[ \t]*"([^"]*)"[ \t]*$', re.MULTILINE)
RE_SESSAO = re.compile(r"precondition[ \t]*\([ \t]*\$auth\.id[ \t]*>[ \t]*0[ \t]*\)")
# O espaço depois de `function.run` é opcional porque o parser oficial o trata
# assim: `function.run"PetBits/exige_equipe"` foi dado como válido por
# `node scripts/validar_xanoscript.mjs`. Exigir o espaço deixava a conferência
# 2 cega para um portão de papel escrito dessa forma numa superfície de tutor
# — que é exatamente o ramo do D1.
def _re_chamada(nome: str) -> "re.Pattern[str]":
    return re.compile(r'function\.run[ \t]*"' + re.escape(nome) + r'"')


# Qualquer uma das duas serve para a conferência 1 (todo endpoint de equipe
# prova alguma coisa) e para a 2 (ninguém de fora prova nada). *Qual* das duas
# é a pergunta da conferência 4.
RE_CHAMADA = re.compile(
    r'function\.run[ \t]*"(?:'
    + "|".join(re.escape(x) for x in (PROVA, PROVA_GERENCIA))
    + r')"'
)
RE_CHAMADA_GERENCIA = _re_chamada(PROVA_GERENCIA)
RE_DEFINICAO = re.compile(r'^[ \t]*function[ \t]*"' + re.escape(PROVA) + r'"', re.MULTILINE)
RE_DB = re.compile(r"^[ \t]*db\.[a-z_]+\b")
RE_STACK = re.compile(r"^[ \t]*stack[ \t]*\{", re.MULTILINE)
RE_TIPO = re.compile(r"^(query|function|table|trigger|task|addon|agent|tool|api_group)\b", re.MULTILINE)


def sem_comentarios(texto: str) -> str:
    """O mesmo texto com os comentários `//` apagados, linha a linha.

    Isto não é capricho, é o que separa a guarda de um `grep`, e serve nas
    duas direções:

    - Comentar a linha da prova para depurar e esquecer de descomentar é
      *exatamente* a regressão que esta guarda procura. Um `grep` cru acharia
      a linha e diria que está tudo bem.
    - Os `.xs` deste projeto explicam o porquê em comentários longos, e um
      deles vai acabar citando `function.run "PetBits/exige_equipe"` como
      exemplo. Sem isto, a conferência 2 acusaria o comentário.

    Só `//` fora de string: os `.xs` do projeto não usam `/* */`, e `//`
    dentro de string acontece de verdade (uma URL numa `description`). Uma
    string de várias linhas abriria um buraco aqui, mas o XanoScript não tem
    uma — nem as aspas duplas nem a crase atravessam a quebra de linha.
    """
    limpas = []
    for linha in texto.splitlines():
        delimitador = ""
        escapado = False
        corte = len(linha)
        for i, c in enumerate(linha):
            if escapado:
                escapado = False
            elif delimitador:
                if c == "\\":
                    escapado = True
                elif c == delimitador:
                    delimitador = ""
            elif c in '"`':
                delimitador = c
            elif c == "/" and linha[i + 1 : i + 2] == "/":
                corte = i
                break
        limpas.append(linha[:corte])
    return "\n".join(limpas)


def apagar_textos(codigo: str) -> str:
    """O mesmo código com o miolo de cada string trocado por espaços.

    Serve só para **contar chaves**, e o comprimento é preservado de
    propósito, para que as posições que os regexes acharam no código continuem
    valendo aqui. Sem isto, uma `description = "o bloco {x}"` abriria um nível
    que o arquivo não tem e a conferência de aninhamento acusaria um arquivo
    correto.

    Mesmas regras do varredor de comentários: `"` e crase delimitam, a barra
    invertida escapa, nada atravessa a quebra de linha.
    """
    limpas = []
    for linha in codigo.splitlines():
        pedacos = []
        delimitador = ""
        escapado = False
        for c in linha:
            if escapado:
                pedacos.append(" ")
                escapado = False
            elif delimitador:
                if c == "\\":
                    pedacos.append(" ")
                    escapado = True
                elif c == delimitador:
                    pedacos.append(c)
                    delimitador = ""
                else:
                    pedacos.append(" ")
            elif c in '"`':
                pedacos.append(c)
                delimitador = c
            else:
                pedacos.append(c)
        limpas.append("".join(pedacos))
    return "\n".join(limpas)


def profundidade(codigo_sem_texto: str, posicao: int) -> int:
    """Quantos blocos estão abertos naquela posição."""
    return (
        codigo_sem_texto.count("{", 0, posicao)
        - codigo_sem_texto.count("}", 0, posicao)
    )


def ler(caminho: Path) -> str:
    """O código do arquivo, já sem comentários."""
    return sem_comentarios(caminho.read_text(encoding="utf-8"))


def relativo(caminho: Path) -> str:
    return caminho.relative_to(PROJETO).as_posix()


def linha_de(codigo: str, posicao: int) -> int:
    return codigo.count("\n", 0, posicao) + 1


def primeiro_db(codigo: str) -> int | None:
    """A linha da primeira instrução `db.*`, ou None se não houver nenhuma."""
    for numero, linha in enumerate(codigo.splitlines(), start=1):
        if RE_DB.match(linha):
            return numero
    return None


def conferir_endpoint(codigo: str) -> list[str]:
    """As falhas de um endpoint de equipe. Lista vazia significa aprovado."""
    falhas = []

    tipo = RE_TIPO.search(codigo)
    if tipo is None or tipo.group(1) != "query":
        achado = tipo.group(1) if tipo else "nenhuma declaração reconhecida"
        falhas.append(
            f"declara `{achado}`, não `query`: está em apis/pet_bits/ com nome "
            "de endpoint de equipe mas não é um endpoint"
        )

    auth = RE_AUTH.search(codigo)
    if auth is None:
        falhas.append(
            '1ª conferência: sem `auth = "user"` — endpoint de equipe sem auth '
            "é a clínica inteira aberta a quem não tem token nenhum"
        )
    elif auth.group(1) != "user":
        falhas.append(
            f'1ª conferência: `auth = "{auth.group(1)}"`, esperado `auth = "user"`'
        )

    if RE_SESSAO.search(codigo) is None:
        falhas.append(
            "1ª conferência: sem `precondition ($auth.id > 0)` — com o id "
            "zerado a prova decidiria sobre uma conta que ninguém autenticou"
        )

    chamada = RE_CHAMADA.search(codigo)
    if chamada is None:
        falhas.append(
            f'1ª conferência: sem `function.run "{PROVA}"` nem '
            f'`"{PROVA_GERENCIA}"` — sem coluna de dono não há `where` para '
            "recortar a consulta, então a tabela inteira vai para qualquer "
            "conta autenticada"
        )
    else:
        # A ordem é desenho, não arrumação (design.md, D2): o arquivo pode ter
        # as três linhas e ainda assim ler antes de provar.
        linha_prova = linha_de(codigo, chamada.start())
        linha_db = primeiro_db(codigo)
        if linha_db is not None and linha_db < linha_prova:
            falhas.append(
                f"1ª conferência: `db.*` na linha {linha_db} vem antes da prova "
                f"na linha {linha_prova} — a consulta roda antes de o direito "
                "de ler estar estabelecido"
            )

        # E a prova tem de estar **solta na `stack`**. Estar presente e estar
        # antes do `db.*` não basta: dentro de um `conditional` ela cumpre as
        # duas coisas e mesmo assim não roda no ramo que não entrou — e aí o
        # `db.query` abaixo devolve a clínica inteira, que é precisamente o
        # que esta guarda existe para impedir.
        sem_texto = apagar_textos(codigo)
        bloco = RE_STACK.search(sem_texto)
        if bloco is not None:
            nivel_da_stack = profundidade(sem_texto, bloco.end())
            nivel_da_prova = profundidade(sem_texto, chamada.start())
            if nivel_da_prova > nivel_da_stack:
                falhas.append(
                    f"1ª conferência: a prova na linha {linha_prova} está "
                    f"aninhada {nivel_da_prova - nivel_da_stack} nível(is) "
                    "dentro da `stack`, e não solta nela — prova dentro de um "
                    "ramo não roda no caminho que não entrou no ramo, e esse "
                    "caminho lê a clínica inteira"
                )

    return falhas


def conferencia_1() -> tuple[int, list[Path]]:
    """A prova em todo endpoint de equipe. Devolve (falhas, arquivos vistos)."""
    print("1. A prova em todo endpoint de equipe\n")

    arquivos = sorted(PASTA_ENDPOINTS.glob(GLOB_EQUIPE))
    if not arquivos:
        # Passa, mas em voz alta: uma guarda que não conferiu nada e diz "ok"
        # é pior que guarda nenhuma, porque alguém lê o "ok" como garantia.
        print(
            f"   AVISO  nenhum arquivo casou com "
            f"{relativo(PASTA_ENDPOINTS)}/{GLOB_EQUIPE}\n"
            "          não há endpoint de equipe para conferir — se já deveria "
            "haver,\n          o problema é o nome do arquivo, não a guarda\n"
        )
        return 0, arquivos

    falhas = 0
    for caminho in arquivos:
        problemas = conferir_endpoint(ler(caminho))
        if not problemas:
            print(f"   ok     {relativo(caminho)}")
            continue
        falhas += 1
        print(f"   FALHA  {relativo(caminho)}")
        for p in problemas:
            print(f"          {p}")
    print()
    return falhas, arquivos


def ignorado_pelo_git(caminho: Path) -> bool:
    """O que o git ignora não é do repositório, e esta é uma guarda de
    REPOSITÓRIO.

    Existe por um caso concreto: a extensão do Xano exporta o workspace
    inteiro para `xano/`, no layout dela — o **mesmo** backend que já está em
    `apis/`, `tables/` e `functions/`, escrito de outro jeito. Varrendo o
    disco, a conferência 2 via essas cópias chamando a prova fora da
    convenção de nomes e acusava as onze de uma vez.

    E guarda que acusa onze coisas certas é guarda que ninguém mais lê. O
    perigo não é o alarme falso em si: é ele treinar quem trabalha aqui a
    ignorar a saída, e aí o alarme verdadeiro passa junto.
    """
    if _IGNORADOS is None:
        return False
    return caminho.resolve() in _IGNORADOS


def _ler_ignorados() -> set[Path] | None:
    """Os caminhos que o git ignora. `None` se o git não responder — fora de
    um repositório a guarda continua servindo, varrendo tudo."""
    try:
        saida = subprocess.run(
            ["git", "ls-files", "--others", "--ignored", "--exclude-standard",
             "--directory", "-z"],
            cwd=PROJETO, capture_output=True, text=True, timeout=30, check=True,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return None
    ignorados: set[Path] = set()
    for item in filter(None, saida.split(chr(0))):
        alvo = (PROJETO / item).resolve()
        if alvo.is_dir():
            ignorados.update(f.resolve() for f in alvo.rglob("*.xs"))
        else:
            ignorados.add(alvo)
    return ignorados


_IGNORADOS: set[Path] | None = None


def conferencia_2(endpoints_de_equipe: list[Path]) -> int:
    """A regra inversa: ninguém mais chama a prova."""
    print("2. A regra inversa: só endpoint de equipe chama a prova\n")

    de_equipe = {c.resolve() for c in endpoints_de_equipe}
    falhas = 0
    conferidos = 0

    for caminho in sorted(PROJETO.rglob("*.xs")):
        if ".git" in caminho.parts or caminho.resolve() in de_equipe:
            continue
        if ignorado_pelo_git(caminho):
            continue
        conferidos += 1
        codigo = ler(caminho)
        chamada = RE_CHAMADA.search(codigo)
        if chamada is None:
            continue
        falhas += 1
        print(f"   ACUSA  {relativo(caminho)}")
        print(
            f"          chama `{PROVA}` na linha "
            f"{linha_de(codigo, chamada.start())}, e não é "
            f"apis/pet_bits/{GLOB_EQUIPE}"
        )
        print(
            "          ou o nome saiu da convenção, e a conferência 1 parou de\n"
            "          olhar para ele, ou é uma superfície de tutor ganhando\n"
            "          portão de papel — que é o ramo que o D1 existe para impedir"
        )

    if falhas == 0:
        print(f"   ok     nenhum dos outros {conferidos} arquivos `.xs` chama a prova")
    print()
    return falhas


def conferencia_3(chamadores: int) -> int:
    """Definir a prova não é chamá-la."""
    print("3. Definir a prova não é chamá-la\n")

    if not ARQUIVO_DA_FUNCAO.exists():
        if chamadores == 0:
            # Ninguém depende dela ainda: a ordem do Migration Plan é a função
            # antes dos endpoints, e este é o estado em que ela ainda não foi
            # escrita. Nada a acusar.
            print(
                f"   AVISO  {relativo(ARQUIVO_DA_FUNCAO)} não existe ainda\n"
                "          nenhum endpoint de equipe a chama, então não há o "
                "que conferir — mas\n          ela precisa estar no "
                "repositório antes do primeiro que chamar\n"
            )
            return 0
        # Com endpoints chamando, a ausência do arquivo é acusação, não aviso.
        # Era o buraco da guarda: ela imprimia a regra ("precisa estar no
        # repositório antes de qualquer endpoint que a chame") e depois saía 0
        # com a regra quebrada na tela.
        print(f"   FALHA  {relativo(ARQUIVO_DA_FUNCAO)} não existe")
        print(
            f"          e {chamadores} endpoint(s) de equipe chamam `{PROVA}` "
            "mesmo assim\n"
            "          a função é a única defesa desta superfície: se ela não "
            "está aqui, nada\n"
            "          no repositório diz o que o Xano vai executar no lugar "
            "dela"
        )
        print()
        return 1

    codigo = ler(ARQUIVO_DA_FUNCAO)
    falhas = 0

    if RE_DEFINICAO.search(codigo) is None:
        falhas += 1
        print(f"   FALHA  {relativo(ARQUIVO_DA_FUNCAO)}")
        print(f'          não declara `function "{PROVA}"`')
    elif RE_CHAMADA.search(codigo) is not None:
        # Não é a regra inversa disfarçada: a função chamando a si mesma é
        # recursão, e aqui seria sinal de arquivo trocado.
        falhas += 1
        print(f"   FALHA  {relativo(ARQUIVO_DA_FUNCAO)}")
        print(f"          declara `{PROVA}` e também a chama")
    else:
        print(
            f"   ok     {relativo(ARQUIVO_DA_FUNCAO)} declara a prova, não a chama"
        )

    print()
    return falhas


def conferencia_4(endpoints: list[Path]) -> int:
    """A prova de gerência aparece exatamente onde deve.

    As conferências 1 e 2 só perguntam se *alguma* prova existe. Isso deixa
    passar a troca de uma pela outra, que é o erro mais provável desta
    superfície: as duas linhas têm o mesmo formato, e quem copia um arquivo de
    leitura como modelo de uma escrita leva junto a prova errada.

    O efeito é silencioso — o endpoint continua recusando tutor, continua
    passando no teste de duas contas, e passa a aceitar equipe comum onde
    deveria exigir gerência. É o mesmo tipo de falha que a ausência da prova,
    um degrau acima e sem nada que a denuncie.
    """
    print("4. A prova de gerência aparece exatamente nas escritas de colaborador\n")

    falhas = 0

    if not ARQUIVO_DA_GERENCIA.exists():
        chamam = [c for c in endpoints if RE_CHAMADA_GERENCIA.search(ler(c))]
        if chamam:
            print(f"   FALHA  {relativo(ARQUIVO_DA_GERENCIA)} não existe")
            print(f"          e {len(chamam)} endpoint(s) a chamam mesmo assim")
            print()
            return 1
        print(f"   AVISO  {relativo(ARQUIVO_DA_GERENCIA)} não existe ainda\n")
        return 0

    if RE_CHAMADA_GERENCIA.search(ler(ARQUIVO_DA_GERENCIA)) is not None:
        falhas += 1
        print(f"   FALHA  {relativo(ARQUIVO_DA_GERENCIA)}")
        print(f"          declara `{PROVA_GERENCIA}` e também a chama")
    else:
        print(f"   ok     {relativo(ARQUIVO_DA_GERENCIA)} declara a prova de gerência")

    exigem = {c.name for c in endpoints if RE_CHAMADA_GERENCIA.search(ler(c))}

    for nome in sorted(ESCRITAS_DE_COLABORADOR - exigem):
        falhas += 1
        print(f"   FALHA  apis/pet_bits/{nome}")
        print(
            f"          mantém o quadro e NÃO exige `{PROVA_GERENCIA}`\n"
            "          uma conta de equipe comum passa a editar o cadastro de "
            "um colaborador"
        )

    for nome in sorted(exigem - ESCRITAS_DE_COLABORADOR):
        falhas += 1
        print(f"   FALHA  apis/pet_bits/{nome}")
        print(
            f"          exige `{PROVA_GERENCIA}` sem manter o quadro\n"
            "          ou a lista de escritas está desatualizada, ou uma "
            "leitura ficou\n          restrita à gerência sem ninguém decidir "
            "isso"
        )

    if not falhas:
        print(
            f"   ok     as {len(ESCRITAS_DE_COLABORADOR)} escritas de "
            "colaborador exigem gerência, e só elas"
        )

    print()
    return falhas


def main() -> int:
    global _IGNORADOS
    _IGNORADOS = _ler_ignorados()
    print("Guarda dos endpoints de equipe\n")

    falhas_1, endpoints = conferencia_1()
    falhas_2 = conferencia_2(endpoints)
    chamadores = sum(1 for c in endpoints if RE_CHAMADA.search(ler(c)))
    falhas_3 = conferencia_3(chamadores)
    falhas_4 = conferencia_4(endpoints)

    total = falhas_1 + falhas_2 + falhas_3 + falhas_4
    if total == 0:
        print(f"{len(endpoints)} endpoint(s) de equipe conferido(s), nenhuma acusação")
        return 0

    print(f"{total} acusação(ões) — nenhum endpoint de equipe deve subir assim")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
