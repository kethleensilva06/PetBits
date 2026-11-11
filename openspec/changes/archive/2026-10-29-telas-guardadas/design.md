## Context

As telas chamam funções de `petbits/xano.py` (`listar_animais`,
`listar_servicos`, ...) nos seus `on_load`. Cada State tem a sua própria
cópia das listas, e o estado do Reflex é por aba.

## Decisions

### D1. Uma camada só, em volta das leituras do `xano.py`

Guardar em cada State repetiria a regra em dez lugares e não resolveria a casa
e a Agenda buscando os mesmos animais. As funções de leitura ganham o
decorador `guardado(grupo, segundos)`; as de gravação, `renova(*grupos)`.
Nenhuma tela muda: elas continuam chamando as mesmas funções.

### D2. Separado por credencial, na memória do servidor

A chave é o token de quem pede, a função e os argumentos. Dado de uma pessoa
só volta para quem apresentar o mesmo token, que já é o segredo da sessão.
Nada vai para o navegador: o computador da recepção é compartilhado, e o que
se guarda inclui CPF, endereço e observações clínicas. Cada instância do
servidor tem a sua memória; com mais de uma, só há menos acertos.

Devolve-se uma cópia: uma tela que altere a lista recebida não altera o
guardado.

### D3. Gravar apaga o assunto, para quem gravou

`renova` apaga os grupos daquele token depois da gravação, com sucesso ou não
(uma falha pode ter gravado em parte). O que outra pessoa mudou aparece quando
o tempo vence ou com o botão Atualizar — por isso os tempos curtos para o que
a equipe muda (agendamentos, pedidos, loja).

| Grupo | Leitura | Tempo | Apagado por |
|---|---|---|---|
| animais | `listar_animais` | 10 min | criar e alterar animal, foto do animal |
| agendamentos | `listar_agendamentos` | 90 s | marcar e cancelar agendamento |
| catalogo | `listar_servicos_agendaveis` | 10 min | criar e alterar serviço |
| ficha | `minha_ficha` | 30 min | alterar ficha, foto de perfil |
| loja | `produtos_da_loja` | 2 min | fazer e cancelar pedido |
| meus_pedidos | `meus_pedidos` | 60 s | fazer e cancelar pedido |
| colaboradores | `listar_colaboradores` | 10 min | criar e alterar colaborador |
| servicos | `listar_servicos` | 10 min | criar e alterar serviço |
| produtos | `listar_produtos` | 5 min | criar e alterar produto, fotos, balcão, situação do pedido |
| tutores | `listar_tutores_da_clinica` | 5 min | tutor de balcão, alterar tutor |
| animais_clinica | `listar_animais_da_clinica` | 5 min | animal da clínica, tutor de balcão, alterar tutor |
| perfil_equipe | `meu_perfil_de_equipe` | 30 min | alterar perfil, foto de equipe |

### D4. Sair apaga tudo daquela credencial

`AuthState._limpar` — o caminho comum de Sair e da sessão vencida — chama
`guardados.esquecer(token)` antes de apagar o token.

### D5. O botão Atualizar

Fica no topo das duas áreas, ao lado de Sair. Apaga tudo daquela credencial e
recarrega a página, o que roda os `on_load` de novo, agora sem nada guardado.

### D6. A memória não cresce sem fim

A cada gravação no guardado, se houver mais de 500 entradas, as vencidas são
removidas.

## Risks / Trade-offs

- Por até o tempo do grupo, uma pessoa pode ver o que outra mudou com atraso
  (por exemplo, a situação de um agendamento mudada pela equipe). O botão
  Atualizar e os tempos curtos nesses grupos limitam isso.
- O estoque mostrado na loja pode estar até 2 minutos atrasado; o Xano
  continua conferindo o estoque na hora do pedido.
