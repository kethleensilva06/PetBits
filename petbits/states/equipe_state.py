"""A área da clínica: painel, colaboradores, serviços e a visão dos clientes.

Três coisas deste arquivo não são estilo, são decisão:

**1. Nada é carregado antes de o direito de carregar estar estabelecido.**
Todo loader começa por `_token_de_equipe()`, que levanta `SemSessao` antes de
qualquer requisição sair. Sem conta de equipe, nenhuma chamada à área da
clínica chega ao backend — nem para contar linhas.

**2. Esconder é conveniência; quem recusa é o Xano.** Qualquer pessoa edita
`petbits_papel` no armazenamento local e vê o menu da equipe. Aí cada
requisição volta 403, porque o papel é lido do banco a cada chamada. A
interface mente, o backend não.

**3. As listas carregam sob demanda, uma por clique.** O painel traz só
contadores, numa requisição. As quatro listas soltas no carregamento
custariam metade do orçamento da instância (10 requisições a cada 20
segundos, compartilhadas por todo mundo) numa única abertura de tela — e um
F5 derrubaria o painel e a tela dos tutores junto.
"""

from typing import Optional

import reflex as rx

from petbits import datas, xano
from petbits.states.auth_state import AuthState
from petbits.states.sessao import SemSessao
from petbits.xano import NaoEncontrado, SessaoExpirada, XanoError

FUNCOES = ["veterinario", "tosador", "atendente"]

FUNCAO_LEGIVEL = {
    "veterinario": "Veterinário",
    "tosador": "Tosador",
    "atendente": "Atendente",
}


def _funcao_legivel(valor: str) -> str:
    return FUNCAO_LEGIVEL.get(valor or "", valor or "-")


def _dinheiro(valor) -> str:
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "~").replace(".", ",").replace("~", ".")
    except (TypeError, ValueError):
        return "-"


def _duracao(minutos) -> str:
    try:
        total = int(minutos)
    except (TypeError, ValueError):
        return "-"
    if total <= 0:
        return "-"
    horas, resto = divmod(total, 60)
    if horas and resto:
        return f"{horas}h{resto:02d}"
    if horas:
        return f"{horas}h"
    return f"{resto} min"


