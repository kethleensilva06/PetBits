## MODIFIED Requirements

### Requirement: Tema do sistema

O app SHALL usar um tema único em todas as telas: cor principal verde-água
(`teal`), cinza quente (`sand`), cantos grandes e a fonte Nunito, sempre na
aparência clara, com o fundo da página branco. A aparência MUST NOT mudar
com a preferência do sistema operacional nem com escolha guardada no
navegador.

#### Scenario: Sistema em modo claro

- **WHEN** alguém abre qualquer tela com o sistema em modo claro
- **THEN** a tela aparece clara, com fundo branco, botões principais verde-água e texto em Nunito

#### Scenario: Sistema em modo escuro

- **WHEN** alguém abre qualquer tela com o sistema em modo escuro
- **THEN** a tela aparece clara do mesmo jeito, com fundo branco

#### Scenario: Trocar pelo ícone

- **WHEN** alguém procura o ícone de sol/lua no topo ou nas portas de entrada
- **THEN** não há ícone: a aparência não se troca pela tela

#### Scenario: A escolha fica

- **WHEN** o navegador guardou o escuro pelo ícone que existia antes
- **THEN** a tela abre clara mesmo assim, e o valor guardado passa a ser o claro
