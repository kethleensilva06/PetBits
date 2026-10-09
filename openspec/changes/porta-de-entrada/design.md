## Context

A entrada hoje é uma página com as abas Cliente/Colaborador sobre um único
formulário (`AuthState.aba`), e a aba só é lida depois do `/auth/me` para
escolher a área (change `aba-define-a-area`).

## Decisions

### D1 — Um formulário só; o destino vem só do papel

O formulário é **o mesmo componente** nas duas páginas, com o mesmo
`AuthState.entrar`, e nada sobre a página é enviado ao servidor. Depois do
`/auth/me`, o destino vem **só do papel** (`rota_do_papel`): equipe vai para a
gerência, o resto para a área de cliente. As garantias da change
`operacao-da-clinica` (D5) valem sem mudança.

*Versão anterior deste D1, desfeita pelo D5:* a página definia
`AuthState.aba`, e a aba escolhia entre gerência e área de cliente para a
conta de equipe. `AuthState.aba` e o parâmetro `aba` de `rota_do_papel`
saíram.

### D2 — A entrada da equipe não oferece "Criar conta"

Diferente da época das abas, agora são duas **páginas** com URLs diferentes,
e o rodapé de cada uma é fixo, igual para qualquer conta. Tirar "Criar conta"
da entrada da equipe é uma diferença entre páginas, não entre contas: não diz
nada sobre o e-mail digitado.

### D3 — O endereço principal sem sessão vai para a página inicial

`carregar_sessao` (o primeiro `on_load` de toda rota privada) passa a mandar
o visitante sem sessão para `/boas-vindas` quando a rota é `/`, e para
`/entrar` nas demais rotas privadas — quem tentou abrir `/agenda` está no
meio de um caminho de cliente. Sessão **expirada** continua indo para
`/entrar` com o aviso.

### D4 — Página inicial sem dados

`/boas-vindas` não tem `on_load` que chame o Xano: só redireciona quem já tem
sessão para a área dele. Não custa requisição ao orçamento.

### D5 — Mudança de rumo: funcionário sempre na gerência

Durante a aplicação, a clínica pediu o contrário do que a change
`aba-define-a-area` tinha feito: funcionário **não** deve usar a área de
cliente. Duas consequências:

1. **Destino:** conta de equipe vai para a gerência por qualquer entrada (D1).
2. **Bloqueio:** `PetState` e `AgendaState`, os carregadores da área de
   cliente, recusam conta de equipe **antes de qualquer requisição** e levam à
   gerência. É o mesmo padrão de guarda por retorno antecipado de
   `EquipeState._token_de_equipe`, ao contrário.

Fica em aberto o que fazer com a change `cadastro-de-cliente-pela-conta`, cujo
motivo era justamente o funcionário usar a área de cliente.

## Risks / Trade-offs

- [Funcionário que também tem animais] → Não usa a área de cliente com a
  conta de equipe (D5). Se precisar, a clínica cria para ele uma conta de
  cliente separada, pelo cadastro público.
- [Conta de equipe com `role` que o sistema não reconhece] → Cai na área de
  cliente como "Sem perfil". Os valores reconhecidos são tratados na change
  `papel-staff`.
