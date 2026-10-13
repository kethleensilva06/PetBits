# Design

## Context

Ver `proposal.md` — Why. O que já existe e condiciona o desenho:

- `colaborador.ativo` é `bool ativo?=true`, e o `PATCH` já o aceita como
  entrada, com o comentário dizendo que desligar é alterá-lo.
- O `PATCH` usa o padrão `pick`: só as chaves presentes no **corpo cru** são
  gravadas. É o que faz "campo não mencionado permanece" ser estrutural.
- A lista **não** filtra por `ativo`, e o comentário da tabela justifica isso.
- Guerhart já construiu exatamente este gesto para **produtos**
  (`alternar_ativo`), na change `loja`.
- Manter o quadro é da gerência desde `papeis-e-abas`.

## Decisions

### D1 — Desligar é alterar um campo, não um endpoint novo

Nada precisa subir para o Xano: o `PATCH` já aceita `ativo`. O que falta é a
tela chamar.

Isso parece óbvio e merece estar escrito, porque a tentação é criar
`POST /equipe/colaboradores/{id}/desligar`. Um endpoint por verbo de negócio
multiplica a superfície que a guarda de repositório tem de cobrir e que o
teste de duas contas tem de exercitar — e cada um novo é mais um lugar onde a
prova de gerência pode faltar. Um campo a mais no `PATCH` que já existe não
cria superfície nenhuma.

**A forma do envio importa:** manda-se **só** `{"ativo": false}`. O padrão
`pick` do backend garante que o resto fica como está — e é por isso que
desligar não pode apagar o telefone de ninguém.

### D2 — Quem saiu continua na lista, e isso é requisito

A saída fácil seria filtrar `ativo == true` na listagem. Ela está
explicitamente proibida, e o motivo está no comentário da tabela desde o
primeiro dia: **filtrar some com o único caminho de religar alguém.** Quem
desligou por engano não teria como voltar atrás pela tela.

E some também com a informação de que aquela pessoa existiu — que é o motivo
de desligar existir em vez de excluir: quem saiu da clínica ainda é quem
executou os serviços já registrados, e o sistema vai precisar dizer quem
atendeu.

O cartão de quem está desligado fica **visivelmente diferente** — selo e
opacidade reduzida, como Guerhart fez nos produtos. Mesma linguagem visual
para o mesmo conceito, em duas telas: quem aprender uma entende a outra.

### D3 — Apagar data de entrada depende de uma medição

O formulário monta `dados["data_entrada"]` **só quando o campo tem valor**.
Campo esvaziado vira chave ausente, o `pick` não a toca, e o valor antigo
permanece — a tela diz que salvou e nada mudou.

A correção parece ser "mandar a chave sempre". Mas **o que o Xano grava num
`timestamp` que recebe string vazia nunca foi medido nesta conta**, e esta é
exatamente a família de construto cujo erro é silencioso: pode gravar 0 (que
a tela já lê como "sem data", e aí funciona), pode recusar com 500, ou pode
gravar algo que a leitura interpreta como 1970.

Então **medir antes**, com um colaborador descartável, e só depois decidir a
forma. Se string vazia não servir, as alternativas são `null` ou `0`
explícito — e a que funcionar fica registrada como fato medido, porque a
próxima tela com campo de data opcional vai esbarrar no mesmo.

### D4 — Esconder o botão é conveniência, como sempre

O botão de desligar aparece só para a gerência, pelo mesmo `AuthState.eh_gerencia`
que já esconde "Editar" e "Novo colaborador". E, como sempre: quem forjar o
papel no armazenamento local vê o botão e recebe 403 do `exige_gerencia`, que
é quem recusa de verdade.

Não há endpoint novo, então **a guarda de repositório não muda** — o `PATCH`
que passa a ser usado para desligar já é um dos dois arquivos que ela exige
que chamem a prova de gerência.

## Risks / Trade-offs

**A lista vai crescer para sempre.** Sem exclusão e sem filtro, todo
colaborador que já passou pela clínica fica na tela. Numa clínica pequena
isso é informação; em dez anos é ruído. A saída futura é um filtro
*opcional* — "mostrar desligados", desmarcado por padrão —, que preserva o
caminho de volta sem poluir o dia a dia. Esta change não o faz porque filtro
por padrão é justamente o que o D2 proíbe, e um filtro opcional merece ser
decidido quando a lista doer.

**Desligar não impede nada ainda.** Não há agendamento atribuído a
colaborador, então o estado é informativo. Quando houver, alguém vai precisar
decidir se um colaborador desligado pode receber atendimento novo — e a
resposta provavelmente é não. Fica registrado para a change de agendamento,
que já existe e é de outra pessoa.

## Migration Plan

Nada a migrar: todos os colaboradores existentes já nascem `ativo = true`.

1. Medir o que o Xano faz com `timestamp` recebendo vazio (D3).
2. A tela: botão de desligar/religar e o envio do campo de data.
