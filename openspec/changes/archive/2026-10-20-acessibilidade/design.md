## Decisions

### D1. Escurecer o sólido, não trocar a cor

`--teal-9` vai de `#12a594` para `#0b7d70` (5,02 com branco) e `--teal-10`,
o tom do passar o mouse, para `#0a7366`. `--orange-9`/`10` vão para `#c24400`
e `#b03d00` (5,1). Sobrescritos em `.radix-themes`, no próprio elemento onde
o Radix liga `--accent-*` a `--teal-*`, então valem também para o `accent`
e para a versão P3 das cores. A marca continua verde-água.

### D2. Texto secundário no `gray` 11

O Radix reserva o 11 para texto de baixo contraste e o 9/10 para fundos
sólidos. O projeto usava 9 e 10 em texto. Todos passam a 11; ícones ficam
mais escuros também, sem prejuízo.

### D3. Um `campo` só, com nome acessível

Os cinco `_campo` iguais (entrar, equipe, histórico, casa, perfil) viram
`visual.campo`. Ele procura dentro do componente o primeiro campo de texto,
área de texto, gatilho de lista ou controle segmentado e põe nele
`aria-label` com o rótulo, se não houver um. O rótulo visível continua igual.

### D4. Foco visível

`:focus-visible` ganha contorno de 2 px em `teal` 11, com afastamento de
2 px. Só aparece na navegação pelo teclado, não no clique.

### D5. Medido, não suposto

A auditoria roda no navegador: para cada texto visível, a razão de contraste
entre a cor e o primeiro fundo opaco; os elementos interativos sem nome; as
imagens sem `alt`. O mesmo roteiro é rodado de novo depois das correções.

### D6. Achados ao medir de novo

- Campo com `on_change` vira `DebounceInput` no Reflex, que embrulha o campo
  em vez de tê-lo como filho. `campo` passou a reconhecer o `DebounceInput`,
  que repassa o `aria-label` ao campo de dentro.
- A busca da loja não tem rótulo visível: ganhou só o `aria-label`. As
  observações da agenda e o campo de senha (com o olho) passaram a usar
  `campo`.
- O `alt` do avatar vai como atributo (`custom_attrs`); como argumento
  comum, o Reflex o tratava como estilo.

Resultado da segunda auditoria: nenhum texto abaixo do contraste mínimo,
nenhum campo ou botão sem nome e nenhuma imagem sem `alt` nas cinco abas do
cliente, nos diálogos de novo animal e de detalhe do produto, na página
inicial, nas entradas, no cadastro e nas dez telas da clínica. O foco pelo
teclado mostra contorno de 2 px.
