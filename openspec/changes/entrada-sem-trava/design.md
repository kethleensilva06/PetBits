## Context

`AuthState.enviando` desabilita o botão de envio das duas telas da porta de
entrada. O estado do Reflex é por navegador e, em desenvolvimento, sobrevive
ao recarregamento da página e ao reinício do backend — então um `True`
esquecido não some sozinho.

## Goals / Non-Goals

**Goals:** nenhum caminho deixa `enviando` preso em `True`.

**Non-Goals:** mudar mensagens, abas, verificação ou destino.

## Decisions

### D1 — `finally` em volta da chamada ao Xano

`entrar` e `cadastrar` passam a zerar `enviando` num `finally` que envolve as
chamadas. Cobre a recusa, o erro inesperado e o sucesso pelo mesmo ponto, em
vez de repetir `self.enviando = False` em cada ramo — que foi exatamente o que
deixou um ramo de fora.

### D2 — Abrir a tela libera o botão

O `finally` não cobre o processo que morre no meio: se o backend reinicia
durante a requisição, nenhum código daquela execução roda mais. Por isso o
`on_load` das duas telas (`redirecionar_se_logado`) também zera `enviando`.

*Alternativa descartada:* não guardar `enviando` no estado. Ele precisa estar
no estado para o botão reagir enquanto a requisição corre.

*Efeito aceito:* recarregar a página **durante** uma tentativa legítima libera
o botão antes de ela terminar, e a pessoa poderia enviar de novo. O pior caso é
uma segunda tentativa de entrar — que custa uma requisição e não muda o
resultado.

## Risks / Trade-offs

- [Erro inesperado continua sem mensagem própria] → Fora do escopo; o botão
  volta, e o erro aparece como o Reflex já mostra.
