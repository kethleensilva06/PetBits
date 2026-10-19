## Context

Hoje o `rx.App()` é criado sem tema: vale o padrão do Radix (azul, cinza
neutro, cantos médios, aparência do sistema). Cada página da área do cliente
monta o próprio topo — `inicio.py`, `agenda.py` e `loja.py` (`_topo`) — e a
área da clínica tem o seu em `equipe.py` (`_casca` e `_navegacao`). As
portas de entrada (`entrar.py`) centralizam o formulário numa página vazia.

## Goals / Non-Goals

**Goals:**

- Uma identidade acolhedora aplicada em todas as telas pelo tema, não tela a
  tela.
- Um cabeçalho só por área, num módulo só.

**Non-Goals:**

- Mudar comportamento, State, `on_load` ou endpoint.
- Seletor de tema.

## Decisions

### D1. O tema vai no `rx.theme` do app

`rx.App(theme=rx.theme(appearance="inherit", accent_color="teal",
gray_color="sand", radius="large"))`. Toda cor que hoje vem de
`rx.color("accent", …)` e `rx.color("gray", …)` muda junto, sem tocar nas
telas. `appearance="inherit"` mantém o claro/escuro do sistema, como pedido.

### D2. Fonte e fundo por folha de estilo em `assets/`

A Nunito vem do Google Fonts em `stylesheets` do `rx.App`, e
`assets/estilo.css` liga a fonte às variáveis do Radix
(`--default-font-family`, `--heading-font-family`) e desenha o fundo com
variáveis do próprio tema (`--accent-a3`, `--orange-a2`, `--color-background`),
para o degradê acompanhar o modo escuro. CSS não é tecnologia de frontend
nova: o Reflex aceita folhas de estilo como mecanismo próprio.

Alternativa descartada: `style=` global no `rx.App`. Ele não alcança o
`body` nem as variáveis do Radix.

### D3. `petbits/visual.py` reúne a marca e os cabeçalhos

- `marca(href, tamanho)`: selo arredondado com `paw-print` + nome.
- `topo_do_cliente(atual)`: o cabeçalho único do cliente, com
  `AuthState.papel_exibido` e `AuthState.sair` — vars e eventos que já
  existem, sem requisição nova.
- `pilula(rotulo, icone, href, ativo)`: o item de menu em pílula, usado no
  cliente e na clínica.

`equipe.py` continua dono de `AREAS` e da `_casca`, mas passa a desenhar o
menu com `pilula` e o topo com `marca`.

### D4. O que sai da casa

Os botões Agendar, Loja e Meus pedidos da casa duplicariam o cabeçalho; saem.
"Novo animal" fica, porque é ação da tela, não navegação.

### D5. Coral só como destaque

`orange` entra em selos (espécie do animal, "Clínica" no topo da equipe), nunca
como cor de ação, para não competir com o verde-água dos botões.

## Risks / Trade-offs

- [O Google Fonts fora do ar] → a pilha de fontes cai para `system-ui`; nada
  quebra.
- [Teste que procura texto do cabeçalho antigo] → os testes em `tests/` são de
  State e de backend, não de layout; conferir rodando a suíte.

## Verificação

- `pytest` passa sem mudança nos testes.
- No navegador, em claro e escuro: boas-vindas, entrar, cadastro, casa, agenda,
  loja, pedidos e três telas da clínica; navegar pelo cabeçalho e conferir o
  destaque.
- `openspec validate identidade-visual --strict`.
