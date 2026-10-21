## 1. Retorno

- [x] 1.1 `proximo_retorno` em `petbits/historico.py`, com testes
- [x] 1.2 `HistoricoTutorState`: `retorno`, `pet_id` e `agendar_retorno`
- [x] 1.3 Aviso e botão no histórico do tutor

## 2. Verificação

- [x] 2.1 Testes locais passam
- [x] 2.2 No navegador, como Ana (localhost)

Achado na verificação: a regra "só o atendimento mais recente" escondia um
retorno pendente quando vinha depois um atendimento sem retorno (uma vacina).
Passou a valer o retorno mais próximo, de hoje em diante, entre todos os
atendimentos não retificados. Conferido como Ana: a Mel não mostra retorno (o de
30/10 estava no atendimento retificado, e a correção não tem retorno); a Nina,
com um atendimento de teste (7, "Verificação do sistema", permanente como os
outros) com retorno em 28/10, mostra "Retorno sugerido para 28/10/2026", e o
botão abriu a Agenda com a Nina e a Clínica escolhidas.