class EquipeState(rx.State):
    # --- painel ---
    total_colaboradores: int = 0
    total_servicos: int = 0
    total_tutores: int = 0
    total_animais: int = 0
    painel_carregado: bool = False

    # --- listas ---
    colaboradores: list[dict] = []
    servicos: list[dict] = []
    tutores: list[dict] = []
    animais: list[dict] = []

    # --- estado de carga, por tela ---
    carregando: bool = False
    erro: str = ""
    ja_carregou: bool = False

    # --- formulário de colaborador ---
    col_dialogo: bool = False
    col_editando: Optional[int] = None
    col_erro: str = ""
    col_nome: str = ""
    col_funcao: str = "veterinario"
    col_telefone: str = ""
    col_email: str = ""
    col_entrada: str = ""

    # --- formulário de serviço ---
    srv_dialogo: bool = False
    srv_editando: Optional[int] = None
    srv_erro: str = ""
    srv_nome: str = ""
    srv_descricao: str = ""
    srv_preco: str = ""
    srv_duracao: str = ""

    salvando: bool = False

    # Reflex 0.9 não gera mais setters automáticos.
    def set_col_dialogo(self, v: bool):
        self.col_dialogo = v

    def set_col_nome(self, v: str):
        self.col_nome = v

    def set_col_funcao(self, v: str):
        self.col_funcao = v

    def set_col_telefone(self, v: str):
        self.col_telefone = v

    def set_col_email(self, v: str):
        self.col_email = v

    def set_col_entrada(self, v: str):
        self.col_entrada = v

    def set_srv_dialogo(self, v: bool):
        self.srv_dialogo = v

    def set_srv_nome(self, v: str):
        self.srv_nome = v

    def set_srv_descricao(self, v: str):
        self.srv_descricao = v

    def set_srv_preco(self, v: str):
        self.srv_preco = v

    def set_srv_duracao(self, v: str):
        self.srv_duracao = v

    # --- vars de tela ---

    @rx.var
    def tem_colaboradores(self) -> bool:
        return len(self.colaboradores) > 0

    @rx.var
    def tem_servicos(self) -> bool:
        return len(self.servicos) > 0

    @rx.var
    def tem_tutores(self) -> bool:
        return len(self.tutores) > 0

    @rx.var
    def tem_animais(self) -> bool:
        return len(self.animais) > 0

    @rx.var
    def mostrar_vazio(self) -> bool:
        """"Vazio" só quer dizer vazio depois de carregar sem erro.

        Sem esta distinção, a tela diz "nenhum resultado" enquanto a lista
        ainda está vindo — e também quando a requisição falhou.
        """
        return self.ja_carregou and not self.carregando and not self.erro

    @rx.var
    def titulo_col(self) -> str:
        return "Editar colaborador" if self.col_editando is not None else "Novo colaborador"

    @rx.var
    def titulo_srv(self) -> str:
        return "Editar serviço" if self.srv_editando is not None else "Novo serviço"

    def limpar_dados(self):
        """Apaga tudo o que pertence a uma pessoa. Chamado pelo `sair`.

        A lista de tutores tem documento, telefone e endereço de clientes.
        Deixar isso na memória do navegador depois que alguém sai é o mesmo
        defeito que, na change anterior, fez a lista de animais de uma pessoa
        aparecer para a seguinte — com observações clínicas.
        """
        self.total_colaboradores = 0
        self.total_servicos = 0
        self.total_tutores = 0
        self.total_animais = 0
        self.painel_carregado = False
        self.colaboradores = []
        self.servicos = []
        self.tutores = []
        self.animais = []
        self.carregando = False
        self.erro = ""
        self.ja_carregou = False
        self.col_dialogo = False
        self.col_editando = None
        self.col_erro = ""
        self.srv_dialogo = False
        self.srv_editando = None
        self.srv_erro = ""
        self.salvando = False
        self._limpar_form_col()
        self._limpar_form_srv()

    # --- sessão -----------------------------------------------------------

    async def _token_de_equipe(self) -> str:
        """Token de quem está logado, **se** for conta de equipe.

        Os dois destinos dizem coisas diferentes: sem sessão vai para a
        entrada; com sessão de tutor volta para a área dele. Nos dois casos o
        `raise` acontece **antes** de qualquer requisição — é isso que faz
        "nenhuma requisição de dados daquela tela chega ao backend" ser
        verdade, e não só a tela ficar escondida.
        """
        auth = await self.get_state(AuthState)
        if not auth.token:
            raise SemSessao("/entrar")
        if not xano.eh_equipe(auth.usuario_papel):
            raise SemSessao("/")
        return auth.token

    async def _encerrar(self, erro: Exception):
        if isinstance(erro, SessaoExpirada):
            auth = await self.get_state(AuthState)
            auth._limpar(expirou=True)
        return rx.redirect(getattr(erro, "destino", "/entrar"))

    def _comecar(self):
        self.erro = ""
        self.carregando = True

    def _falhou(self, erro: Exception):
        self.erro = str(erro)
        self.carregando = False
        self.ja_carregou = True

    # --- painel -----------------------------------------------------------

    async def carregar_painel(self):
        self._comecar()
        try:
            token = await self._token_de_equipe()
            dados = await xano.painel_equipe(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            return self._falhou(erro)

        self.total_colaboradores = int(dados.get("colaboradores") or 0)
        self.total_servicos = int(dados.get("servicos") or 0)
        self.total_tutores = int(dados.get("tutores") or 0)
        self.total_animais = int(dados.get("animais") or 0)
        self.painel_carregado = True
        self.carregando = False
        self.ja_carregou = True
        self.erro = ""

    # --- colaboradores ----------------------------------------------------

    async def carregar_colaboradores(self):
        self._comecar()
        self.colaboradores = []
        try:
            token = await self._token_de_equipe()
            registros = await xano.listar_colaboradores(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            return self._falhou(erro)

        self.colaboradores = [
            {
                "id": c.get("id"),
                "nome": c.get("nome") or "-",
                "funcao": _funcao_legivel(c.get("funcao")),
                "telefone": c.get("telefone") or "-",
                "email": c.get("email") or "-",
                "entrada": datas.para_exibir(c.get("data_entrada")),
                "ativo": bool(c.get("ativo")),
                # Crus, para o formulário de edição não precisar de outra
                # requisição: a tela já tem o registro em mãos.
                "_funcao": c.get("funcao") or "veterinario",
                "_telefone": c.get("telefone") or "",
                "_email": c.get("email") or "",
                "_entrada": datas.para_campo(c.get("data_entrada")),
            }
            for c in registros
        ]
        self.carregando = False
        self.ja_carregou = True

    def _limpar_form_col(self):
        self.col_nome = ""
        self.col_funcao = "veterinario"
        self.col_telefone = ""
        self.col_email = ""
        self.col_entrada = ""

    def novo_colaborador(self):
        self.col_editando = None
        self.col_erro = ""
        self._limpar_form_col()
        self.col_dialogo = True

    def editar_colaborador(self, registro: dict):
        self.col_editando = registro["id"]
        self.col_erro = ""
        self.col_nome = registro["nome"]
        self.col_funcao = registro["_funcao"]
        self.col_telefone = registro["_telefone"]
        self.col_email = registro["_email"]
        self.col_entrada = registro["_entrada"]
        self.col_dialogo = True

    def fechar_colaborador(self):
        self.col_dialogo = False
        self.col_erro = ""

    async def salvar_colaborador(self):
        # As mesmas recusas existem no backend, e é lá que elas valem. Aqui
        # servem para a mensagem sair em português e sem gastar requisição.
        if not self.col_nome.strip():
            self.col_erro = "Informe o nome do colaborador."
            return
        if self.col_funcao not in FUNCOES:
            self.col_erro = "Escolha uma função."
            return

        dados = {
            "nome": self.col_nome.strip(),
            "funcao": self.col_funcao,
            "telefone": self.col_telefone.strip(),
            "email": self.col_email.strip(),
        }
        if self.col_entrada.strip():
            dados["data_entrada"] = self.col_entrada.strip()

        self.salvando = True
        yield

        try:
            token = await self._token_de_equipe()
            if self.col_editando is None:
                await xano.criar_colaborador(dados, token=token)
            else:
                await xano.atualizar_colaborador(self.col_editando, dados, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.salvando = False
            yield await self._encerrar(erro)
            return
        except (NaoEncontrado, XanoError) as erro:
            self.salvando = False
            self.col_erro = str(erro)
            return

        self.salvando = False
        self.col_dialogo = False
        self.col_erro = ""
        resultado = await self.carregar_colaboradores()
        if resultado is not None:
            yield resultado

    # --- serviços ---------------------------------------------------------

    async def carregar_servicos(self):
        self._comecar()
        self.servicos = []
        try:
            token = await self._token_de_equipe()
            registros = await xano.listar_servicos(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            return self._falhou(erro)

        self.servicos = [
            {
                "id": s.get("id"),
                "nome": s.get("nome") or "-",
                "descricao": s.get("descricao") or "",
                "preco": _dinheiro(s.get("preco")),
                "duracao": _duracao(s.get("duracao_minutos")),
                "_preco": datas.numero_para_campo(s.get("preco")) or "0",
                "_duracao": str(s.get("duracao_minutos") or ""),
            }
            for s in registros
        ]
        self.carregando = False
        self.ja_carregou = True

    def _limpar_form_srv(self):
        self.srv_nome = ""
        self.srv_descricao = ""
        self.srv_preco = ""
        self.srv_duracao = ""

    def novo_servico(self):
        self.srv_editando = None
        self.srv_erro = ""
        self._limpar_form_srv()
        self.srv_dialogo = True

    def editar_servico(self, registro: dict):
        self.srv_editando = registro["id"]
        self.srv_erro = ""
        self.srv_nome = registro["nome"]
        self.srv_descricao = registro["descricao"]
        self.srv_preco = registro["_preco"]
        self.srv_duracao = registro["_duracao"]
        self.srv_dialogo = True

    def fechar_servico(self):
        self.srv_dialogo = False
        self.srv_erro = ""

    async def salvar_servico(self):
        if not self.srv_nome.strip():
            self.srv_erro = "Informe o nome do serviço."
            return
        try:
            preco = float((self.srv_preco or "0").replace(",", "."))
        except ValueError:
            self.srv_erro = "O preço precisa ser um número."
            return
        if preco < 0:
            self.srv_erro = "O preço não pode ser negativo."
            return
        try:
            duracao = int(self.srv_duracao)
        except (TypeError, ValueError):
            self.srv_erro = "Informe a duração em minutos."
            return
        # Zero é um valor *informado*, não um campo omitido: ele atravessa a
        # alteração e chegaria na gravação. É por isso que a recusa existe nos
        # dois lados, e não só na criação.
        if duracao <= 0:
            self.srv_erro = "A duração precisa ser maior que zero."
            return

        dados = {
            "nome": self.srv_nome.strip(),
            "descricao": self.srv_descricao.strip(),
            "preco": preco,
            "duracao_minutos": duracao,
        }

        self.salvando = True
        yield

        try:
            token = await self._token_de_equipe()
            if self.srv_editando is None:
                await xano.criar_servico(dados, token=token)
            else:
                await xano.atualizar_servico(self.srv_editando, dados, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.salvando = False
            yield await self._encerrar(erro)
            return
        except (NaoEncontrado, XanoError) as erro:
            self.salvando = False
            self.srv_erro = str(erro)
            return

        self.salvando = False
        self.srv_dialogo = False
        self.srv_erro = ""
        resultado = await self.carregar_servicos()
        if resultado is not None:
            yield resultado

    # --- a visão da clínica -----------------------------------------------
    #
    # Só leitura, e a ausência de botões de criar e alterar é o que comunica
    # isso: a escrita de tutor e de animal pela equipe não foi desenhada.

    async def carregar_tutores(self):
        self._comecar()
        self.tutores = []
        try:
            token = await self._token_de_equipe()
            registros = await xano.listar_tutores_da_clinica(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            return self._falhou(erro)

        self.tutores = [
            {
                "id": t.get("id"),
                "nome": t.get("nome") or "-",
                "documento": t.get("documento") or "-",
                "telefone": t.get("telefone") or "-",
                "email": t.get("email") or "-",
                "endereco": t.get("endereco") or "-",
            }
            for t in registros
        ]
        self.carregando = False
        self.ja_carregou = True

    async def carregar_animais(self):
        self._comecar()
        self.animais = []
        try:
            token = await self._token_de_equipe()
            registros = await xano.listar_animais_da_clinica(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            return self._falhou(erro)

        self.animais = [
            {
                "id": a.get("id"),
                "nome": a.get("nome") or "-",
                "especie": a.get("especie") or "-",
                "raca": a.get("raca") or "-",
                "nascimento": datas.para_exibir(a.get("data_nascimento")),
                "peso": datas.numero_para_campo(a.get("peso")) or "-",
                # O animal sem tutor válido aparece aqui de propósito: para o
                # tutor ele é invisível por construção, mas esconder da
                # clínica um registro quebrado é pior do que mostrá-lo.
                "tutor": a.get("tutor_nome") or "— sem tutor —",
                "sem_tutor": not a.get("tutor_nome"),
            }
            for a in registros
        ]
        self.carregando = False
        self.ja_carregou = True
