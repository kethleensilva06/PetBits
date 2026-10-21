## ADDED Requirements

### Requirement: Horário e contato à vista

A página inicial pública e todas as telas do cliente SHALL mostrar o horário
de funcionamento (segunda a sábado, das 8h às 18h; domingo fechado) e o e-mail
de contato petbitsgroup@gmail.com, com link para escrever.

#### Scenario: Visitante procura o contato

- **WHEN** alguém abre a página inicial sem entrar
- **THEN** vê o horário de funcionamento e o e-mail petbitsgroup@gmail.com

#### Scenario: Cliente em qualquer tela

- **WHEN** a tutora está na Loja
- **THEN** o rodapé mostra o horário e o e-mail de contato
