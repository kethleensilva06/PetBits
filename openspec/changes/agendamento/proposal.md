## Why

Hoje o tutor cadastra os animais e não consegue fazer mais nada com eles: não
há como marcar uma consulta ou um banho. É a change 4 do roteiro, e a primeira
em que o sistema passa a fazer o trabalho de uma clínica — reservar o tempo de
um profissional para um animal. O modelo de domínio já chama o Agendamento de
"o conceito onde mora a regra mais delicada do sistema": dois agendamentos não
podem ocupar o mesmo profissional ao mesmo tempo.

## What Changes

- **Tela de agenda do tutor** (`/agenda`), com um calendário do mês. O tutor
  escolhe **Clínica** ou **Banho e tosa**, o serviço, o animal e o dia; vê os
  horários livres daquele dia e confirma um.
- **O sistema escolhe o profissional**: um veterinário (ou clínico geral) para
  serviço de clínica, um tosador para banho e tosa, entre os ativos que
  estiverem livres no intervalo inteiro do serviço.
- **Horário de funcionamento**: segunda a sexta, das 8h às 18h; sábado, das 8h
  às 12h; domingo fechado. Horários de 30 em 30 minutos, no fuso de São Paulo.
  O atendimento inteiro — início mais duração — tem de caber no expediente.
- **Meus agendamentos**: o tutor vê os seus, com animal, serviço, profissional,
  dia, hora e situação, e **cancela até 24 horas antes**. Cancelar não apaga:
  o registro fica, marcado como cancelado, e o horário volta a ficar livre.
- **Agenda da clínica** (`/equipe/agenda`): a equipe vê os agendamentos de um
  dia, só leitura.
- **Categoria do serviço**: o catálogo ganha a categoria (`clinica` ou
  `banho_tosa`), escolhida pela equipe na tela de serviços. Serviço sem
  categoria não é oferecido ao tutor.
- **O tutor lê o catálogo**: nome, descrição, preço e duração dos serviços com
  categoria. Alterar continua exclusivo da equipe.

## Capabilities

### New Capabilities

- `agendamentos`: marcar, listar e cancelar agendamentos pelo tutor; a
  não-sobreposição por profissional; o horário de funcionamento; a escolha do
  profissional pela função; a agenda do dia para a equipe.

### Modified Capabilities

- `servicos`: categoria do serviço, e leitura do catálogo pelo tutor.

## Fora do escopo

- A equipe marcar, remarcar, cancelar ou mudar a situação de um agendamento
  (em andamento, concluído). A agenda da equipe é só leitura nesta change; as
  situações existem na tabela para a change de histórico clínico usar.
- Remarcar: o tutor cancela e marca de novo.
- Feriados, folgas e horário próprio de cada profissional. Todo profissional
  ativo é considerado disponível no expediente da clínica.
- Notificação por e-mail ou mensagem.
- Pagamento.

## Impact

- **Xano**: tabela nova `agendamento`; coluna nova `categoria` em `servico`;
  endpoints novos do tutor (`servicos` para leitura, `agenda/ocupacao`,
  `agendamentos` para listar e criar, `agendamentos/{id}/cancelar`) e da equipe
  (`equipe/agenda`); `equipe_servico_create` e `equipe_servico_update` passam a
  aceitar a categoria. Publicação pelo Xano CLI.
- **Reflex**: página `/agenda` e estado próprio; página `/equipe/agenda`;
  campo de categoria no formulário de serviço; link para a agenda na tela
  inicial do tutor e no menu da equipe.
- **Orçamento de requisições (10 a cada 20 s)**: abrir a agenda custa 3
  (serviços, animais, meus agendamentos); escolher um dia custa 1; confirmar
  custa 2 (criar e recarregar a lista).
