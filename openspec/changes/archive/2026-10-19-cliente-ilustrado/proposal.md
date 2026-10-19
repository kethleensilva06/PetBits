## Why

Depois da `identidade-visual`, a área do cliente tem cor e cabeçalho, mas
ainda é só texto em cartões: o animal da tutora é um nome e um selo, o
produto da loja é uma lista de campos, e uma tela vazia diz "Nenhum
agendamento ainda." e nada mais. Para quem é cliente de uma clínica de
bairro, a tela deveria parecer feita para o animal dela, não uma planilha.

## What Changes

- Ilustrações próprias em SVG, com as cores do PetBits, em
  `assets/ilustracoes/`: cão, gato e "outro animal"; uma por categoria de
  produto (ração, petisco, brinquedo, higiene, acessório, medicamento); a do
  banner; e as das telas vazias.
- **Casa:** banner de boas-vindas com ilustração, a saudação e atalhos para
  Agendar e Loja; cada cartão de animal ganha o avatar da espécie.
- **Loja:** cada produto ganha a imagem da categoria no topo do cartão.
- **Telas vazias ilustradas:** casa sem animal, Meus pedidos sem pedido e
  Meus agendamentos sem agendamento, com ilustração e texto acolhedor.
- Corrige, de passagem, o aviso "`<div>` dentro de `<p>`" que o React dá no
  aviso "Você tem acesso à área da clínica" da casa — está na mesma tela
  mexida aqui.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: ganha os requisitos das ilustrações da área do
  cliente — avatar por espécie, imagem por categoria, banner e telas vazias.

## Fora do escopo

- Foto real do animal enviada pela tutora (upload): o projeto exclui
  anexos de imagem, e isso pediria armazenamento no Xano.
- Imagem própria por produto cadastrada pela equipe.
- Ilustrações na área da clínica.
- Qualquer mudança de regra, endpoint ou número de requisições.

## Impact

- Código: `petbits/ilustracoes.py` novo, `petbits/states/pet_state.py` e
  `petbits/states/loja_state.py` (um campo de imagem calculado no próprio
  State, sem requisição), `petbits/pages/inicio.py`, `loja.py`, `agenda.py`.
- Arquivos: `assets/ilustracoes/*.svg`.
- Testes: `tests/test_ilustracoes.py` para a escolha da imagem.
- Backend (Xano) e dependências: nenhum impacto.
