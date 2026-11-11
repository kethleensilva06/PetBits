## Why

A usuária relata ter de entrar de novo toda vez que fecha e abre o site. No
código, o token já fica no armazenamento local e vale 24 horas no Xano; no
site local, entrar, fechar a aba e abrir outra manteve a sessão. Mas nada na
tela diz quanto tempo a sessão dura, a validade é só a do Xano (que o site não
conhece até a próxima revalidação) e não há como escolher, num computador de
recepção, que a sessão acabe ao fechar o navegador. O pedido: manter a pessoa
dentro da área dela por algumas horas.

## What Changes

- A tela de entrada (clientes e equipe) ganha a caixa **Manter conectado**,
  marcada de início.
- Marcada: a sessão vale **12 horas** a partir da entrada, mesmo fechando o
  navegador.
- Desmarcada: a sessão acaba ao fechar o navegador (e nunca passa das mesmas
  12 horas). Abas novas continuam dentro enquanto o navegador estiver aberto.
- A validade é conferida pelo próprio site ao abrir qualquer página, sem
  requisição ao Xano. Vencida, a pessoa vai para a entrada com o aviso "Sua
  sessão expirou"; fechada pelo navegador, volta sem aviso.
- O cadastro também deixa a pessoa conectada por 12 horas.
- Sessões guardadas antes desta change, sem validade, são encerradas sem aviso
  uma vez.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `autenticacao`: a persistência da sessão passa a ter validade de 12 horas e
  a escolha de manter conectado.

## Impact

- Código: `petbits/states/auth_state.py`, `petbits/pages/entrar.py`; testes.
- Backend: nenhum. O token do Xano continua valendo 24 horas, mais que as 12
  do site.
