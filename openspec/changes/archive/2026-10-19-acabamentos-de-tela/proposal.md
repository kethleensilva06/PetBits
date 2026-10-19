## Why

As telas cresceram rápido hoje e ficaram arestas que todo mundo vê:

- o Xano devolve as recusas sem acento ("A senha atual nao confere.", "CPF
  invalido."), e a tela as mostra assim, ao lado de textos bem escritos;
- no celular, as 9 abas da clínica quebram em 3 linhas e o "Sair" desce para
  uma segunda linha do topo;
- a loja não tem busca nem filtro, o carrinho só aparece dentro da loja, e
  para levar 3 unidades é preciso clicar 3 vezes;
- CPF e telefone aparecem crus (`12345678901`, `11988887777`) e são digitados
  sem ajuda;
- "Dados atualizados." e "Senha alterada." ficam parados na tela até recarregar;
- a verificação de ponta a ponta deixa um "Produto de verificação" **ativo**
  na loja do cliente quando para no meio — foi o que apareceu hoje.

## What Changes

- **Mensagens com acento:** o cliente HTTP (`petbits/xano.py`) acentua as
  recusas conhecidas do backend antes de chegarem à tela
  (`petbits/mensagens.py`). Os endpoints não mudam.
- **Avisos passageiros:** as confirmações do perfil (dados, senha, foto) viram
  notificação que some sozinha.
- **Menu da clínica no celular:** abaixo da largura média, as abas dão lugar a
  um botão de menu com as 9 áreas; o topo esconde o que não cabe.
- **Loja:** busca por nome, filtro por categoria, ícone de carrinho com a
  quantidade no cabeçalho do cliente, e escolha da quantidade no detalhe do
  produto. Nada disso faz requisição: tudo sai da lista que a loja já tem.
- **Máscaras:** CPF (`000.000.000-00`) e telefone (`(00) 00000-0000`) são
  formatados enquanto se digita, nos cadastros e nos perfis
  (`petbits/mascaras.py`).
- **Verificação de ponta a ponta:** o produto de verificação é desativado
  sempre, mesmo quando a rodada para no meio.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `identidade-visual`: mensagens em português correto; menu da clínica no
  celular; avisos passageiros.
- `produtos`: busca, filtro, quantidade no detalhe e carrinho no cabeçalho.
- `verificacao`: a ponta a ponta não deixa produto de teste à venda.

## Fora do escopo

- Esqueletos de carregamento, linha do tempo do pedido e fotos na página de
  boas-vindas: ficam para outra change.
- Acentuar as mensagens no próprio Xano.
- Máscara em outros campos (preço, data).

## Impact

- Código: `petbits/mensagens.py` e `petbits/mascaras.py` novos;
  `petbits/xano.py`, `petbits/visual.py`, `petbits/pages/equipe.py`,
  `petbits/pages/loja.py`, `petbits/states/loja_state.py`,
  `auth_state.py`, `equipe_state.py`, `perfil_state.py`;
  `scripts/verificar_ponta_a_ponta.py`.
- Testes: `tests/test_mensagens.py`, `tests/test_mascaras.py`, filtro da loja.
- Backend e dependências: nenhum impacto.
