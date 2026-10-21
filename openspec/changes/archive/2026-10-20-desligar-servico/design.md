## Decisions

### D1. `bool ativo?=true`

A coluna nasce com padrão `true`, como em `colaborador` e `produto`. As
leituras usam `ativo != false`.

**Medido em 20/10, e corrigido:** a primeira versão publicou `bool ativo?`
sem padrão, contando que os serviços antigos ficariam com a coluna vazia e
valeriam como ativos. O Xano gravou `false` em todos eles — o mesmo que o
projeto já tinha medido para coluna de vínculo numérica —, e o catálogo do
tutor ficou vazio por cerca de 15 minutos, entre a publicação e a prova que
achou o defeito. Os três serviços com categoria foram religados à mão, e a
coluna passou a ter padrão `true`; republicar o padrão não mexeu nos valores
gravados. As duas "Sonda" ficaram desligadas por esse mesmo efeito, que é o
estado que esta change queria para elas.

### D2. Onde o inativo é recusado

- `servico_list_tutor.xs`: o `where` ganha `ativo != false`.
- `agendamento_create.xs` e `agenda_ocupacao.xs`: o `output` do serviço
  ganha `ativo`, e a mesma recusa de "não está disponível" do serviço sem
  categoria vale para o inativo.
- `equipe_servico_list.xs` e `equipe_servico_get.xs`: `ativo` no `output`,
  para a tela mostrar o selo.
- `equipe_servico_update.xs`: `bool ativo?` no `input`; o `pick` pelo corpo
  cru já existe, então só o que veio é gravado.

### D3. Tela como a de produtos

Selo "Inativo" e botão Desativar/Ativar no cartão, chamando o mesmo `PATCH`.

### D4. Sondas de escrita com nome só de espaços

Nos quatro endpoints de escrita da lista do script, a prova de equipe (ou de
gerência) vem antes da validação do nome — conferido nos `.xs`. Com
`{"nome": "   "}`, a entrada é aceita, o `trim` esvazia o nome, a prova roda
(o cliente recebe 403) e a validação recusa a equipe (400) antes de gravar. O
critério do script (equipe ≠ 403) não muda.

**Medido:** com `{"nome": ""}` o `POST` dava 400 também para o cliente — o Xano
confere a entrada antes da pilha, e "" num campo obrigatório é recusado ali —,
e a sonda deixava de provar a recusa de equipe. É a mesma regra que
`equipe_tutor_create.xs` já registra sobre `filters=trim`.

Um teste local lê a lista do script e confere que toda sonda de
`POST`/`PATCH` tem nome só de espaços.

## Verificação

- `validar_xanoscript.mjs`; `--dry-run` mostrando só a coluna nova em
  `servico`; publicar.
- Contra o Xano: desativar um serviço com categoria e conferir que some da
  lista do tutor e que agendar dá a recusa; reativar e conferir que volta;
  rodar o `teste_duas_contas.py` e comparar as listas de serviços e
  colaboradores antes e depois.
- Navegador: desativar e reativar pela tela; desativar as duas "Sonda".
- `unittest`, `verificar_equipe.py`, `openspec validate desligar-servico --strict`.
