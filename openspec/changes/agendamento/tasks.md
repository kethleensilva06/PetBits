## 1. Preparação

- [x] 1.1 Conferir o login do Xano CLI (`xano profile me`) contra o workspace 169225; puxar o workspace para uma pasta **temporária** fora do projeto e registrar o formato de pastas que o CLI usa — nada é publicado neste passo
- [x] 1.2 Validar com `scripts/validar_xanoscript.mjs` todo `.xs` novo ou alterado antes de qualquer publicação

## 2. Tabelas

- [x] 2.1 `tables/agendamento.xs`: `id_pet`, `id_servico`, `id_colaborador`, `inicio`, `fim` (timestamps), `situacao` (enum D7), `observacoes?`, `cancelado_em?`, `created_at`, com índices por `id_colaborador`+`inicio` e por `id_pet`; publicar com `--dry-run` primeiro; verificar pelo schema publicado
- [x] 2.2 `servico.categoria` (`enum?`, D5); publicar; verificar que os serviços existentes continuam listando na tela da equipe

## 3. Endpoints do tutor

- [ ] 3.1 `servico_list_tutor.xs` (`GET servicos`): `auth = "user"`, só serviços com categoria, `output` explícito; verificar com um serviço sem categoria que ele não aparece — **Situação:** publicado em 2026-10-08; sem token responde 401. Falta a verificação com conta de tutor
- [x] 3.2 `agenda_ocupacao.xs` (`GET agenda/ocupacao`): profissionais compatíveis e intervalos ocupados não cancelados do dia (D2); verificar que a resposta não tem nome nem contato — **Situação:** publicado; a rodada da ponta a ponta ampliada em 2026-10-11 conferiu que a resposta só traz ids e intervalos, sem nome nem contato
- [ ] 3.3 `agendamento_create.xs` (`POST agendamentos`): posse do animal, categoria, grade, futuro, expediente (D3), escolha do profissional dentro de transação com trava (D4); verificar cada recusa da spec com uma requisição — **Situação:** publicado; a ponta a ponta provou grade de 30 minutos, horário livre aceito e sobreposição com o único profissional recusada; a rodada da ponta a ponta ampliada em 2026-10-11 provou domingo, antes das 8h, fim depois do fechamento de sábado, horário no passado e animal de outro cliente recusados. Falta: marcações simultâneas
- [x] 3.4 `agendamento_list.xs` (`GET agendamentos`): só dos animais do tutor, com nomes de animal, serviço e profissional; verificar com duas contas — **Situação:** publicado; a rodada da ponta a ponta ampliada em 2026-10-11 conferiu com duas contas que o segundo cliente não vê o agendamento do primeiro
- [x] 3.5 `agendamento_cancelar.xs` (`POST agendamentos/{id}/cancelar`): D6; verificar prazo de 24 h, já cancelado, e agendamento alheio respondendo como inexistente — **Situação:** publicado; a ponta a ponta provou cancelar com mais de 24 h e cancelar de novo recusado; a rodada da ponta a ponta ampliada em 2026-10-11 provou que o agendamento de outro cliente é recusado. O prazo de menos de 24 h fica com o teste local `pode_cancelar` e a leitura do endpoint (design da `ampliar-ponta-a-ponta`, D2): testá-lo deixaria um agendamento que ninguém cancela

## 4. Endpoints da equipe

- [x] 4.1 `equipe_agenda.xs` (`GET equipe/agenda`): D8; verificar que a guarda `verificar_equipe.py` passa com ele, e com token de tutor que recusa — **Situação:** publicado; a guarda passa na conferência 1–3 (a 5 acusa os arquivos de autenticação não publicados, assunto à parte); cliente pedindo a agenda da clínica foi recusado na ponta a ponta
- [x] 4.2 `equipe_servico_create.xs` e `equipe_servico_update.xs` aceitam `categoria`, recusando valor fora do conjunto; verificar com "hospedagem" — **Situação:** publicado em 2026-10-08; a categoria foi salva pela tela da equipe; a rodada da ponta a ponta ampliada em 2026-10-11 provou "hospedagem" recusada

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
- [x] 6.4 `openspec validate --strict` e `verificar_equipe.py` limpos — **Situação:** em 2026-10-11, depois da change `limpar-endpoints-fora-do-ar`: `validate --all --strict` sem falha e `verificar_equipe.py` sem acusação
