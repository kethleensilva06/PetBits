## 1. Horário

- [x] 1.1 `petbits/clinica.py` com o horário e o e-mail; `EXPEDIENTE` de sábado até 18h
- [x] 1.2 `agendamento_create.xs`: sábado até 18h; validar e publicar
- [x] 1.3 Provar no Xano: sábado às 17h aceito (e cancelado em seguida), domingo recusado

## 2. Tela

- [x] 2.1 Rodapé com horário e e-mail nas telas do cliente; bloco na página inicial; texto da agenda
- [x] 2.2 `tests/test_clinica.py`: o texto do horário bate com o `EXPEDIENTE`

## 3. Verificação

- [x] 3.1 Testes locais passam
- [x] 3.2 No navegador: página inicial, Loja, Agenda com sábado à tarde
- [x] 3.3 Os testes antigos do sábado às 12h foram atualizados: `tests/test_agenda.py` (último horário de 90 min passa a 16h30) e a recusa de `scripts/verificar_ponta_a_ponta.py` (passa a 17h30, que não cabe antes das 18h)

Medido no Xano: sábado 24/10 às 18h, recusado ("não cabe no horário"); às 17h,
aceito (agendamento de teste 12 da Ana, cancelado em seguida). Na tela, a Agenda
oferece de 08:00 a 17:30 no sábado para a consulta de 30 min; o rodapé da Loja e
a página inicial mostram o horário e o e-mail, com link.
