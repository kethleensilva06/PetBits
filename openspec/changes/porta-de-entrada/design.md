## Context

A entrada hoje é uma página com as abas Cliente/Colaborador sobre um único
formulário (`AuthState.aba`), e a aba só é lida depois do `/auth/me` para
escolher a área (change `aba-define-a-area`).

## Decisions

### D1 — A página faz o papel da aba, e o resto não muda

`AuthState.aba` continua existindo, mas quem a define é o `on_load` de cada
página de entrada (`cliente` em `/entrar`, `colaborador` em
`/entrar/equipe`), não um controle na tela. O formulário é **o mesmo
componente** nas duas páginas, com o mesmo `AuthState.entrar`; a aba segue sem
entrar em requisição nenhuma e só decide o destino depois da aceitação. Assim
as garantias da change `operacao-da-clinica` (D5) e da `aba-define-a-area`
valem sem reescrever nada delas.

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

## Risks / Trade-offs

- [Links antigos para `/entrar` usados por funcionários] → `/entrar` leva à
  área de cliente; a entrada de clientes tem o link "É da equipe? Entrada da
  equipe".
