## Decisions

### D1. Uma requisição, em evento próprio

`PetState.carregar_proximo` entra no `on_load` da casa depois de
`PetState.carregar`. Em evento separado, os animais aparecem sem esperar a
agenda, e uma falha na agenda não vira erro na casa: o cartão só não aparece.
A casa passa de 1 para 2 requisições ao abrir, dentro do orçamento de 10 a
cada 20 segundos.

### D2. O que é "próximo"

`petbits/proximo.py`: entre os agendamentos `marcado` ou `em_andamento` que
ainda não terminaram (`fim` depois de agora), o de início mais cedo. Um
atendimento em andamento agora continua sendo o próximo até terminar.
Cancelados e concluídos ficam de fora.

### D3. Dia legível

"Hoje" e "amanhã" pelo dia de São Paulo; depois disso, o dia por extenso
("qua, 22 de outubro"), sempre com a hora.
