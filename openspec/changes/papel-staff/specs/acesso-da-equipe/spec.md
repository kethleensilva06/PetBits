## MODIFIED Requirements

### Requirement: Conta sem papel definido não alcança nada da clínica

Os papéis de equipe SHALL ser `admin` e `staff`, com o mesmo acesso. Uma conta
cujo papel esteja ausente, vazio ou com qualquer outro valor SHALL ser tratada
como **sem** acesso à área da clínica. A verificação MUST ser por igualdade a
um dos papéis de equipe, e não por exclusão do papel de tutor.

#### Scenario: Conta sem papel

- **WHEN** uma conta sem papel definido tenta uma operação da área da clínica
- **THEN** o backend recusa
- **AND** recebe a mesma recusa que uma conta de tutor receberia, sem revelar
  em que estado a conta está

#### Scenario: Papel com valor desconhecido

- **WHEN** uma conta cujo papel não é nem equipe nem tutor tenta uma operação
  da área da clínica
- **THEN** o backend recusa

#### Scenario: Conta staff

- **WHEN** uma conta com papel `staff` entra pela entrada da equipe e abre a
  gerência
- **THEN** ela vai para a gerência e o backend atende as operações da clínica,
  como para `admin`
