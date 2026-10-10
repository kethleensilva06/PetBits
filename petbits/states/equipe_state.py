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

from datetime import date, timedelta
from typing import Optional

import reflex as rx

from petbits import agenda as regras_da_agenda
from petbits import datas, xano
from petbits.states.auth_state import AuthState
from petbits.pedidos import ROTULOS_ACAO, proximas
from petbits.states.loja_state import CATEGORIAS as CATEGORIAS_PRODUTO
from petbits.states.loja_state import ENTREGAS, ORIGENS, PAGAMENTOS, SITUACOES, reais
from petbits.states.sessao import SemSessao
from petbits.xano import NaoEncontrado, SessaoExpirada, XanoError

# A função é o CARGO, não o nível de acesso. "Gerente" aqui quer dizer quem
# administra a clínica no dia a dia; quem administra o SISTEMA é definido pelo
# papel da conta, que é outra coisa e mora na tabela `user`. Confundir os dois
# seria o caminho mais curto para alguém ganhar acesso ao se autointitular.
CATEGORIAS = regras_da_agenda.CATEGORIAS

FUNCOES = ["gerente", "veterinario", "clinico_geral", "tosador", "atendente"]

FUNCAO_LEGIVEL = {
    "gerente": "Gerente",
    "veterinario": "Veterinário",
    "clinico_geral": "Clínico geral",
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
    srv_categoria: str = ""

    # Catálogo da loja (change `loja`).
    produtos: list[dict] = []
    prd_dialogo: bool = False
    prd_editando: Optional[int] = None
    prd_erro: str = ""
    prd_nome: str = ""
    prd_descricao: str = ""
    prd_categoria: str = "racao"
    prd_marca: str = ""
    prd_unidade: str = ""
    prd_preco: str = ""
    prd_estoque: str = ""

    # Pedidos da loja (change `pedidos-da-equipe`).
    pedidos_clinica: list[dict] = []
    filtro_pedidos: str = "todos"

    # Venda no balcão (change `venda-no-balcao`).
    balcao_cliente: str = ""
    balcao_carrinho: dict[str, int] = {}
    balcao_aviso: str = ""
    balcao_erro: str = ""

    # Agenda do dia (change `agendamento`, D8). Só leitura.
    agenda_dia_iso: str = ""
    agenda: list[dict] = []

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

    def set_srv_categoria(self, v: str):
        self.srv_categoria = v

    def set_prd_dialogo(self, v: bool):
        self.prd_dialogo = v

    def set_prd_nome(self, v: str):
        self.prd_nome = v

    def set_prd_descricao(self, v: str):
        self.prd_descricao = v

    def set_prd_categoria(self, v: str):
        self.prd_categoria = v

    def set_prd_marca(self, v: str):
        self.prd_marca = v

    def set_prd_unidade(self, v: str):
        self.prd_unidade = v

    def set_prd_preco(self, v: str):
        self.prd_preco = v

    def set_prd_estoque(self, v: str):
        self.prd_estoque = v

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
    def mostrar_carregando(self) -> bool:
        """Carregando é um estado, não o resto do mundo.

        Sem esta var, "carregando" era o caso padrão de tudo que não fosse
        "tem dado" nem "vazio" — e uma requisição recusada ficava mostrando
        o erro **e** o spinner, para sempre. Visto com um papel forjado no
        armazenamento local: o 403 aparecia certo, e embaixo dele a tela
        prometia que os tutores ainda estavam vindo.

        É a mesma família de defeito que a change anterior corrigiu do outro
        lado, quando "ainda carregando" era mostrado como "não há animais".
        Os três estados precisam ser disjuntos e explícitos.
        """
        return self.carregando or (not self.ja_carregou and not self.erro)

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
        self.agenda = []
        self.agenda_dia_iso = ""
        self.produtos = []
        self.pedidos_clinica = []
        self.filtro_pedidos = "todos"
        self.balcao_cliente = ""
        self.balcao_carrinho = {}
        self.balcao_aviso = ""
        self.balcao_erro = ""
        self.prd_dialogo = False
        self.prd_editando = None
        self.prd_erro = ""
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
                "categoria": CATEGORIAS.get(s.get("categoria") or "", "Sem categoria"),
                "_categoria": s.get("categoria") or "",
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
        self.srv_categoria = ""

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
        self.srv_categoria = registro["_categoria"]
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
        # Só vai quando escolhida: na alteração, não mandar é não mexer.
        if self.srv_categoria:
            dados["categoria"] = self.srv_categoria

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

    # --- catálogo da loja (change `loja`) -----------------------------------

    @rx.var
    def tem_produtos(self) -> bool:
        return len(self.produtos) > 0

    @rx.var
    def titulo_prd(self) -> str:
        return "Editar produto" if self.prd_editando is not None else "Novo produto"

    async def carregar_produtos(self):
        self._comecar()
        self.produtos = []
        try:
            token = await self._token_de_equipe()
            registros = await xano.listar_produtos(token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            return self._falhou(erro)
        self.produtos = [
            {
                "id": p.get("id"),
                "nome": p.get("nome") or "-",
                "descricao": p.get("descricao") or "",
                "categoria": CATEGORIAS_PRODUTO.get(p.get("categoria") or "", "-"),
                "marca": p.get("marca") or "",
                "unidade": p.get("unidade") or "",
                "preco": _dinheiro(p.get("preco")),
                "estoque": f"{int(p.get('estoque') or 0)} em estoque",
                "ativo": bool(p.get("ativo")),
                "_categoria": p.get("categoria") or "racao",
                "_preco": datas.numero_para_campo(p.get("preco")),
                "_estoque": str(int(p.get("estoque") or 0)),
            }
            for p in registros
        ]
        self.carregando = False
        self.ja_carregou = True

    def novo_produto(self):
        self.prd_editando = None
        self.prd_erro = ""
        self.prd_nome = ""
        self.prd_descricao = ""
        self.prd_categoria = "racao"
        self.prd_marca = ""
        self.prd_unidade = ""
        self.prd_preco = ""
        self.prd_estoque = ""
        self.prd_dialogo = True

    def editar_produto(self, registro: dict):
        self.prd_editando = registro["id"]
        self.prd_erro = ""
        self.prd_nome = registro["nome"]
        self.prd_descricao = registro["descricao"]
        self.prd_categoria = registro["_categoria"]
        self.prd_marca = registro["marca"]
        self.prd_unidade = registro["unidade"]
        self.prd_preco = registro["_preco"]
        self.prd_estoque = registro["_estoque"]
        self.prd_dialogo = True

    async def salvar_produto(self):
        if not self.prd_nome.strip():
            self.prd_erro = "Informe o nome do produto."
            return
        try:
            preco = float((self.prd_preco or "").replace(",", "."))
        except ValueError:
            self.prd_erro = "O preço precisa ser um número."
            return
        if preco <= 0:
            self.prd_erro = "O preço tem de ser maior que zero."
            return
        try:
            estoque = int(self.prd_estoque)
        except (TypeError, ValueError):
            self.prd_erro = "Informe o estoque em unidades."
            return
        if estoque < 0:
            self.prd_erro = "O estoque não pode ser negativo."
            return
        dados = {
            "nome": self.prd_nome.strip(),
            "descricao": self.prd_descricao.strip(),
            "categoria": self.prd_categoria,
            "marca": self.prd_marca.strip(),
            "unidade": self.prd_unidade.strip(),
            "preco": preco,
            "estoque": estoque,
        }
        self.salvando = True
        yield
        try:
            token = await self._token_de_equipe()
            if self.prd_editando is None:
                await xano.criar_produto(dados, token=token)
            else:
                await xano.atualizar_produto(self.prd_editando, dados, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            yield await self._encerrar(erro)
            return
        except (NaoEncontrado, XanoError) as erro:
            self.prd_erro = str(erro)
            return
        finally:
            self.salvando = False
        self.prd_dialogo = False
        resultado = await self.carregar_produtos()
        if resultado is not None:
            yield resultado

    async def alternar_ativo(self, registro: dict):
        """Ativar ou desativar manda SÓ `ativo`: o padrão `pick` do backend
        deixa os outros campos como estão."""
        try:
            token = await self._token_de_equipe()
            await xano.atualizar_produto(registro["id"], {"ativo": not registro["ativo"]},
                                         token=token)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except (NaoEncontrado, XanoError) as erro:
            self.erro = str(erro)
            return
        return await self.carregar_produtos()

    # --- pedidos da loja (change `pedidos-da-equipe`) ------------------------

    @rx.var
    def tem_pedidos_clinica(self) -> bool:
        return len(self.pedidos_clinica) > 0

    async def set_filtro_pedidos(self, valor: str):
        self.filtro_pedidos = valor
        return await self.carregar_pedidos_clinica()

    async def carregar_pedidos_clinica(self):
        self._comecar()
        self.pedidos_clinica = []
        filtro = "" if self.filtro_pedidos == "todos" else self.filtro_pedidos
        try:
            token = await self._token_de_equipe()
            dados = await xano.pedidos_da_clinica(filtro, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            return self._falhou(erro)
        itens: dict = {}
        for i in dados.get("itens") or []:
            itens.setdefault(i.get("id_pedido"), []).append({
                "texto": f"{int(i.get('quantidade') or 0)} × {i.get('produto_nome') or '-'}",
                "linha": reais(i.get("valor_linha")),
            })
        self.pedidos_clinica = [
            {
                "id": p.get("id"),
                "quando": regras_da_agenda.data_curta(p.get("created_at")),
                "cliente": " · ".join(filter(None, [p.get("cliente_nome") or "-",
                                                    p.get("cliente_telefone") or ""])),
                "situacao": SITUACOES.get(p.get("situacao") or "", "-"),
                "entrega": ENTREGAS.get(p.get("entrega") or "", "-"),
                "endereco": p.get("endereco_entrega") or "",
                "pagamento": PAGAMENTOS.get(p.get("forma_pagamento") or "", "-"),
                "origem": ORIGENS.get(p.get("origem") or "site", ""),
                "pago": bool(p.get("pago_em")),
                "total": reais(p.get("total")),
                "itens": itens.get(p.get("id"), []),
                "acoes": [{"situacao": s, "rotulo": ROTULOS_ACAO[s]}
                          for s in proximas(p.get("situacao") or "", p.get("entrega") or "")],
            }
            for p in dados.get("pedidos") or []
        ]
        self.carregando = False
        self.ja_carregou = True

    async def avancar_pedido(self, pedido_id: int, situacao: str):
        try:
            token = await self._token_de_equipe()
            await xano.mudar_situacao_do_pedido(pedido_id, situacao, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            return await self._encerrar(erro)
        except (NaoEncontrado, XanoError) as erro:
            self.erro = str(erro)
            return
        return await self.carregar_pedidos_clinica()

    # --- venda no balcão (change `venda-no-balcao`) -------------------------

    def set_balcao_cliente(self, valor: str):
        self.balcao_cliente = valor

    @rx.var
    def produtos_a_venda(self) -> list[dict]:
        return [p for p in self.produtos if p["ativo"] and int(p["_estoque"] or 0) > 0]

    @rx.var
    def itens_balcao(self) -> list[dict]:
        por_id = {str(p["id"]): p for p in self.produtos}
        itens = []
        for pid, qtd in self.balcao_carrinho.items():
            p = por_id.get(pid)
            if p:
                preco = float(p["_preco"] or 0)
                itens.append({"id": pid, "nome": p["nome"], "quantidade": qtd,
                              "linha": reais(preco * qtd),
                              "pode_mais": qtd < int(p["_estoque"] or 0)})
        return itens

    @rx.var
    def total_balcao(self) -> str:
        por_id = {str(p["id"]): p for p in self.produtos}
        return reais(sum(float(por_id[pid]["_preco"] or 0) * q
                         for pid, q in self.balcao_carrinho.items() if pid in por_id))

    async def carregar_balcao(self):
        """Clientes e catálogo: duas requisições, as listas que a área da
        equipe já tem."""
        self.balcao_aviso = ""
        self.balcao_erro = ""
        resultado = await self.carregar_tutores()
        if resultado is not None:
            return resultado
        return await self.carregar_produtos()

    def balcao_adicionar(self, produto_id: int):
        pid = str(produto_id)
        estoque = next((int(p["_estoque"] or 0) for p in self.produtos
                        if str(p["id"]) == pid), 0)
        atual = self.balcao_carrinho.get(pid, 0)
        if atual < estoque:
            self.balcao_carrinho = {**self.balcao_carrinho, pid: atual + 1}
        self.balcao_aviso = ""

    def balcao_tirar(self, produto_id: str):
        atual = self.balcao_carrinho.get(produto_id, 0)
        resto = {k: v for k, v in self.balcao_carrinho.items() if k != produto_id}
        if atual > 1:
            resto[produto_id] = atual - 1
        self.balcao_carrinho = resto

    async def confirmar_venda(self):
        if not self.balcao_cliente:
            self.balcao_erro = "Escolha o cliente."
            return
        if not self.balcao_carrinho:
            self.balcao_erro = "Adicione ao menos um produto."
            return
        self.balcao_erro = ""
        self.salvando = True
        yield
        try:
            token = await self._token_de_equipe()
            itens = [{"produto_id": int(pid), "quantidade": q}
                     for pid, q in self.balcao_carrinho.items()]
            venda = await xano.vender_no_balcao(int(self.balcao_cliente), itens, token=token)
        except (SemSessao, SessaoExpirada) as erro:
            yield await self._encerrar(erro)
            return
        except XanoError as erro:
            self.balcao_erro = str(erro)
            return
        finally:
            self.salvando = False
        cliente = next((t["nome"] for t in self.tutores
                        if str(t["id"]) == self.balcao_cliente), "")
        self.balcao_aviso = (f"Venda nº {venda.get('id')} registrada para {cliente}: "
                             f"{reais(venda.get('total'))}.")
        self.balcao_carrinho = {}
        resultado = await self.carregar_produtos()
        if resultado is not None:
            yield resultado

    # --- agenda do dia (change `agendamento`, D8) ---------------------------

    @rx.var
    def agenda_titulo(self) -> str:
        if not self.agenda_dia_iso:
            return ""
        return regras_da_agenda.data_por_extenso(date.fromisoformat(self.agenda_dia_iso))

    @rx.var
    def tem_agenda(self) -> bool:
        return len(self.agenda) > 0

    async def carregar_agenda(self):
        self._comecar()
        self.agenda = []
        if not self.agenda_dia_iso:
            self.agenda_dia_iso = regras_da_agenda.hoje().isoformat()
        dia = date.fromisoformat(self.agenda_dia_iso)
        try:
            token = await self._token_de_equipe()
            registros = await xano.agenda_da_clinica(
                regras_da_agenda.inicio_do_dia_ms(dia), token=token
            )
        except (SemSessao, SessaoExpirada) as erro:
            self.carregando = False
            return await self._encerrar(erro)
        except XanoError as erro:
            return self._falhou(erro)

        self.agenda = [
            {
                "id": a.get("id"),
                "horario": f"{regras_da_agenda.hora(a.get('inicio'))}–"
                           f"{regras_da_agenda.hora(a.get('fim'))}",
                "animal": " · ".join(filter(None, [a.get("pet_nome") or "-",
                                                   a.get("pet_especie") or ""])),
                "tutor": " · ".join(filter(None, [a.get("tutor_nome") or "-",
                                                  a.get("tutor_telefone") or ""])),
                "servico": a.get("servico_nome") or "-",
                "profissional": a.get("profissional_nome") or "-",
                "situacao": regras_da_agenda.SITUACOES.get(a.get("situacao") or "", "-"),
                "cancelado": a.get("situacao") == "cancelado",
                "observacoes": a.get("observacoes") or "",
            }
            for a in registros
        ]
        self.carregando = False
        self.ja_carregou = True

    async def mudar_dia_da_agenda(self, passo: int):
        dia = date.fromisoformat(self.agenda_dia_iso or regras_da_agenda.hoje().isoformat())
        self.agenda_dia_iso = (dia + timedelta(days=passo)).isoformat()
        return await self.carregar_agenda()

    async def agenda_de_hoje(self):
        self.agenda_dia_iso = regras_da_agenda.hoje().isoformat()
        return await self.carregar_agenda()

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
