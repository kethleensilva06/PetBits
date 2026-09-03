# PetBits

Frontend em [Reflex](https://reflex.dev) para o sistema de gestão de uma clínica
veterinária / petshop, baseado no banco `Petshop_DQL`.

## Rodando o projeto

```bash
python -m venv .venv
```

Ative o ambiente (Windows PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

Instale as dependências e execute:

```bash
pip install -r requirements.txt
```

```bash
reflex run
```

A aplicação fica disponível em http://localhost:3000.

## Banco de dados

Por padrão a aplicação usa um SQLite local (`petbits.db`), criado automaticamente
na primeira execução. Para apontar para o SQL Server da disciplina, defina a
variável de ambiente `DB_URL` antes de rodar:

```bash
export DB_URL="mssql+pyodbc://usuario:senha@servidor/Petshop_DQL?driver=ODBC+Driver+17+for+SQL+Server"
```

Nesse caso também é preciso instalar o driver: `pip install pyodbc`.

## Estrutura

```
petbits/
├── models.py          # tabelas SQLModel (espelham o schema Petshop_DQL)
├── database.py        # engine, sessão e criação das tabelas
├── petbits.py         # app e registro das rotas
├── components/        # layout, sidebar e componentes de UI reutilizáveis
├── pages/             # uma página por rota
└── states/            # um State por entidade, com a lógica de CRUD
```

## Rotas

| Rota | Página | Entidades |
|------|--------|-----------|
| `/` | Painel com indicadores e próximos agendamentos | todas |
| `/clientes` | Cadastro de tutores | `Cliente` |
| `/pets` | Cadastro de pets | `Pet` → `Cliente` |
| `/agendamentos` | Agenda de serviços | `Agendamento` → `Pet`, `Servico`, `Funcionario` |
| `/prontuarios` | Histórico clínico | `Prontuario` → `Pet`, `Funcionario` |
| `/servicos` | Catálogo de serviços | `Servico` |
| `/produtos` | Catálogo de produtos | `Produto` |
| `/pedidos` | Pedidos e seus itens | `Pedido`, `Itens_Pedido` → `Produto` |
| `/funcionarios` | Equipe | `Funcionario` |

## Arquitetura do frontend

Cada entidade segue o mesmo padrão:

- **State** (`petbits/states/`): guarda a lista exibida, os campos do formulário
  e os métodos `load_*`, `open_new`, `open_edit`, `save` e `delete`. O
  carregamento inicial acontece no `on_load` da rota, declarado em `petbits.py`.
- **Página** (`petbits/pages/`): monta a barra de busca, a tabela e o diálogo de
  formulário, ligando os componentes aos eventos do State.
- **Componentes** (`petbits/components/`): `layout` (sidebar + cabeçalho),
  `sidebar` (navegação) e helpers de UI (`form_field`, `row_actions`,
  `empty_state`, `page_toolbar`).

Telas que mostram dados de mais de uma tabela (pets com o nome do tutor,
agendamentos com pet/serviço/responsável) montam a lista como `list[dict]` já
resolvida no State, evitando consultas no meio da renderização.
