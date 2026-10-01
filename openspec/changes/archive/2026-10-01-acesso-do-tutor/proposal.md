# Proposal

## Why

O sistema não tem porta de entrada: hoje a aplicação Reflex é uma página em
branco e o workspace do Xano só tem o template de autenticação que veio de
fábrica, sem nenhum conceito do domínio.

Sem saber **quem** está do outro lado, nenhuma outra funcionalidade do PetBits
pode existir. Sete dos nove conceitos do domínio (`docs/domain-model.md`)
pendem de um Tutor, e toda decisão de autorização é uma subida por essa árvore
até encontrar um. Esta é, portanto, a primeira fatia possível: a que dá ao
sistema a noção de identidade sobre a qual as demais se apoiam.

Ela também é utilizável por si só — uma pessoa cria a própria conta e entra —,
então entrega valor observável em vez de ser uma camada de infraestrutura.

## What Changes

- Uma pessoa **cria a própria conta** pelo site, informando nome, e-mail,
  senha e os dados de tutor (documento de identificação e contato).
- Uma pessoa **entra** com e-mail e senha, e **sai** quando quiser.
- A **sessão sobrevive a recarregar a página** e a reiniciar o servidor de
  desenvolvimento.
- Existe uma **tela pós-login** mínima que cumprimenta a pessoa pelo nome.
  Ela é o destino do login; o conteúdo dela chega nas changes seguintes.
- As rotas privadas ficam **inacessíveis a quem não entrou**, e a barreira é
  verificada no backend, não só escondendo a tela.
- Passa a existir o conceito de **Tutor** como registro do domínio, distinto
  da conta de acesso, com vínculo **opcional** entre os dois: a clínica
  precisa poder cadastrar quem chega no balcão e nunca vai usar o site.
- O cadastro público cria **sempre** um tutor. Nenhum caminho da aplicação
  concede o papel de equipe.

### Fora do escopo

Explicitamente adiado para outras changes: animais, agenda e agendamento,
catálogo de serviços, cadastro de colaboradores, histórico clínico, petshop,
a área administrativa da equipe, recuperação de senha e identidade visual.

Esta change também **não** cria o cadastro de tutor pela clínica (tutor de
balcão). Ela apenas garante que o modelo comporte esse caso, para não ter de
ser desfeito depois.

## Capabilities

### New Capabilities

- `autenticacao`: quem entra no sistema e como a sessão se comporta — criação
  de conta, entrada, saída, persistência da sessão, expiração e o papel do
  usuário. Não cobre o que cada papel pode fazer em cada tela; cobre apenas
  quem a pessoa é.
- `tutores`: o Tutor como registro do domínio — seus dados, a unicidade do
  documento de identificação e o vínculo opcional com uma conta de acesso.

### Modified Capabilities

Nenhuma: o projeto ainda não possui specs consolidadas.

## Impact

**Xano** (`workspace 169225`, API group `PetBits`)

- Tabela nova para o Tutor.
- Endpoint novo de cadastro, que cria a conta e a ficha numa só requisição —
  o `auth/signup` do template cria apenas a conta.
- Endpoint novo para o usuário logado obter a própria ficha.
- Reaproveita sem alterar: `auth/login` e `auth/me` do grupo `Authentication`.

**Aplicação Reflex**

- Módulo cliente da API do Xano (primeiro código a falar HTTP no projeto).
- State de sessão e a guarda das rotas privadas.
- Páginas de entrada e de cadastro, e a tela pós-login.
- Registro de rotas em `petbits/petbits.py`.

**Configuração**

- `.env` já aponta para os dois API groups da conta
  (`XANO_BASE_URL`, `XANO_AUTH_BASE_URL`).
- Provável nova dependência Python para requisições HTTP, a ser registrada em
  `requirements.txt`.

**Restrição a respeitar**: o plano gratuito do Xano aceita 10 requisições a
cada 20 segundos por instância. Entrar no sistema não deve custar mais do que
duas.
