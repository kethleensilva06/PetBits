## Context

A change `porta-de-entrada` criou a página inicial pública em `/boas-vindas` e
as entradas em `/entrar` (clientes) e `/entrar/equipe`, deixando `/` como a
casa do cliente logado. Quem pediu a mudança quer a página de boas-vindas no
endereço principal e a entrada de clientes numa página própria.

## Decisions

### D1 — Mapa de endereços

| Endereço | Antes | Depois |
| --- | --- | --- |
| `/` | área do cliente | boas-vindas |
| `/inicio` | — | área do cliente |
| `/entrar/cliente` | — | entrada de clientes |
| `/entrar/equipe` | entrada da equipe | sem mudança |
| `/entrar` | entrada de clientes | leva a `/entrar/cliente` |
| `/boas-vindas` | boas-vindas | leva a `/` |

`/inicio` foi escolhido por ser curto e por já ser o nome do arquivo da tela
(`pages/inicio.py`).

### D2 — Endereços antigos viram redirecionamento

`/entrar` e `/boas-vindas` continuam registrados, com uma página vazia cujo
`on_load` redireciona. Removê-los deixaria um 404 para quem guardou o link, e
mantê-los como cópia das páginas novas deixaria dois endereços para a mesma
porta.

### D3 — Para onde vai quem não tem sessão

- Abrir `/inicio` sem sessão leva a `/` (a página pública), como hoje `/`
  levava a `/boas-vindas`.
- As demais rotas privadas, sessão expirada e "Sair" levam à entrada de
  clientes, agora `/entrar/cliente`.
- Uma conta de equipe que abre `/inicio`, `/agenda`, `/loja` ou `/pedidos`
  continua indo para a gerência; uma sessão sem papel de equipe que abre a área
  da clínica vai para `/inicio`.

## Risks / Trade-offs

- [Link interno esquecido apontando para `/`] → Ele levaria à página pública,
  que redireciona quem tem sessão para a área do papel: o efeito é um salto a
  mais, não uma tela errada. A busca pelos links está nas tarefas.
