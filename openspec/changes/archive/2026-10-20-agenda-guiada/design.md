## Decisions

### D1. Passos derivados do que já está escolhido

`AgendaState.passos` calcula as quatro etapas a partir de `servico_id`,
`pet_id` e `horario_ms`: cada uma feita ou não, e a atual é a primeira não
feita. Nada novo para guardar, e a faixa nunca discorda dos campos.

### D2. Resumo como linhas, não como frase

`AgendaState.linhas_do_resumo` devolve rótulo e valor de Serviço, Duração,
Preço, Animal e Quando; o que não foi escolhido aparece como "a escolher".
A frase `resumo` continua, usada no aviso de sucesso e para habilitar o
Confirmar.

### D3. Coluna de passos e resumo ao lado

Em tela larga, grade `3fr 2fr`: passos à esquerda, resumo à direita com
`position: sticky`, para ficar à vista enquanto se rola o calendário. No
celular, uma coluna, com o resumo no fim.

### D4. `.ics` montado na tela

`petbits/calendario.py` monta um VCALENDAR com um VEVENT (início e fim em
UTC, título, descrição e local "Clínica PetBits"), com quebra de linha CRLF
e texto escapado, como manda a RFC 5545. Ao marcar, o State guarda o último
compromisso (título, início e fim pela duração do serviço); o botão chama
`rx.download` com o texto. Sem requisição, sem dado de outra pessoa: só o
que o tutor acabou de marcar.
