## MODIFIED Requirements

### Requirement: Persistência da sessão

Uma sessão iniciada SHALL permanecer válida enquanto a pessoa não sair e a
credencial não expirar, sobrevivendo a recarregamentos da página, a abas
novas e a reinícios do servidor de aplicação. A sessão SHALL valer por no
máximo 12 horas a partir da entrada. Na entrada, a pessoa SHALL poder escolher
**Manter conectado** (marcado de início): marcado, a sessão sobrevive a fechar
o navegador; desmarcado, a sessão acaba ao fechar o navegador.

#### Scenario: Recarregar a página

- **WHEN** a pessoa autenticada recarrega a página
- **THEN** ela continua autenticada, sem informar as credenciais de novo

#### Scenario: Reiniciar o servidor de aplicação

- **WHEN** o servidor de aplicação é reiniciado e a pessoa recarrega a página
- **THEN** ela continua autenticada

#### Scenario: Abrir em outra aba

- **WHEN** a pessoa abre o sistema numa aba nova do mesmo navegador
- **THEN** ela continua autenticada

#### Scenario: Fechar e abrir o navegador mantendo conectado

- **GIVEN** a pessoa entrou com "Manter conectado" marcado há menos de 12 horas
- **WHEN** ela fecha o navegador e abre o sistema de novo
- **THEN** ela vai direto para a sua área, sem informar as credenciais

#### Scenario: Fechar o navegador sem manter conectado

- **GIVEN** a pessoa entrou com "Manter conectado" desmarcado
- **WHEN** ela fecha o navegador e abre o sistema de novo
- **THEN** ela não está mais autenticada
- **AND** a tela de entrada não mostra aviso de sessão expirada

#### Scenario: Passaram 12 horas

- **WHEN** a pessoa abre qualquer página mais de 12 horas depois de entrar
- **THEN** a sessão é encerrada sem consultar o backend
- **AND** a tela de entrada informa que a sessão expirou
