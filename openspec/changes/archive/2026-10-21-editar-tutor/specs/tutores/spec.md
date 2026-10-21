## ADDED Requirements

### Requirement: A equipe altera os dados de um tutor

A equipe SHALL poder alterar nome, CPF, telefone, e-mail e endereço de um
tutor. Só os campos enviados MUST mudar. O CPF MUST ter 11 dígitos, ser válido
e não pertencer a outro tutor. O e-mail MUST NOT ser de outro tutor nem de
outra conta. Quando o tutor tem conta de cliente, mudar o e-mail SHALL mudar
também o e-mail de entrada, na mesma transação. A operação MUST ser exclusiva
da equipe.

#### Scenario: Corrigir o CPF

- **WHEN** a atendente troca o CPF de um tutor por um CPF válido e livre
- **THEN** o tutor passa a ter o CPF novo, e o perfil do cliente mostra o novo

#### Scenario: CPF de outro tutor

- **WHEN** a atendente informa o CPF de outro tutor
- **THEN** a alteração é recusada e nada muda

#### Scenario: Trocar o e-mail de quem tem conta

- **WHEN** a atendente troca o e-mail de um tutor que tem conta no site
- **THEN** o cliente passa a entrar com o e-mail novo e a mesma senha

#### Scenario: Conta da equipe ligada à ficha

- **WHEN** a ficha está ligada a uma conta que não é de cliente e alguém tenta trocar o e-mail
- **THEN** a alteração é recusada

#### Scenario: Tutor tenta alterar

- **WHEN** uma conta de cliente chama a alteração, fora da interface
- **THEN** o backend recusa
