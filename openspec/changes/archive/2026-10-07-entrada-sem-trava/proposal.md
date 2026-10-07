## Why

O botão **Entrar** pode ficar desabilitado para sempre. `entrar` e
`cadastrar` marcam `enviando = True` antes de chamar o Xano e só voltam a
`False` no fim da execução normal ou num `XanoError`. Se a execução é
interrompida no meio — o servidor de desenvolvimento reinicia ao salvar um
arquivo, ou surge um erro que não é `XanoError` — o `False` nunca chega. Como
o estado do Reflex é guardado por navegador e sobrevive a recarregar a
página, a pessoa fica sem conseguir entrar nem criar conta naquele navegador.
Aconteceu de fato: o botão ficou cinza e recarregar não resolveu.

## What Changes

- `entrar` e `cadastrar` liberam o botão **em qualquer saída** — sucesso,
  recusa, erro inesperado — e não só nos caminhos previstos.
- Abrir a tela de entrada ou de cadastro **libera o botão**: uma tentativa que
  morreu no meio não deixa a tela travada para a próxima visita.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `autenticacao`: requisito novo de que as telas de entrada e de cadastro
  nunca ficam travadas por uma tentativa anterior.

## Fora do escopo

- Mensagem nova para erro inesperado: o erro continua aparecendo como o Reflex
  já mostra; o que muda é que o botão volta a funcionar.
- Qualquer mudança na verificação de credencial, nas abas ou no destino por
  papel.

## Impact

- Código: `petbits/states/auth_state.py` (`entrar`, `cadastrar`,
  `redirecionar_se_logado`).
- Requisições ao Xano: nenhuma a mais.
