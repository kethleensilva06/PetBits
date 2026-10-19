## MODIFIED Requirements

### Requirement: Tema do sistema

O app SHALL usar um tema único em todas as telas: cor principal verde-água
(`teal`), cinza quente (`sand`), cantos grandes e a fonte Nunito. A aparência
clara ou escura SHALL seguir a preferência do sistema operacional até a
pessoa escolher outra pelo ícone de sol/lua, presente no topo das duas áreas
e nas portas de entrada. A escolha SHALL ficar guardada no navegador e valer
nas visitas seguintes, sem requisição ao backend.

#### Scenario: Sistema em modo claro

- **WHEN** alguém abre qualquer tela com o sistema em modo claro
- **THEN** a tela aparece clara, com botões principais verde-água e texto em Nunito

#### Scenario: Sistema em modo escuro

- **WHEN** alguém abre qualquer tela com o sistema em modo escuro
- **THEN** a tela aparece escura, com a mesma cor principal

#### Scenario: Trocar pelo ícone

- **WHEN** alguém toca no ícone de sol/lua
- **THEN** a tela troca de claro para escuro, ou o contrário, na hora

#### Scenario: A escolha fica

- **WHEN** a pessoa escolheu o escuro e recarrega a página ou volta outro dia
- **THEN** a tela abre escura, mesmo com o sistema em modo claro
