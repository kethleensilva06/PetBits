## ADDED Requirements

### Requirement: As telas de entrada e de cadastro nunca ficam travadas

Uma tentativa de entrar ou de criar conta que termine de qualquer forma —
aceita, recusada, com erro inesperado ou interrompida — MUST NOT deixar o
botão de envio desabilitado. Ao abrir a tela de entrada ou de cadastro, o
botão de envio SHALL estar disponível.

#### Scenario: Recusa libera o botão

- **WHEN** a pessoa envia credenciais inválidas
- **THEN** a recusa aparece e o botão Entrar volta a ficar disponível

#### Scenario: Erro inesperado libera o botão

- **WHEN** a tentativa de entrar termina com um erro que não é uma recusa do
  Xano
- **THEN** o botão Entrar volta a ficar disponível

#### Scenario: Tentativa interrompida não trava a próxima visita

- **WHEN** uma tentativa foi interrompida no meio, sem resposta, e a pessoa
  abre ou recarrega a tela de entrada
- **THEN** o botão Entrar está disponível
