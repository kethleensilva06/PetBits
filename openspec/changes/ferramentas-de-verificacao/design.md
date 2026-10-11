## Context

- As regras de tela estão em módulos puros (`petbits/agenda.py`,
  `petbits/pedidos.py`, `petbits/contas_de_teste.py`, `petbits/xano.py` nos
  papéis) e em manipuladores de State que dá para chamar com um objeto simples
  no lugar do `self`, como os testes desta sessão já fizeram.
- O AGENTS.md pede não acrescentar dependência sem necessidade.

## Decisions

### D1 — `unittest`, da biblioteca padrão

Sem `pytest`: nada a instalar, nada a acrescentar ao `requirements.txt`. Os
testes de State chamam o manipulador por `.fn` com um `SimpleNamespace` —
testam a regra, não o Reflex.

### D2 — Públicos permitidos com motivo, no próprio script

A lista fica em `scripts/verificar_equipe.py`, com o motivo de cada um ao
lado. Um endpoint público novo obriga quem o cria a escrever por que ele é
público — é a pergunta "que pergunta este endpoint responde a quem não tem
credencial?" virando campo obrigatório.

### D3 — A ponta a ponta usa o cliente HTTP do app

`scripts/verificar_ponta_a_ponta.py` chama as funções de `petbits/xano.py`,
as mesmas das telas. Pausa de 2,2 s entre requisições pelo limite de 10 a
cada 20 s. Cria só o que precisa e com nome reconhecível ("Produto de
verificação …"); desativa o produto no fim. Agenda: usa o primeiro animal do
cliente, um serviço de banho e tosa e um dia útil a pelo menos dois dias,
para o cancelamento caber no prazo de 24 h. Pulos são explícitos ("pulado:
cliente sem animal") e não contam como falha.

## Risks / Trade-offs

- [A ponta a ponta deixa dados no Xano] → São reconhecíveis pelo nome e pela
  data; o produto fica desativado e o agendamento, cancelado.
- [Não testa a tela] → O que ela testa é o contrato com o backend, onde moram
  as regras que protegem; a tela continua sendo conferida no navegador.
