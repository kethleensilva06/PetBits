# Spec Delta

## Purpose

Define o que distingue uma conta da equipe da clínica de uma conta de tutor:
para onde cada uma é levada ao entrar, o que cada uma alcança, e o que acontece
com uma conta cujo papel não está definido.

## ADDED Requirements

### Requirement: O papel decide para onde a pessoa vai

Ao entrar, o sistema SHALL conduzir a pessoa à área correspondente ao papel da
conta: a equipe ao painel da clínica, o tutor aos seus animais. O papel MUST
ser lido do servidor, nunca do que o cliente informou.

#### Scenario: Conta de equipe entra

- **WHEN** uma conta com papel de equipe é autenticada
- **THEN** a pessoa é levada ao painel da clínica

#### Scenario: Conta de tutor entra

- **WHEN** uma conta com papel de tutor é autenticada
- **THEN** a pessoa é levada à área dos animais dela

#### Scenario: Papel alterado enquanto a sessão está aberta

- **WHEN** o papel de uma conta é alterado no servidor e a pessoa recarrega a
  página
- **THEN** o sistema passa a tratá-la pelo papel novo, sem precisar entrar de
  novo

### Requirement: Somente a equipe alcança a operação da clínica

Toda operação sobre colaboradores, serviços, e sobre a visão da clínica de
tutores e animais SHALL exigir uma conta de equipe. A recusa MUST acontecer no
backend, e MUST valer para requisições feitas fora da interface.

#### Scenario: Tutor tenta alcançar a operação

- **WHEN** uma conta de tutor faz qualquer operação da área da clínica
- **THEN** o backend recusa
- **AND** nenhum dado é devolvido

#### Scenario: Requisição sem credencial

- **WHEN** qualquer operação da área da clínica é feita sem credencial
- **THEN** o backend recusa

#### Scenario: Papel adulterado no navegador

- **WHEN** alguém altera o papel guardado no armazenamento local para o de
  equipe e navega até a área da clínica
- **THEN** nenhum dado da clínica é devolvido
- **AND** o backend recusa cada operação

### Requirement: Conta sem papel definido não alcança nada da clínica

Uma conta cujo papel esteja ausente, vazio ou com valor desconhecido SHALL ser
tratada como **sem** acesso à área da clínica. A verificação MUST ser por
igualdade ao papel de equipe, e não por exclusão do papel de tutor.

#### Scenario: Conta sem papel

- **WHEN** uma conta sem papel definido tenta uma operação da área da clínica
- **THEN** o backend recusa
- **AND** recebe a mesma recusa que uma conta de tutor receberia, sem revelar
  em que estado a conta está

#### Scenario: Papel com valor desconhecido

- **WHEN** uma conta cujo papel não é nem equipe nem tutor tenta uma operação
  da área da clínica
- **THEN** o backend recusa

### Requirement: A área da clínica não aparece para quem não é da equipe

A interface SHALL oferecer a navegação da clínica apenas a quem tem conta de
equipe. Esconder MUST ser conveniência: o acesso direto ao endereço de uma
tela da clínica, sem conta de equipe, MUST NOT exibir nem carregar dado algum.

#### Scenario: Tutor acessa diretamente um endereço da clínica

- **WHEN** um tutor autenticado digita o endereço de uma tela da clínica
- **THEN** é conduzido de volta à área dele
- **AND** nenhuma requisição de dados daquela tela chega ao backend

#### Scenario: Visitante acessa diretamente um endereço da clínica

- **WHEN** alguém sem sessão acessa o endereço de uma tela da clínica
- **THEN** é conduzido à tela de entrada
