# painel-da-clinica Specification

## Purpose
Define o que o painel da clínica — a tela inicial da equipe — mostra: quem
vem hoje e os pedidos que esperam a equipe, numa requisição só e sem
contato de tutor.

## Requirements

### Requirement: O painel mostra quem vem hoje

O painel da clínica SHALL abrir com os agendamentos do dia de hoje, de todos
os profissionais, em ordem de horário, com horário, animal, tutor, serviço,
profissional e situação. Os agendamentos cancelados MUST NOT aparecer. O
painel MUST NOT mostrar telefone, documento nem endereço do tutor.

#### Scenario: Dia com agendamentos

- **WHEN** alguém da equipe abre o painel num dia com consultas marcadas às 9h e às 15h
- **THEN** vê as duas, a das 9h primeiro, com o animal, o tutor, o serviço e o profissional

#### Scenario: Agendamento cancelado

- **WHEN** um dos agendamentos de hoje foi cancelado
- **THEN** ele não aparece no painel

#### Scenario: Dia sem agendamentos

- **WHEN** não há agendamento hoje
- **THEN** o painel diz que não há ninguém marcado para hoje e oferece abrir a Agenda

### Requirement: O painel mostra os pedidos que esperam a equipe

O painel SHALL mostrar quantos pedidos estão aguardando pagamento, pagos e
prontos para retirada. Clicar num desses números SHALL abrir a tela de
Pedidos filtrada por aquela situação.

#### Scenario: Abrir os pagos

- **WHEN** alguém da equipe clica no número de pedidos pagos
- **THEN** vai para Pedidos com o filtro "Pagos" escolhido

### Requirement: O painel custa uma requisição

Abrir o painel SHALL fazer uma única requisição ao Xano, e essa requisição
MUST ser exclusiva da equipe.

#### Scenario: Abrir o painel

- **WHEN** alguém da equipe abre o painel
- **THEN** sai uma requisição, `GET equipe/painel`, com contadores, agenda do dia e pedidos

#### Scenario: Tutor pede o painel

- **WHEN** uma conta de tutor pede o painel, fora da interface
- **THEN** o backend recusa
