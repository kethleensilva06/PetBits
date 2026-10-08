# Design

## Context

Ver `proposal.md` — Why. O que condiciona o desenho:

- `tutor.documento` tem índice **único**, e duplicata em índice único sai como
  **HTTP 500 `Duplicate record detected`** (fato medido) — recusa sem motivo
  legível, que o D10 da change de operação manda evitar.
- `tutor.id_user` é opcional, e o Xano grava **0** quando omitido (fato
  medido 1). É assim que um tutor de balcão fica "sem conta".
- O cadastro público normaliza o documento na pilha (`replace` não existe como
  filtro de entrada) e recusa de forma **genérica**, de propósito: ele é
  público, e distinguir "documento em uso" de "e-mail em uso" confirmaria se
  um CPF alvo é cliente da clínica.
- A spec de animais diz, hoje, que o dono **vem do servidor** e que qualquer
  `id_tutor` do corpo é ignorado, em todos os verbos.

## Goals / Non-Goals

**Goals:**

- Permitir atender quem chega no balcão sem afrouxar nada do que já está
  provado.
- Deixar a armadilha do vínculo **visível**, em vez de deixá-la acontecer em
  silêncio.

**Non-Goals:**

- Ligar tutor de balcão a conta de acesso. Continua pendente, e esta change
  explica melhor por que ela precisa existir.
- Editar e excluir tutor e animal pela clínica.

## Decisions

### D1 — A inversão do dono, e o que a torna segura

Esta é a primeira escrita do sistema em que **o cliente diz de quem é o
dado**. Em todo o resto, o dono vem da credencial, e `id_tutor` no corpo é
descartado.

Não dá para manter a regra aqui: a atendente está cadastrando o animal de
outra pessoa, e a credencial dela não aponta para tutor nenhum — conta de
equipe não tem ficha. Então a regra ganha dois lados:

| caminho | o que se faz com o `id_tutor` do corpo |
|---|---|
| tutor (`POST /pet`) | **ignora** — o dono vem de `tutor_do_token` |
| equipe (`POST /equipe/animais`) | **confere** — tem de existir no banco |

"Conferir" é o que substitui "ignorar", e a conferência é uma consulta ao
banco **antes** da gravação, não uma checagem de formato:

```
precondition ($input.id_tutor > 0) { ... }

db.query tutor {
  where = $db.tutor.id == $input.id_tutor
  output = ["id"]
  return = {type: "single"}
} as $dono

precondition ($dono != null) { error_type = "notfound" ... }

db.add pet { data = { ... id_tutor: $dono.id ... } }
```

**Grava pelo id que a CONSULTA devolveu**, nunca pelo do input — ainda que
sejam iguais por construção. É a mesma forma do `pet_update.xs`, e ela está
aqui para que copiar este arquivo como modelo não perca justamente a parte
que importa.

**O risco que isto cria, e que nenhuma guarda pega:** alguém copia
`equipe_animal_create.xs` como modelo de uma escrita do tutor e leva junto o
`int id_tutor` da declaração de entrada. O endpoint continua compilando,
continua recusando quem não tem sessão, e passa a aceitar que um tutor
cadastre animal no nome de outro. A defesa possível é o comentário no topo
dos dois arquivos, dizendo em qual lado cada um está e por quê. Está escrito
como defesa fraca porque é fraca.

### D2 — A conferência do documento vem antes da gravação

Duplicata em índice único é HTTP 500 com texto em inglês. Deixar o índice
"cuidar disso" entrega à atendente um erro cru onde devia haver "este
documento já está cadastrado".

Então: `db.has tutor` pelo documento **normalizado**, e `precondition` antes
do `db.add`. O índice continua lá — ele é a garantia de último recurso, para
a corrida entre duas atendentes cadastrando a mesma pessoa ao mesmo tempo. A
conferência é pela mensagem; o índice é pela verdade.

### D3 — O documento é normalizado aqui também, pelo mesmo motivo de lá

`123.456.789-01` e `12345678901` são o mesmo documento. Sem normalizar, os
dois criam duas fichas para a mesma pessoa — exatamente o que o índice único
existe para impedir, contornado por pontuação. O cadastro público já corrige
isso na pilha; **o de balcão precisa corrigir igual**, ou as duas portas
divergem e a de balcão vira a fácil.

Isto é a segunda cópia da mesma regra, e a divergência é questão de tempo. A
saída é extrair para função, como `tutor_do_token` já foi. **Esta change não
faz isso**, e fica registrado como dívida — a mesma que o design anterior
anotou sobre a validação de nome e espécie.

### D4 — Aqui a recusa é explícita, e no cadastro público não. Isso é coerente

Parece contradição e não é. O que a recusa genérica do cadastro público
protege é a pergunta *"este CPF é cliente da clínica?"* feita por **qualquer
pessoa, sem credencial**. A recusa de balcão responde a mesma pergunta para
**uma atendente autenticada da própria clínica** — que tem a lista inteira de
tutores a um clique, e para quem esconder isso seria teatro.

A regra que fica: **o que se esconde é função de quem pergunta, não do dado.**

### D5 — A armadilha que esta change cria

Tutor de balcão ocupa o documento e não tem conta. Se a pessoa tentar se
cadastrar depois pelo aplicativo, o cadastro público recusa — documento já
existe — com a mensagem genérica, que de propósito **não explica**. Ela fica
sem acesso e sem saber por quê.

Antes desta change o caso era raro, porque a clínica não criava tutores.
Agora vai ser comum. Não dá para resolver aqui: resolver é ligar a conta nova
à ficha existente, que é a change pendente, e fazê-lo pelo cadastro público
significaria deixar alguém reivindicar uma ficha alheia informando o CPF
dela.

O que esta change faz é **documentar e tornar visível**: a tela de cadastro
de balcão diz, ao criar, que aquela pessoa não terá acesso ao aplicativo
enquanto a clínica não ligar a conta. Avisar na hora é pior que resolver e
muito melhor que descobrir depois.

## Risks / Trade-offs

**Toda a equipe cria tutor e animal, inclusive quem não é da gerência.** Foi o
pedido, e faz sentido — atender quem chega é o trabalho do balcão. Mas
significa que oito contas podem inserir na base de clientes, e a change
anterior já registrou que uma credencial de equipe comprometida é a base
inteira; agora ela também **escreve**.

**Não há como desfazer.** Esta change acrescenta criação e não acrescenta
edição nem exclusão. Um tutor cadastrado com o documento errado fica errado,
e o documento está num índice único — então nem a pessoa certa consegue ser
cadastrada depois. É o argumento mais forte para a edição vir logo.

**A segunda cópia da normalização de documento** (D3), e **o `id_tutor` de
entrada que não pode vazar para o caminho do tutor** (D1), são dívidas com
data marcada: as duas vencem na primeira vez que alguém copiar um arquivo
como modelo do outro.

## Migration Plan

Nada a migrar: as duas tabelas já existem e nenhuma coluna muda.

1. `equipe_tutor_create.xs` e `equipe_animal_create.xs`, os dois com
   `exige_equipe` — não gerência.
2. A guarda de repositório não muda: os dois arquivos entram na convenção
   `equipe_*` e chamam a prova de equipe, que é o que ela já cobra.
3. Reflex: os dois formulários, com a escolha do tutor responsável no de
   animal.
