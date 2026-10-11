## ADDED Requirements

### Requirement: O repositório só guarda endpoints que estão no ar

Um `.xs` de endpoint que não está publicado no Xano MUST NOT ficar no
repositório: quando um endpoint sai do ar, o arquivo sai na mesma change.

#### Scenario: Endpoint despublicado

- **WHEN** um endpoint é despublicado no Xano
- **THEN** o `.xs` dele é removido do repositório na mesma change, e a
  guarda `verificar_equipe.py` não o acusa mais
