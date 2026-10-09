## 1. Preparação

- [x] 1.1 Conferir o login do Xano CLI (`xano profile me`) contra o workspace 169225; puxar o workspace para uma pasta **temporária** fora do projeto e registrar o formato de pastas que o CLI usa — nada é publicado neste passo
- [x] 1.2 Validar com `scripts/validar_xanoscript.mjs` todo `.xs` novo ou alterado antes de qualquer publicação

## 2. Tabelas

- [x] 2.1 `tables/agendamento.xs`: `id_pet`, `id_servico`, `id_colaborador`, `inicio`, `fim` (timestamps), `situacao` (enum D7), `observacoes?`, `cancelado_em?`, `created_at`, com índices por `id_colaborador`+`inicio` e por `id_pet`; publicar com `--dry-run` primeiro; verificar pelo schema publicado
- [x] 2.2 `servico.categoria` (`enum?`, D5); publicar; verificar que os serviços existentes continuam listando na tela da equipe

## 3. Endpoints do tutor

- [ ] 3.1 `servico_list_tutor.xs` (`GET servicos`): `auth = "user"`, só serviços com categoria, `output` explícito; verificar com um serviço sem categoria que ele não aparece — **Situação:** publicado em 2026-10-08; sem token responde 401. Falta a verificação com conta de tutor
- [ ] 3.2 `agenda_ocupacao.xs` (`GET agenda/ocupacao`): profissionais compatíveis e intervalos ocupados não cancelados do dia (D2); verificar que a resposta não tem nome nem contato — **Situação:** publicado em 2026-10-08; sem token responde 401. Falta a verificação com conta de tutor
- [ ] 3.3 `agendamento_create.xs` (`POST agendamentos`): posse do animal, categoria, grade, futuro, expediente (D3), escolha do profissional dentro de transação com trava (D4); verificar cada recusa da spec com uma requisição — **Situação:** publicado em 2026-10-08; sem token responde 400 (os campos obrigatórios são conferidos antes do login) e, com os campos, 401. Falta a verificação de cada recusa com conta de tutor, e a das duas marcações simultâneas
- [ ] 3.4 `agendamento_list.xs` (`GET agendamentos`): só dos animais do tutor, com nomes de animal, serviço e profissional; verificar com duas contas — **Situação:** publicado em 2026-10-08; sem token responde 401. Falta a verificação com duas contas
- [ ] 3.5 `agendamento_cancelar.xs` (`POST agendamentos/{id}/cancelar`): D6; verificar prazo de 24 h, já cancelado, e agendamento alheio respondendo como inexistente — **Situação:** publicado em 2026-10-08; sem token responde 401. Falta a verificação com conta de tutor

## 4. Endpoints da equipe

- [ ] 4.1 `equipe_agenda.xs` (`GET equipe/agenda`): D8; verificar que a guarda `verificar_equipe.py` passa com ele, e com token de tutor que recusa — **Situação:** publicado em 2026-10-08; a guarda passa com 12 endpoints; com sessão de equipe a agenda do dia abriu, vazia e sem erro. Falta a recusa com token de tutor
- [ ] 4.2 `equipe_servico_create.xs` e `equipe_servico_update.xs` aceitam `categoria`, recusando valor fora do conjunto; verificar com "hospedagem" — **Situação:** publicado em 2026-10-08; na tela da equipe, o serviço "Banho e tosa" foi salvo com a categoria e voltou classificado. Falta a recusa de "hospedagem"

## 5. Reflex

- [x] 5.1 Cliente HTTP em `petbits/xano.py` para os endpoints novos
- [x] 5.2 Cálculo dos horários livres em Python (D2, D3) com testes dos cenários da spec: dia útil vazio, sábado com 90 min, domingo, profissional ocupado em parte, sem profissional
- [x] 5.3 Página `/agenda` do tutor: categoria, serviço, animal, calendário do mês (domingos e dias passados desabilitados), horários livres, observações, confirmar; "Meus agendamentos" com Cancelar só quando faltar mais de 24 h
- [x] 5.4 Link para a agenda na tela inicial do tutor
- [x] 5.5 Página `/equipe/agenda` só leitura, com troca de dia, e item no menu da equipe
- [x] 5.6 Campo Categoria no formulário de serviço da equipe e na lista

## 6. Verificação de ponta a ponta

- [ ] 6.1 Percurso do tutor no navegador: marcar, ver na lista, cancelar com mais de 24 h; e o horário cancelado voltar a aparecer como livre
- [ ] 6.2 Percurso da equipe: definir categoria de um serviço, ver o agendamento na agenda do dia
- [ ] 6.3 Medir o custo em requisições de abrir a agenda e de escolher um dia (`PETBITS_MEDIR`)
- [ ] 6.4 `openspec validate --strict` e `verificar_equipe.py` limpos
