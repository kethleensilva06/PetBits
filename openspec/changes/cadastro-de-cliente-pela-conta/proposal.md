## Why

A clínica quer que os funcionários também possam ser clientes — cadastrar os
próprios animais e marcar banho ou consulta. Desde a change
`aba-define-a-area`, quem é da equipe entra na área de cliente pela aba
Cliente, mas encontra a tela vazia: a conta dele não tem **ficha de tutor**,
e sem ficha não há animal nem agendamento. Hoje a ficha só nasce junto com a
conta, no cadastro público; uma conta que já existe não tem como ganhar uma.

## What Changes

- Na área de cliente, uma conta **sem ficha de tutor** vê "Complete seu
  cadastro de cliente", com CPF (obrigatório), telefone e endereço.
- Enviar cria a ficha **vinculada à própria conta**, com o nome e o e-mail da
  conta. O vínculo vem do token, nunca da requisição.
- O CPF segue as regras que já valem: 11 dígitos depois de tirar a pontuação,
  e único. CPF já usado recebe a **mesma recusa genérica** do cadastro
  público, com o motivo indo só para o registro do servidor.
- Conta que já tem ficha não ganha outra.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `tutores`: uma conta autenticada sem ficha pode criar a própria ficha.

## Fora do escopo

- A equipe criar ficha de cliente **para outra pessoa** (escrita da equipe
  sobre tutor continua não desenhada).
- Editar a ficha depois de criada.
- Criar as fichas dos funcionários em lote: cada um completa a sua, com o
  próprio CPF.

## Impact

- Xano: endpoint novo `POST me/tutor`. Publicação pelo Xano CLI, só ele.
- Reflex: `PetState` passa a perguntar `GET me/tutor` (já existe) **apenas**
  para conta de equipe — uma requisição a mais na abertura da área de cliente
  só para quem pode estar sem ficha; tutor nasce com ficha e não paga nada.
  Formulário na tela inicial do cliente.
