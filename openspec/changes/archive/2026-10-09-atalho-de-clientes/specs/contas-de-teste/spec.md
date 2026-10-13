## MODIFIED Requirements

### Requirement: Atalho de contas de teste na tela de entrada

Em modo de desenvolvimento, a tela de entrada SHALL abrir a lista das contas
de teste da **equipe** quando a pessoa pressionar `Alt+1`, e a dos
**clientes** quando pressionar `Alt+2`. Uma conta é de cliente quando o
rótulo do bloco começa com `TUTOR` ou `CLIENTE`; qualquer outra é de equipe.
Com uma lista aberta, o atalho da outra SHALL trocar de lista, o da mesma
SHALL fechá-la, e `Esc` SHALL fechar qualquer uma. A lista MUST mostrar, para
cada conta, apenas o rótulo e o e-mail — nunca a senha.

#### Scenario: Abrir a lista

- **WHEN** a pessoa está na tela de entrada, em modo de desenvolvimento, e
  pressiona `Alt+1`
- **THEN** a lista das contas de equipe aparece no canto inferior esquerdo
- **AND** cada item mostra o rótulo e o e-mail da conta, sem a senha

#### Scenario: Abrir a lista de clientes

- **WHEN** a pessoa pressiona `Alt+2`
- **THEN** aparece só a lista das contas cujo rótulo começa com `TUTOR` ou
  `CLIENTE`

#### Scenario: Trocar de lista

- **WHEN** a lista da equipe está aberta e a pessoa pressiona `Alt+2`
- **THEN** a lista passa a ser a dos clientes, sem fechar

#### Scenario: Fechar a lista

- **WHEN** a lista está aberta e a pessoa pressiona `Esc`, ou o mesmo atalho
  que a abriu
- **THEN** a lista fecha e o formulário fica como estava

#### Scenario: A lista não depende da aba

- **WHEN** a pessoa abre a lista com a aba Cliente e depois com a aba
  Colaborador
- **THEN** a lista é a mesma nas duas
