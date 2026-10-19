## ADDED Requirements

### Requirement: Foto do animal

O dono SHALL enviar uma foto do animal, que substitui a anterior e aparece no
cartão no lugar da foto genérica da espécie. A posse MUST ser provada pelo
token antes da gravação, como na edição. Só imagens JPG, PNG ou WebP de até
5 MB SHALL ser aceitas.

#### Scenario: Foto do próprio animal

- **WHEN** a tutora envia a foto da Mel pelo diálogo de edição
- **THEN** o cartão da Mel passa a mostrar essa foto

#### Scenario: Animal de outro tutor

- **WHEN** alguém envia foto para o `pet_id` de um animal que não é seu
- **THEN** a resposta é a mesma de animal inexistente e nada é gravado

#### Scenario: Sem foto

- **WHEN** o animal não tem foto enviada
- **THEN** o cartão mostra a foto genérica da espécie
