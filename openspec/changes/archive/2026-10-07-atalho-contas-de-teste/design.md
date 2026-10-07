## Context

O motivo está em proposal.md (Why). O que importa para o desenho:

- A tela de entrada (`petbits/pages/entrar.py`) tem um formulário só, com
  `AuthState.login_email` e `AuthState.login_senha`, e duas abas que **não
  podem** diferir em nada observável (D5 da change `operacao-da-clinica`).
- `contas-de-teste.local.txt` já existe como convenção: está no `.gitignore`
  e `scripts/teste_duas_contas.py` o lê. Formato: uma linha de título que
  começa com maiúscula abre um bloco; dentro dele, linhas `email:` e `senha:`.
- O estado do Reflex mora no backend Python; o navegador só recebe o que é
  variável de estado. Isso é o que permite a senha ficar fora do navegador até
  a escolha.

## Goals / Non-Goals

**Goals:** o mesmo gesto do projeto Mercadinho (`Alt+1`, lista no canto,
clique preenche, `Esc` fecha), sem credencial em arquivo versionado e sem
existir em produção.

**Non-Goals:** entrar com um clique; administrar as contas; valer fora da tela
de entrada.

## Decisions

### D1 — O arquivo é o que já existe, no formato que já existe

As contas saem de `contas-de-teste.local.txt`, e não de uma variável nova no
`.env`. O arquivo já está no `.gitignore` e já é onde o projeto guarda conta de
teste; uma segunda fonte faria as duas divergirem. O título de cada bloco vira
o rótulo da lista, então os blocos `TUTOR` e `EQUIPE` que o script usa
continuam válidos, e blocos a mais (outras contas de equipe) só aparecem na
lista — o script lê o último `EQUIPE`, como já fazia.

*Alternativa descartada:* senhas no código, como no Mercadinho. O `AGENTS.md`
proíbe credencial em código, e o repositório deste projeto é compartilhado.

### D2 — A senha só sai do backend na escolha

A lista enviada ao navegador tem só rótulo e e-mail. O clique manda o
**índice** da conta; o backend relê o arquivo e preenche `login_email` e
`login_senha`. A partir daí a senha está no navegador do mesmo jeito que se a
pessoa a tivesse digitado — é o campo do formulário.

### D3 — Duas travas para produção

1. **Na montagem:** a página só inclui o ouvinte de teclado e a janelinha
   quando `reflex.utils.exec.is_prod_mode()` é falso. Em produção eles não
   existem no pacote compilado.
2. **No manipulador:** abrir a lista e preencher conferem o modo de novo e não
   fazem nada em produção. A primeira trava é de tela; a segunda é a que vale
   se alguém mandar o evento pelo WebSocket na mão — a mesma regra do
   projeto de que esconder não é proteger.

### D4 — Ouvinte de teclado do próprio Reflex

`rx.window_event_listener(on_key_down=...)` recebe a tecla e os
modificadores. É componente do Reflex, então não fere a regra de tecnologia
única de frontend. `Alt+1` alterna; `Esc` fecha. O ouvinte só existe na tela
de entrada e só em desenvolvimento, então as teclas digitadas nas demais telas
não geram evento nenhum.

### D5 — Igual nas duas abas

A lista não lê `AuthState.aba` e o preenchimento não a altera. Uma lista
diferente por aba seria a primeira diferença observável entre elas — em
desenvolvimento, mas o hábito de não criar essa diferença é o que vale.

## Risks / Trade-offs

- [Em desenvolvimento, toda tecla pressionada na tela de entrada vira um
  evento para o backend local] → Só na tela de entrada e só em
  desenvolvimento; não sai da máquina e não toca o Xano.
- [Alguém roda o app em modo de desenvolvimento num servidor exposto, com o
  arquivo presente] → A lista mostraria e-mails e o clique entregaria a senha.
  Mitigação: o arquivo é local de quem desenvolve, e o modo de produção é o
  único previsto para publicação (`reflex run --env prod`). Fica registrado
  no README.
- [O arquivo fica desatualizado em relação ao Xano] → A entrada falha com a
  recusa normal; o arquivo se corrige à mão.

## Migration Plan

Nada a migrar. Quem já tem `contas-de-teste.local.txt` vê as contas dele na
lista sem mudar nada. Para desfazer, basta remover o componente da página.
