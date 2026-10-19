## Context

A `identidade-visual` deu tema, marca e cabeçalho. A espécie do animal é texto
livre (`PetState.f_especie`, sem lista), e a categoria do produto é uma das
seis chaves de `rotulos.CATEGORIAS_PRODUTO`, mas `LojaState` guarda só o
rótulo legível. As telas vazias são uma linha de texto (pedidos, agenda) ou
um cartão sem imagem (casa).

## Goals / Non-Goals

**Goals:** a área do cliente com imagem onde hoje só há texto, sem custo de
requisição e funcionando no claro e no escuro.

**Non-Goals:** upload de foto, imagem por produto, área da clínica.

## Decisions

### D1. SVG próprio, em `assets/ilustracoes/`

Ilustrações desenhadas à mão em SVG, no estilo plano, com teal, coral e
areia. Cada uma tem o próprio fundo arredondado, então não depende da cor da
página e funciona nos dois modos. Sem banco de imagens: não há licença a
conferir nem download, e o arquivo é pequeno.

### D2. A escolha da imagem é função pura em `petbits/ilustracoes.py`

`imagem_da_especie(texto)` normaliza (minúsculas, sem acento, sem espaço nas
pontas) e casa por lista de palavras; `imagem_da_categoria(chave)` usa a
chave crua. Os States chamam essas funções ao montar cada item, junto com
os outros campos de tela — é onde o resto da formatação já mora, e permite
testar sem Reflex. A loja passa a guardar a chave crua só para isso.

### D3. Banner substitui o título da casa

A saudação e o subtítulo saem do `titulo_de_pagina` e vão para dentro do
banner, que tem a ilustração à direita (escondida no celular para não
empurrar o conteúdo) e os atalhos Agendar e Loja. "Novo animal" fica fora do
banner, ao lado do título da lista "Seus animais".

### D4. Tela vazia é um componente só

`tela_vazia(imagem, titulo, texto, acao)` em `petbits/visual.py`, usado nas
três telas. As condições de "mostrar vazio" já existem e não mudam
(`PetState.mostrar_vazio`, e a cadeia `carregando`/lista nas outras duas).

### D5. O aviso de `<div>` dentro de `<p>`

`rx.callout("texto")` põe os filhos dentro de um `<p>`; passar um `hstack`
gera `<div>` dentro de `<p>`. Trocar por texto e link soltos (`<a>` pode
estar dentro de `<p>`).

## Risks / Trade-offs

- [Espécie escrita de um jeito não previsto, como "dog"] → cai na genérica;
  sem erro. A lista de palavras pode crescer depois.

## Verificação

- `tests/test_ilustracoes.py`: espécies e categorias, incluindo acento,
  maiúscula, vazio e desconhecido; a suíte toda passa.
- No navegador, como tutora: banner e avatares na casa; imagens na loja; as
  três telas vazias (pedidos e agendamentos com uma conta de teste sem
  histórico, ou criada por `scripts/criar_clientes_de_teste.py`); claro,
  escuro e celular; sem erro novo no console; nenhuma requisição externa
  além da fonte.
- `openspec validate cliente-ilustrado --strict`.
