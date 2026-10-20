## ADDED Requirements

### Requirement: A tela de agendar guia o tutor

A tela de agendar SHALL mostrar os passos Serviço, Animal, Horário e
Confirmar, com os feitos marcados e o atual destacado, e um resumo do que vai
ser marcado — serviço, duração, preço, animal, dia e horário —, em que o que
falta escolher aparece como "a escolher". O botão de confirmar SHALL ficar no
resumo.

#### Scenario: Começo

- **WHEN** o tutor abre Agendar sem nada escolhido
- **THEN** o passo atual é Serviço e o resumo diz "a escolher" em todas as linhas

#### Scenario: Faltando o horário

- **WHEN** o tutor escolheu o serviço e o animal
- **THEN** Serviço e Animal aparecem feitos, Horário é o atual, e o resumo mostra o serviço, a duração, o preço e o animal

### Requirement: Compromisso na agenda do celular

Depois de marcar, a tela SHALL oferecer um arquivo de calendário (`.ics`) com
o serviço, o animal, o início e o fim do agendamento. O arquivo MUST ser
montado na própria tela, sem requisição ao backend.

#### Scenario: Adicionar à agenda

- **WHEN** a tutora marca uma consulta e toca em "Adicionar à agenda do celular"
- **THEN** recebe um arquivo `.ics` com a consulta, do horário marcado até o fim pela duração do serviço
