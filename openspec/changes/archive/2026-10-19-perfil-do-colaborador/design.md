## Context

A ficha de colaborador (`tables/colaborador.xs`) não tem vínculo com conta: a
spec diz que colaborador é registro, não credencial, e a gerência cadastra
quem nem usa o sistema. As contas de equipe são linhas de `user` com papel
`admin` ou `staff`, conferidas por `PetBits/exige_equipe`. Medido em 19/10:
das oito contas de equipe de teste, sete têm ficha com o mesmo e-mail; a da
Carla não tem nenhuma. A `perfil-e-fotos` deixou o modelo de tela (`/perfil`,
`PerfilState`), a troca de senha (`POST me/senha`, para qualquer conta) e as
medições de upload (extensão em campo próprio, `|in:`, `try_catch`).

## Decisions

### D1. A ficha é achada pelo e-mail da conta

`db.get user` pelo `$auth.id`, e a ficha é a de `colaborador.email` igual ao
e-mail da conta. Nenhum campo novo de vínculo: o e-mail da ficha já é mantido
pela gerência, e é ela quem decide de quem é cada ficha. Duas fichas com o
mesmo e-mail são ambíguas: recusa, em vez de escolher uma.

Alternativa descartada: `id_user` em `colaborador`. Seria o vínculo certo a
longo prazo, mas pede tela para a gerência ligar conta e ficha — escopo de
outra change.

### D2. Os endpoints são `equipe_*` e passam pela prova de equipe

`equipe_meu_perfil_get.xs`, `equipe_meu_perfil_update.xs` e
`equipe_meu_perfil_foto.xs`, nas rotas `equipe/meu-perfil` e
`equipe/meu-perfil/foto`. O prefixo não é estética: `scripts/verificar_equipe.py`
confere que todo `equipe_*.xs` chama a prova e que nenhum outro chama.

### D3. O `PATCH` só conhece nome e telefone

Corpo cru + `pick`, como o `PATCH me/tutor`: `funcao`, `email`,
`data_entrada` e `ativo` nem estão no `input`. Quando `nome` vem, o nome da
conta (`user.name`) muda junto, na mesma transação.

### D4. O mesmo conserto no `PATCH me/tutor`

A saudação vem de `user.name` (`GET auth/me`), e o `PATCH me/tutor` só mudava
a ficha. Passa a mudar também `user.name` quando o nome vem.

### D5. Foto: mesmo endpoint da `perfil-e-fotos`, outra tabela

Coluna `image? foto` em `colaborador`. O upload repete o do tutor, com as
medições de lá. A marca "Powered by Xano" vale aqui também (plano gratuito).

### D6. Tela e cabeçalho

`/equipe/perfil` usa a casca da clínica (`_casca`), com o avatar no topo no
lugar do nome solto, levando ao perfil. `AuthState.usuario_foto` serve às
duas áreas; na entrada de quem é da equipe, a foto vem do `GET
equipe/meu-perfil` (uma requisição a mais, só na entrada).

## Risks / Trade-offs

- [A gerência muda o e-mail da ficha] → a ficha deixa de ser daquela conta e
  o perfil mostra o aviso; é o mesmo controle que a gerência já tem.
- [Nome da conta e da ficha divergem por alteração da gerência] → a gerência
  altera só a ficha; a saudação segue a conta até o próprio colaborador
  salvar o perfil. Aceito.

## Verificação

- `validar_xanoscript.mjs`; `publicar.py --dry-run` mostrando só a coluna nova
  em `colaborador`; publicar.
- Contra o Xano: conta com ficha lê e altera o telefone; `funcao` no corpo
  ignorada; nome vazio recusado; nome alterado aparece em `auth/me` e volta ao
  original; conta sem ficha (Carla) recebe a ficha vazia e a alteração
  recusada; conta de tutor recusada; foto WebP aceita, PDF recusado; o mesmo
  conserto de nome no `PATCH me/tutor`.
- Navegador: avatar no topo da clínica abre `/equipe/perfil`; salvar dados,
  senha atual errada, foto; Carla vê o aviso; claro, escuro e celular.
- `unittest`, `verificar_equipe.py`, `openspec validate perfil-do-colaborador --strict`.
