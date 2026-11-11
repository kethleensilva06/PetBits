## Why

Toda tela pede tudo de novo ao Xano cada vez que abre, mesmo quando nada
mudou. A casa do cliente e a Agenda buscam os mesmos animais e os mesmos
agendamentos; colaboradores e serviços quase nunca mudam e são buscados a cada
clique no menu. Isso deixa as telas mais lentas e gasta o limite do Xano (10
requisições a cada 20 segundos por instância). A usuária pediu para guardar o
que só muda quando a própria pessoa muda.

## What Changes

- As leituras ao Xano que mudam pouco ficam guardadas por um tempo, na memória
  do servidor do site, separadas por credencial: o dado de uma pessoa nunca é
  servido a outra, e nada pessoal é gravado no navegador nem em cookie.
- Tempos: animais, serviços, colaboradores e o catálogo de serviços, 10 min;
  ficha e perfil, 30 min; produtos, tutores e animais da clínica, 5 min; loja,
  2 min; agendamentos, 90 s; pedidos do cliente, 60 s.
- Continuam sempre atualizados: painel, agenda e pedidos da clínica, ocupação
  do dia, históricos e a confirmação da sessão.
- Toda gravação feita pela pessoa apaga na hora o que estava guardado daquele
  assunto: ela vê o próprio cadastro ou alteração imediatamente.
- Sair, ou a sessão vencer, apaga tudo o que estava guardado daquela
  credencial.
- Um botão **Atualizar** no topo das duas áreas apaga o guardado e recarrega a
  tela, para quem quer ver na hora o que outra pessoa mudou.

## Capabilities

### New Capabilities

- `desempenho`: leituras guardadas por tempo, separadas por credencial, e o
  botão Atualizar.

### Modified Capabilities

Nenhuma.

## Impact

- Código: `petbits/guardados.py` (novo), `petbits/xano.py`,
  `petbits/states/auth_state.py`, `petbits/visual.py`,
  `petbits/pages/equipe.py`; testes.
- Backend: nenhum.
