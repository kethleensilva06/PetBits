## ADDED Requirements

### Requirement: O servidor aceita a conexão das páginas do site

O servidor publicado SHALL aceitar a conexão de eventos vinda dos endereços
que servem o site (Reflex Cloud, GitHub Pages e o servidor de
desenvolvimento) e MUST recusar a vinda de qualquer outro endereço.

#### Scenario: Página publicada conecta

- **WHEN** alguém abre o site em `petbits-blue-grass.reflex.run` ou em
  `kethleensilva06.github.io`
- **THEN** a página conecta ao servidor e funciona

#### Scenario: Endereço de fora

- **WHEN** uma página de outro endereço tenta abrir a conexão de eventos
- **THEN** o servidor recusa
