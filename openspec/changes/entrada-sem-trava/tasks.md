## 1. Código

- [x] 1.1 `entrar`: zerar `enviando` num `finally` em volta das chamadas ao Xano (D1); verificar com uma falha simulada que não é `XanoError` que `enviando` termina em `False`
- [x] 1.2 `cadastrar`: o mesmo `finally` (D1); verificar do mesmo jeito
- [x] 1.3 `redirecionar_se_logado` zera `enviando` (D2); verificar com `enviando = True` que a chamada o deixa em `False`

## 2. Percurso

- [x] 2.1 No navegador que estava travado: recarregar a tela de entrada e conferir que o botão Entrar está habilitado
- [x] 2.2 Conferir que o botão continua desabilitado **durante** o envio (o comportamento original não se perdeu)

## 3. Fechamento

- [x] 3.1 Rodar `openspec validate --strict` e `scripts/verificar_equipe.py`; os dois limpos
