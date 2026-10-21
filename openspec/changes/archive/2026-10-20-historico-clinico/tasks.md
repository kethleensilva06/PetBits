## 1. Backend

- [x] 1.1 `tables/atendimento.xs` (D1)
- [x] 1.2 `equipe_atendimento_create.xs` (D2, D4)
- [x] 1.3 `equipe_animal_historico.xs` e `pet_historico.xs` (D3)
- [x] 1.4 `equipe_agenda.xs` devolve `id_pet`, `id_colaborador` e `servico_categoria` (D5)
- [x] 1.5 Validar, `--dry-run`, publicar — a prévia mostrou a tabela nova, três endpoints novos e a agenda atualizada

## 2. Reflex

- [x] 2.1 Cliente HTTP em `petbits/xano.py`
- [x] 2.2 Clínica: histórico e registro nos animais; registro pela agenda; retificar (D5) — em `petbits/states/historico_state.py` e `petbits/pages/historico.py`, fora do `EquipeState`; a linha do tempo é montada por `petbits/historico.py` (funções puras, com `tests/test_historico.py`)
- [x] 2.3 Casa do tutor: linha do tempo (D5)

## 3. Docs

- [x] 3.1 `docs/project-overview.md`: histórico entregue

## 4. Verificação

- [x] 4.1 Contra o Xano, como no design — **Feito em 20/10:** registro de emergência da Mel aceito; recusas com 400 para diagnóstico só de espaços, atendente (Bianca), colaboradora desligada (Renata), data futura, retorno antes da data, retificação apontando para atendimento da Nina, agendamento cancelado e agendamento já concluído; conta de tutor recebeu 403 no registro e na rota de leitura da equipe. A retificação foi aceita e ficou com `retifica` apontando para o original. Registrar a partir de um agendamento marcado (consulta da Mel, amanhã às 10h) gravou o atendimento e deixou o agendamento `concluido`. O tutor leu o histórico da Mel com só `colaborador_nome` e `colaborador_funcao` de quem atendeu — nenhum contato, nem `registrado_por` —; outro tutor e um id inexistente receberam o mesmo 404.
      Os atendimentos de teste não se apagam, por regra: ficam no histórico da Mel e da Nina (animais de teste da Ana), com o motivo "Verificação do sistema"
- [x] 4.2 Navegador: registrar, retificar, ler na casa — **Visto em 20/10:** como Carla, "Histórico" da Mel abriu a linha do tempo com o original "Retificado" e a correção "Retificação de 20/10/2026"; "Registrar atendimento" abriu o formulário com a data de hoje e só os cinco veterinários e clínicos gerais ativos na escolha de quem atendeu; o registro (peso digitado "28,7") entrou no topo da lista; "Retificar" abriu o formulário com tudo preenchido e o aviso de que o original continua (cancelado, sem gravar). Na agenda, o botão aparecia também nos banhos da tosadora — corrigido para só serviço clínico (D5); registrar pela consulta das 15h da Nina deixou o agendamento "Concluído" e sem o botão. Como Ana, "Histórico" da Mel mostrou os quatro atendimentos, sem "Retificar", e o do Tomate disse que ainda não há atendimento.
      Duas observações da verificação: um clique em "Registrar" disparado logo depois de digitar foi recusado com "diagnóstico em branco", porque o campo ainda não tinha mandado o texto (os campos do Reflex esperam uma fração de segundo) — o segundo clique passou; e a recarga da agenda depois do registro deu o aviso de limite de requisições do Xano, por causa da quantidade de chamadas da própria verificação, e passou na tentativa seguinte. Os atendimentos do mesmo dia apareciam em ordem arbitrária; a linha do tempo passou a desempatar pelo registro mais recente
- [x] 4.3 `unittest`, `verificar_equipe.py`, `openspec validate historico-clinico --strict`
