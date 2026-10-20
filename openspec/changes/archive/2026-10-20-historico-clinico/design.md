## Context

O modelo de domínio já descreve o Atendimento (`docs/domain-model.md`): um
animal, um colaborador, data, diagnóstico, tratamento, retorno; nunca é
removido; correção por retificação; o tutor lê, a equipe escreve; pode nascer
de um agendamento ou não. `tables/agendamento.xs` reservou `em_andamento` e
`concluido` "para a change de histórico clínico".

## Decisions

### D1. Tabela `atendimento`

`id_pet` e `id_colaborador` obrigatórios; `id_agendamento` e `retifica`
(id do atendimento corrigido) opcionais; `data_atendimento` (timestamp),
`motivo`, `diagnostico` (obrigatório), `tratamento`, `peso`, `retorno`
(timestamp); `registrado_por` (id da conta do token); `created_at`. Índices
por `id_pet` e `data_atendimento`.

Os vínculos opcionais são gravados como 0 quando ausentes (medido no
projeto para coluna de vínculo), então "sem retificação" é `retifica == 0`.

### D2. Um endpoint de escrita, e só de criação

`POST equipe/atendimentos` cria. Não existe `PATCH` nem `DELETE`: a garantia
de que o histórico não se apaga é estrutural. Retificar é o mesmo `POST` com
`retifica`, que tem de apontar para um atendimento do **mesmo** animal.

Ordem, toda antes de gravar: prova de equipe; animal existe; colaborador
ativo e veterinário/clínico geral; diagnóstico não vazio; data não futura;
retorno não antes da data; retificação do mesmo animal; agendamento (D4).

### D3. Leitura em dois endpoints, um por área

- `GET equipe/animais/{pet_id}/historico`: prova de equipe.
- `GET pet/{pet_id}/historico`: posse provada pelo token, como o `pet/{pet_id}`;
  animal alheio e inexistente dão o mesmo 404.

Os dois devolvem os atendimentos do animal, do mais recente ao mais antigo,
com `colaborador_nome` e `colaborador_funcao` por `join` e `eval` — nunca o
contato (`colaborador`, "Dados de colaborador não são informação de
cliente"). Quem está retificado é calculado na tela, a partir dos `retifica`
da própria lista: o original nunca é tocado.

### D4. Concluir o agendamento

Com `id_agendamento`, o endpoint confere que é do mesmo animal e que não está
cancelado nem concluído, e, na mesma transação do registro, faz o `db.patch`
do agendamento para `concluido`.

### D5. Telas

- Clínica, **Animais**: botão "Histórico" no cartão abre um diálogo com a
  linha do tempo e "Registrar atendimento". O formulário escolhe o
  profissional entre os veterinários e clínicos gerais ativos.
- Clínica, **Agenda**: em agendamento marcado de serviço **clínico**,
  "Registrar atendimento" abre o mesmo formulário com animal, profissional e
  agendamento preenchidos. `equipe/agenda` passa a devolver `id_pet`,
  `id_colaborador` e `servico_categoria` (só para a equipe). Banho e tosa não
  tem o botão: não tem diagnóstico, e a tosadora não registra atendimento —
  achado na verificação, com o botão aparecendo no banho da Juliana.
- Cada atendimento da linha do tempo tem "Retificar", que abre o formulário
  com os dados dele e `retifica` preenchido.
- Casa do tutor: "Histórico" no cartão do animal abre a linha do tempo, só de
  leitura. As requisições são sob demanda, ao abrir — nenhuma a mais no
  carregamento da casa.

## Risks / Trade-offs

- [Registro errado não some] → é a regra; a retificação deixa a correção
  visível e com data.
- [Colaborador sem conta registrando por outro] → `registrado_por` guarda a
  conta que digitou, para diagnóstico.

## Verificação

- `validar_xanoscript.mjs`; `--dry-run` mostrando a tabela nova e os
  endpoints; publicar.
- Contra o Xano: registrar (emergência e pela agenda, com o agendamento
  virando concluído); recusas — diagnóstico vazio, tosador, colaborador
  desligado, data futura, retorno antes, agendamento cancelado, retificação de
  outro animal, conta de tutor; leitura do tutor com e sem posse; nenhum
  campo de contato na resposta.
- Navegador: registrar e retificar pela clínica; ver a linha do tempo na casa
  do tutor.
- `unittest`, `verificar_equipe.py`, `openspec validate historico-clinico --strict`.
