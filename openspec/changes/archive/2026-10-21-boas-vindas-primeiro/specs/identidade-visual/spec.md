## MODIFIED Requirements

### Requirement: Marca do PetBits

A marca (selo com patinha e o nome PetBits) SHALL aparecer no topo das portas
de entrada, da área do cliente e da área da clínica. Nas áreas logadas, a
marca SHALL levar à tela inicial da área.

#### Scenario: Marca na área do cliente

- **WHEN** o tutor clica na marca em qualquer tela da área do cliente
- **THEN** vai para a casa (`/animais`)

#### Scenario: Marca na área da clínica

- **WHEN** alguém da equipe clica na marca em qualquer tela da clínica
- **THEN** vai para o painel (`/equipe`)
