"""Modelos de dados do PetBits, espelhando o schema Petshop_DQL (SQL Server).

Cada classe representa uma tabela do banco de dados. Os tipos e restrições
seguem o script SQL original, adaptados para o ORM SQLModel.
"""

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel

CARGOS_FUNCIONARIO = ["veterinario", "tosador", "atendente"]
STATUS_PEDIDO = ["pendente", "pago", "enviado", "entregue"]
STATUS_AGENDAMENTO = ["agendado", "em_andamento", "concluido", "cancelado"]


class Cliente(SQLModel, table=True):
    """Tutor responsável pelos pets cadastrados."""

    __tablename__ = "cliente"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cpf: str = Field(unique=True, index=True)
    email: Optional[str] = Field(default=None, unique=True)
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    data_cadastro: datetime = Field(default_factory=datetime.now)


class Funcionario(SQLModel, table=True):
    """Colaborador da clínica (veterinário, tosador ou atendente)."""

    __tablename__ = "funcionario"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    cpf: str = Field(unique=True, index=True)
    cargo: str
    telefone: Optional[str] = None
    email: Optional[str] = Field(default=None, unique=True)
    data_contratacao: Optional[date] = None


class Produto(SQLModel, table=True):
    """Item vendável do petshop (ração, brinquedo, medicamento etc.)."""

    __tablename__ = "produto"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    categoria: Optional[str] = None
    marca: Optional[str] = None
    unidade: Optional[str] = None
    preco_venda: float = 0.0


class Servico(SQLModel, table=True):
    """Serviço prestado pela clínica (banho, tosa, consulta etc.)."""

    __tablename__ = "servico"

    id: Optional[int] = Field(default=None, primary_key=True)
    nome_servico: str
    descricao: Optional[str] = None
    preco: float = 0.0
    duracao_estimada: Optional[int] = None


class Pet(SQLModel, table=True):
    """Animal de estimação vinculado a um cliente."""

    __tablename__ = "pet"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="cliente.id")
    nome: str
    especie: str
    raca: Optional[str] = None
    data_nascimento: Optional[date] = None
    peso: Optional[float] = None
    observacoes: Optional[str] = None


class Pedido(SQLModel, table=True):
    """Pedido de compra de produtos feito por um cliente."""

    __tablename__ = "pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_cliente: int = Field(foreign_key="cliente.id")
    data_pedido: datetime = Field(default_factory=datetime.now)
    status: str = "pendente"
    valor_total: float = 0.0


class Agendamento(SQLModel, table=True):
    """Horário marcado para um pet realizar um serviço com um funcionário."""

    __tablename__ = "agendamento"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_pet: int = Field(foreign_key="pet.id")
    id_servico: int = Field(foreign_key="servico.id")
    id_funcionario: int = Field(foreign_key="funcionario.id")
    data_hora: datetime
    status: str = "agendado"
    observacoes: Optional[str] = None


class ItensPedido(SQLModel, table=True):
    """Item (produto + quantidade) que compõe um pedido."""

    __tablename__ = "itens_pedido"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_pedido: int = Field(foreign_key="pedido.id")
    id_produto: int = Field(foreign_key="produto.id")
    quantidade: int = 1
    valor_unitario: float = 0.0
    valor_total: float = 0.0


class Prontuario(SQLModel, table=True):
    """Registro de atendimento clínico de um pet."""

    __tablename__ = "prontuario"

    id: Optional[int] = Field(default=None, primary_key=True)
    id_pet: int = Field(foreign_key="pet.id")
    id_funcionario: int = Field(foreign_key="funcionario.id")
    data_atendimento: datetime = Field(default_factory=datetime.now)
    diagnostico: Optional[str] = None
    tratamento_realizado: Optional[str] = None
    proxima_consulta: Optional[date] = None
