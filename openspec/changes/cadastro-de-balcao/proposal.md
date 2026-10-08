# Proposal

## Why

Metade do atendimento de uma clínica chega sem aviso. A pessoa aparece no
balcão com o animal, e hoje **não há como registrar nenhum dos dois** — as
telas de tutores e de animais são só leitura, e a única forma de um tutor
existir é ele se cadastrar sozinho pelo aplicativo.

Isso foi decisão consciente: a change `operacao-da-clinica` deixou o cadastro
de balcão fora de escopo porque criar tutor envolve o vínculo opcional com
conta de acesso, e porque a **escrita de equipe nunca foi desenhada** — o
padrão "prova + ação" da change dos animais depende de uma cláusula de dono
que, do lado da clínica, não existe. As duas pendências estão registradas por
escrito, e esta change é a que as resolve.

## What Changes

- A equipe **cadastra tutor de balcão**: nome, documento e contato, **sem**
  conta de acesso.
- A equipe **cadastra animal para um tutor existente**, escolhendo de quem é.
- Toda a equipe pode fazer as duas coisas — não só a gerência. Atender quem
  chega é o trabalho do balcão.

### O que torna isto diferente de tudo que já existe

Até agora, **nenhuma escrita do sistema deixava o cliente dizer de quem é o
dado**. No caminho do tutor isso é regra explícita: "o dono do animal vem do
servidor", e um identificador de tutor no corpo é ignorado em todos os verbos.

A escrita de balcão **inverte isso por necessidade**: a atendente está
cadastrando o animal de outra pessoa, então o dono tem de vir da requisição.
A regra não é afrouxada — ela passa a ter dois lados, e o lado novo troca
"ignore o que mandaram" por "**confira** o que mandaram": o tutor informado
precisa existir, e isso é verificado contra o banco antes de qualquer
gravação.

É a diferença entre um sistema que não confia no cliente e um que não confia
no cliente **mas precisa aceitar um apontamento dele**. O risco é o mesmo de
sempre — alguém copiar o endpoint de balcão como modelo do endpoint do tutor
e trazer junto o `id_tutor` de entrada.

### Fora do escopo

- **Ligar um tutor de balcão a uma conta de acesso depois.** Continua sendo
  a pendência que a change anterior registrou, e esta change a torna **mais
  visível**, não menos: ver Impact.
- **Editar e excluir** tutor e animal pela clínica. Esta change acrescenta só
  a criação, que é o que falta para atender quem chega.
- Promover alguém, serviços, agendamento.

## Capabilities

### Modified Capabilities

- `tutores`: a equipe passa a criar tutor de balcão, e a recusa por documento
  repetido passa a poder ser **explícita** nesse caminho — ao contrário do
  cadastro público, onde ela é genérica de propósito.
- `animais`: o dono passa a poder vir da requisição **no caminho da equipe**,
  conferido contra o banco; no caminho do tutor nada muda.

## Impact

**Xano** (`workspace 169225`)

- `POST /equipe/tutores` e `POST /equipe/animais`, os dois exigindo equipe
  (não gerência).

**Aplicação Reflex**

- Formulários de novo tutor e novo animal na área da clínica, com escolha do
  tutor responsável.

**Uma armadilha que esta change cria, e que precisa estar dita**

Um tutor de balcão fica com o documento ocupado e **sem** conta. Se essa
mesma pessoa tentar se cadastrar depois pelo aplicativo, o cadastro público
recusa — o documento já existe — com a mensagem genérica que existe para não
revelar quem é cliente. Resultado: **ela não consegue acesso, e a mensagem
não explica por quê.**

Isso não é defeito desta change: é a pendência de vínculo aparecendo onde dá
para vê-la. Antes, o caso era raro porque a clínica não criava tutores; agora
vai ser comum. Fica registrado como o motivo mais forte até hoje para a change
de vínculo existir.

**Restrições a respeitar**

- O documento continua único, e duplicata em índice único sai como HTTP 500
  cru: a conferência tem de acontecer **antes** da gravação.
- O animal continua precisando de um tutor existente — `id_tutor` zerado ou
  inexistente não pode ser gravado.
- A recusa explícita vale **só** no caminho autenticado da equipe. O cadastro
  público continua genérico.
