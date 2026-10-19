## Why

O PetBits ainda tem a cara do Radix sem ajuste nenhum: azul padrão, fonte do
sistema, cantos médios e nenhum sinal de que é uma clínica veterinária. Cada
tela do cliente desenhou o próprio cabeçalho (a casa com botões soltos, a
agenda com um link "Meus animais", a loja com outro menu), então quem navega
entre elas vê o topo mudar de forma a cada clique. É hora de dar ao sistema
uma identidade acolhedora e um cabeçalho que não muda de lugar.

## What Changes

- Tema do app: cor principal verde-água (`teal`), cinza quente (`sand`),
  cantos grandes, fonte Nunito; claro ou escuro conforme o sistema
  operacional, como hoje.
- Marca do PetBits (patinha num selo arredondado + nome) num componente só,
  usado nas portas de entrada, na área do cliente e na área da clínica.
- Cabeçalho único da área do cliente, com Meus animais, Agendar, Loja e Meus
  pedidos, a tela atual destacada, e o Sair. Substitui os três cabeçalhos
  diferentes de hoje; os botões Agendar/Loja/Meus pedidos da casa passam para
  ele.
- Área da clínica: o menu vira abas em pílula, com a tela atual destacada,
  num topo com a marca.
- Portas de entrada (boas-vindas, entrar, entrada da equipe, cadastro): fundo
  com um degradê suave, formulário dentro de um cartão, marca no topo.
- Espécie do animal e selos de destaque em coral (`orange`), o segundo tom da
  identidade.

## Capabilities

### New Capabilities

- `identidade-visual`: a aparência comum do sistema — tema, marca e os
  cabeçalhos de navegação das duas áreas.

### Modified Capabilities

Nenhuma. Nenhuma regra de negócio, de acesso ou de sessão muda.

## Fora do escopo

- Mudar o que qualquer tela faz, os dados que mostra ou as requisições que
  dispara: nenhum `on_load`, State ou endpoint é alterado.
- Logotipo desenhado à mão ou ilustrações: a marca usa o ícone `paw-print`
  do Lucide, que o Reflex já traz.
- Seletor manual de tema claro/escuro.
- Responsividade nova além do que o Radix já dá; o cabeçalho só precisa
  quebrar linha sem estourar a largura.

## Impact

- Código: `petbits/petbits.py` (tema e folha de estilo), módulo novo
  `petbits/visual.py`, `petbits/pages/*`, `assets/estilo.css` novo.
- Dependências: nenhuma nova. A fonte vem do Google Fonts por folha de
  estilo, sem pacote.
- Backend (Xano): nenhum impacto.
