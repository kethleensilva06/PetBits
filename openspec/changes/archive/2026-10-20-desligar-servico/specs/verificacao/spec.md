## ADDED Requirements

### Requirement: O teste das duas contas não grava nada

O `scripts/teste_duas_contas.py` SHALL conferir cada endpoint de equipe sem
criar nem alterar registro. As sondas de escrita MUST usar um corpo que a
validação recusa depois da prova de equipe, de modo que a equipe receba uma
recusa diferente de 403 e o cliente receba 403.

#### Scenario: Rodada completa

- **WHEN** o teste das duas contas roda até o fim
- **THEN** a lista de serviços e a de colaboradores têm os mesmos registros de antes

#### Scenario: A prova continua sendo conferida

- **WHEN** a sonda de criação de serviço vai com a conta de equipe
- **THEN** a resposta é 400 (nome em branco), e não 403
