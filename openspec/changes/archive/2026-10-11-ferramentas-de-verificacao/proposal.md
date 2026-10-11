## Why

Em todas as changes recentes, o gargalo foi o mesmo: "falta verificar com
login". Agendamento, loja, pedidos, balcão e o papel `staff` estão publicados
no Xano sem nunca terem rodado com uma conta logada, e cada verificação
depende de alguém clicar o percurso inteiro. Além disso, os testes que
provaram as regras locais (horários livres, transições de pedido, carrinho,
grupos de contas) foram scripts descartáveis — nada impede que essas regras
quebrem em silêncio. E a lição registrada na change `operacao-da-clinica`
("liste todo endpoint sem `auth = user`") nunca virou conferência automática.

## What Changes

- **Testes locais** em `tests/`, com `unittest` (sem dependência nova): as
  regras de tela que não dependem do Xano — horários livres e prazo de
  cancelamento, transições de pedido, carrinhos da loja e do balcão, leitura
  e grupos das contas de teste, papéis e destinos. Rodam em segundos.
- **Guarda de endpoints públicos**: `scripts/verificar_equipe.py` ganha a
  conferência 4 — todo endpoint sem `auth = "user"` precisa estar numa lista
  de públicos permitidos, com o motivo escrito. Hoje: `entrar` e
  `tutor/cadastro`.
- **Verificação de ponta a ponta** (`scripts/verificar_ponta_a_ponta.py`),
  rodada por quem desenvolve: entra com uma conta de equipe e uma de cliente
  do `contas-de-teste.local.txt` e confere, no Xano de verdade, os cenários
  das specs da agenda, da loja, dos pedidos, do balcão e da separação entre
  equipe e cliente. Resultado por cenário (passou / falhou) e código de saída.

## Capabilities

### New Capabilities

- `verificacao`: as conferências automáticas do projeto — testes locais,
  guarda de endpoints e verificação de ponta a ponta.

### Modified Capabilities

Nenhuma.

## Fora do escopo

- Integração contínua (rodar no GitHub a cada push).
- Testes de tela no navegador.

## Impact

- Código: `tests/`, `scripts/verificar_equipe.py`,
  `scripts/verificar_ponta_a_ponta.py`, `README.md`.
- A guarda passa a **acusar** os cinco `.xs` de autenticação que foram
  despublicados no Xano mas continuam no repositório — é a primeira coisa que
  ela encontra, e não é falso positivo.
- A verificação de ponta a ponta deixa dados de teste no Xano: um produto
  de verificação (desativado no fim), pedidos e um agendamento cancelado.
