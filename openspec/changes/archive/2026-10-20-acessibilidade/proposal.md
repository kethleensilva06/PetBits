## Why

Uma auditoria nas telas do cliente (Meus animais, Agendar, Loja, Meus pedidos,
Meu perfil), medida no navegador pelas regras do WCAG 2.1 AA, achou:

- texto branco sobre o verde-água dos botões principais com contraste 3,07
  (o mínimo é 4,5);
- o texto cinza secundário (`gray` 9 e 10) com contraste 3,34 e 3,87, em
  quase toda tela: raça, peso, datas, avisos de formulário;
- o texto da aba atual (`teal` 11 sobre `teal` 4) com 3,82;
- os campos de formulário sem nome para o leitor de tela: o rótulo é um texto
  solto acima do campo;
- o avatar do topo sem texto alternativo;
- a página declarada em inglês (`lang="en"`), e o leitor de tela lê o
  português com pronúncia inglesa.

## What Changes

- Os tons do verde-água sólido (9 e 10) e do laranja sólido ficam mais
  escuros, para o branco por cima passar de 4,5.
- O texto secundário passa a usar o `gray` 11 (6,04 sobre branco), e o texto
  da aba atual o `teal` 12.
- Um único `campo(rotulo, componente)` em `petbits/visual.py` substitui os
  cinco iguais das páginas e dá ao campo o nome do rótulo (`aria-label`).
- O avatar ganha texto alternativo; a página passa a `lang="pt-BR"`.
- Um contorno de foco visível em tudo que recebe foco pelo teclado.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: as telas atendem ao contraste e aos nomes acessíveis do WCAG 2.1 AA.

## Fora do escopo

- Auditoria com leitor de tela real (NVDA, VoiceOver).
- Mudar o desenho das telas.

## Impact

- Código: `assets/estilo.css`, `petbits/visual.py`, `petbits/petbits.py`,
  as páginas em `petbits/pages/`; `tests/test_acessibilidade.py`.
