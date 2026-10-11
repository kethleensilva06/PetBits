# Spec Delta

## ADDED Requirements

### Requirement: A equipe tem dois níveis

O sistema SHALL distinguir **gerência** de **equipe comum**. Os dois alcançam
a área da clínica; apenas a gerência mantém o quadro de colaboradores.

A verificação de nível MUST acontecer no backend, e MUST ler o papel do banco
a cada requisição. A conferência MUST ser por igualdade ao papel esperado, e
não por exclusão dos demais.

#### Scenario: Equipe comum alcança a área da clínica

- **WHEN** uma conta de equipe comum abre o painel, o catálogo, os tutores ou
  os animais
- **THEN** recebe os dados normalmente

#### Scenario: Equipe comum não mantém o quadro

- **WHEN** uma conta de equipe comum tenta criar ou alterar um colaborador,
  fora da interface
- **THEN** o backend recusa
- **AND** o cadastro permanece inalterado

#### Scenario: Gerência mantém o quadro

- **WHEN** uma conta de gerência cria ou altera um colaborador
- **THEN** a operação é aceita

#### Scenario: Tutor continua fora

- **WHEN** uma conta de tutor tenta qualquer operação da área da clínica
- **THEN** o backend recusa, como antes

#### Scenario: Papel desconhecido não vira gerência

- **WHEN** uma conta cujo papel está ausente ou fora dos valores previstos
  tenta manter o quadro
- **THEN** o backend recusa

### Requirement: A interface mostra só o que a conta alcança

A área da clínica SHALL omitir, para quem não é da gerência, os controles de
manter o quadro. Omitir MUST ser conveniência: a requisição direta, sem
gerência, MUST ser recusada pelo backend.

#### Scenario: Equipe comum não vê os controles

- **WHEN** uma conta de equipe comum abre a tela de colaboradores
- **THEN** a lista aparece
- **AND** não há controle de criar nem de alterar

#### Scenario: Nível adulterado no navegador

- **WHEN** alguém altera o papel guardado no armazenamento local para o de
  gerência
- **THEN** os controles aparecem
- **AND** cada operação de manter o quadro é recusada pelo backend
