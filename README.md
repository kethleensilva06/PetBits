# PetBits

Sistema de gestão para uma clínica veterinária que também opera como petshop.
Frontend em [Reflex](https://reflex.dev), persistência no
[Xano](https://xano.com).

O projeto é desenvolvido com apoio de agentes de IA, seguindo o fluxo do
[OpenSpec](https://github.com/fission-ai/openspec): nenhuma funcionalidade
entra sem uma change correspondente.

## Documentação

| Documento | Responde |
|---|---|
| [`docs/project-overview.md`](docs/project-overview.md) | O que é o projeto |
| [`docs/domain-model.md`](docs/domain-model.md) | Quais são os conceitos e como se relacionam |
| [`AGENTS.md`](AGENTS.md) | Como o agente deve trabalhar no projeto |
| [`openspec/config.yaml`](openspec/config.yaml) | Contexto e regras válidos em toda change |
| `openspec/specs/` | Comportamento consolidado do sistema |
| `openspec/changes/` | O que está sendo planejado ou implementado |

## Ambiente

Python 3.10+, `venv` + `pip` (não usar `uv`).

```bash
python -m venv .venv
```

Ative o ambiente (Windows PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e preencha os dois base URLs do Xano.

Execute:

```bash
reflex run
```

A aplicação fica em http://localhost:3000.

> **Windows:** se o `reflex run` abortar com `UnicodeEncodeError: 'charmap'`,
> o console está em cp1252. Rode com `$env:PYTHONUTF8=1; reflex run`.

## Primeiro acesso

A primeira tela é a página inicial (`/boas-vindas`), com três caminhos:
**Sou cliente** (`/entrar`), **Sou da equipe** (`/entrar/equipe`) e
**Criar conta** (`/cadastro`).

1. Clique em **Criar conta** e preencha nome, e-mail, documento e senha.
   A senha precisa de pelo menos 8 caracteres, com uma letra e um número.
2. Ao concluir, você já entra autenticado e cai na sua área.
3. Para voltar depois, use **Sou cliente → Entrar** com o mesmo e-mail e senha.

Funcionários entram por **Sou da equipe**. A gerência só abre para contas com
`role = admin` no Xano; qualquer outra conta, mesmo por essa entrada, vai para
a área de cliente.

Na tela inicial ficam os seus animais. Use **Cadastrar animal** para o
primeiro, e **Editar** para alterar qualquer um deles. Você vê apenas os seus:
quem decide isso é o backend, a partir de quem está autenticado.

A conta criada pelo site é sempre de **tutor** — é isso que permite o
cadastro ser público. O acesso da equipe da clínica chega numa change
própria.

A sessão sobrevive a recarregar a página, a abrir outra aba e a reiniciar o
`reflex run`. Sair limpa tudo.

## Contas de teste (Alt+1 e Alt+2)

Em desenvolvimento (`reflex run`), na tela de entrada, **Alt+1** abre no
canto inferior esquerdo a lista das contas de teste da **equipe**, e
**Alt+2** a dos **clientes**. Clicar numa conta preenche e-mail e senha; é só
clicar em **Entrar**. Com uma lista aberta, o atalho da outra troca de lista;
**Esc** fecha.

É cliente o bloco cujo rótulo começa com `TUTOR` ou `CLIENTE`; o resto é
equipe. Só aparecem contas com a senha preenchida.

As contas vêm de `contas-de-teste.local.txt`, na raiz do projeto. Ele é
ignorado pelo git — cada pessoa cria o seu. Cada bloco começa com uma linha em
maiúscula, que vira o rótulo na lista:

```text
EQUIPE — Nome da pessoa
  email: pessoa@exemplo.com
  senha: ...

TUTOR — conta criada pelo cadastro
  email: tutor@exemplo.com
  senha: ...
```

O mesmo arquivo alimenta `scripts/teste_duas_contas.py`, que usa o último
bloco `TUTOR` e o último `EQUIPE`.

Em produção (`reflex run --env prod`) o atalho não existe. **Não publique o
app em modo de desenvolvimento** com esse arquivo presente: quem abrisse a
tela de entrada veria as contas.

### Criar clientes de teste

Para ter clientes no **Alt+2** sem criá-los um por um pela tela:

```bash
python scripts/criar_clientes_de_teste.py 5
```

O script cria os clientes pelo cadastro público — **na base de verdade** —,
com dados fictícios (e-mail `cliente.teste.<data>.<n>@exemplo.com`, CPF
fictício, senha gerada), e acrescenta cada um a `contas-de-teste.local.txt`.
A senha não aparece na saída; ela vai só para o arquivo.

### Criar produtos de exemplo

Para a loja ter o que vender:

```bash
python scripts/criar_produtos_de_exemplo.py
```

Entra com a primeira conta de equipe com senha do `contas-de-teste.local.txt`
e cadastra 15 produtos, nas seis categorias, pelo mesmo cadastro da tela de
Produtos. Rodar de novo não duplica: produto com o mesmo nome é pulado.

## Ciclo de desenvolvimento

```text
Explore → Propose → Review → Apply → Archive → próxima change
```

Toda modificação do projeto passa por uma change e termina registrada em
`openspec/changes/archive/`. O que já foi entregue está consolidado em
`openspec/specs/`.
