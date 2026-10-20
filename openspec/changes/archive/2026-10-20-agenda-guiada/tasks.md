## 1. Calendário

- [x] 1.1 `petbits/calendario.py`: `ics(...)` conforme a RFC 5545, com testes em `tests/test_calendario.py`

## 2. State

- [x] 2.1 `passos`, `linhas_do_resumo` e `ultimo_agendamento` no `AgendaState`; `baixar_ics`
- [x] 2.2 `tests/test_agenda_guiada.py` para passos e resumo

## 3. Tela

- [x] 3.1 Faixa de progresso, passos numa coluna, resumo fixo ao lado com o Confirmar
- [x] 3.2 Botão "Adicionar à agenda do celular" no aviso de sucesso

## 4. Verificação

- [x] 4.1 Testes locais passam
- [x] 4.2 No navegador, como Ana: os passos avançam, o resumo enche; computador e celular (sem marcar de verdade: o botão do .ics só aparece depois de marcar, e o arquivo está coberto por `tests/test_calendario.py`)
