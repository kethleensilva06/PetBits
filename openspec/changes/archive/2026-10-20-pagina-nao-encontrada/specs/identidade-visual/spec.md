## ADDED Requirements

### Requirement: Página não encontrada

Um endereço que não existe SHALL mostrar uma página do PetBits, em português,
com a marca, a mensagem de que a página não foi encontrada e os caminhos Ir ao
início e Voltar. A página MUST NOT fazer requisição ao Xano.

#### Scenario: Link velho

- **WHEN** alguém abre `/pagina-que-nao-existe`
- **THEN** vê "Página não encontrada", com a marca e os botões Ir ao início e Voltar

#### Scenario: Ir ao início

- **WHEN** a pessoa clica em Ir ao início
- **THEN** vai para `/`, que a leva à sua área ou à página inicial pública
