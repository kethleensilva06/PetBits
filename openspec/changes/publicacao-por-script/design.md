## Context

O procedimento manual está no "Registro da publicação" da change
`agendamento`. O Xano CLI organiza o workspace em `table/`,
`function/<grupo>/` e `api/<grupo>/<caminho>_<VERBO>.xs`; o repositório usa
`tables/`, `functions/` e `apis/<grupo>/<nome>.xs`.

## Decisions

### D1 — O caminho vem do conteúdo

- `table produto {` → `table/produto.xs`
- `function "PetBits/exige_equipe" {` → `function/pet_bits/exige_equipe.xs`
- `query "equipe/pedidos/{pedido_id}/situacao" verb=POST` com
  `api_group = "PetBits"` → `api/pet_bits/equipe/pedidos/pedido_id/situacao_POST.xs`

O grupo vira minúsculas com `_` (`PetBits` → `pet_bits`, `Quick Start` →
`quick_start`); `{param}` vira `param`. É a regra observada no `workspace
pull`. A `--conferir` comprova a tradução contra o workspace real: um arquivo
publicado que não encontra par indica regra errada ou divergência.

### D2 — Pasta temporária nova a cada execução

O script puxa o workspace numa pasta nova em `%TEMP%` (caminho curto — o
Windows recusa caminhos longos para o Node), copia por cima só os arquivos
pedidos e passa cada um com `-i`. Nunca `--sync`, nunca `--delete`: o que não
foi nomeado não é tocado, nem para atualizar.

### D3 — Publicar exige o pedido e repete a prévia

Sem `--publicar`, o script para depois do `--dry-run`. Com `--publicar`, roda
o `--dry-run` de novo, mostra, e só então publica com `--force` (o CLI pede
confirmação interativa que o terminal não responde).

### D4 — Arquivo igual ao do Xano fica fora (comparação conservadora)

Medido: a prévia do CLI marca `UPDATE` até para arquivo que não mudou, porque
compara texto cru, e a exportação do Xano reescreve o código — tira
comentários e `== true`, quebra listas em várias linhas, move `output` para
depois de `sort`, e acrescenta `guid`. Foi o efeito que quase republicou o
`entrar POST`.

O script compara o código **normalizado** (sem comentários, `guid`,
`description` e linhas em branco) e deixa fora o arquivo igual ao do Xano.
A normalização não desfaz as reescritas de forma, então a comparação é
**conservadora**: pode mostrar como diferente um arquivo que não mudou — e
aí a prévia aparece e quem publica decide —, mas nunca deixa de fora um
arquivo com código diferente.

## Risks / Trade-offs

- [O CLI mudar o formato de pastas] → A `--conferir` acusa na hora: os
  arquivos publicados deixam de achar par.
