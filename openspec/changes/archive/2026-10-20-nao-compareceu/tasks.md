## 1. Backend

- [x] 1.1 `tables/agendamento.xs`: `faltou` no enum
- [x] 1.2 `equipe_agendamento_falta.xs`: prova de equipe, trava, só `marcado` com início passado
- [x] 1.3 `equipe_atendimento_create.xs`: só `marcado` ou `em_andamento`
- [x] 1.4 Validar, publicar e provar: tutor recusado, futuro recusado, passado aceito, atendimento recusado depois

## 2. Tela

- [x] 2.1 Rótulo "Não compareceu"; `xano.marcar_falta`; `EquipeState.marcar_falta`
- [x] 2.2 Botão Não compareceu, com confirmação, no agendamento marcado já começado

## 3. Verificação

- [x] 3.1 Testes locais passam
- [x] 3.2 No navegador, como equipe

Medido no Xano: conta de tutor recusada; agendamento futuro (6) recusado,
"ainda não chegou"; inexistente, "não encontrado"; um marcado de 10 dias atrás
(1, dado de teste antigo) passou a `faltou`, e marcar de novo foi recusado;
registrar atendimento a partir dele, com veterinário, foi recusado. Na tela, o
agendamento 9 (5 dias atrás, marcado) mostrou o botão, e a confirmação o passou
a "Não compareceu". Os agendamentos 1 e 9 ficam com falta.
- [x] 3.3 Mensagens novas acentuadas (`petbits/mensagens.py`: "só", "concluído")
