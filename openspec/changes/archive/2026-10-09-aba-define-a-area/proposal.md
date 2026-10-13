## Why

Quem é da equipe e também quer usar o sistema como cliente — marcar o banho
do próprio animal, ver a vitrine — entra pela aba **Cliente** e cai no painel
da clínica, porque hoje o destino vem só do papel da conta. A clínica pediu
que a aba Cliente abra a área de cliente.

## What Changes

- Depois que a senha é **aceita**, a aba escolhida decide a área:
  - aba **Cliente** → área de cliente, para qualquer conta;
  - aba **Colaborador** → área da equipe **se** a conta for de equipe; conta
    de tutor continua indo para a área de cliente, porque não tem acesso à da
    equipe.
- A verificação da credencial **não muda**: as duas abas continuam usando o
  mesmo formulário e o mesmo endpoint, e a aba continua sem ser enviada ao
  servidor. Recusas seguem idênticas nas duas abas.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `autenticacao`: o destino depois da entrada passa a considerar a aba, sem
  nunca levar uma conta de tutor à área da equipe.

## Fora do escopo

- Criar ficha de tutor para contas de equipe. Uma conta de equipe sem ficha
  vê a área de cliente vazia, com o aviso que já existe para conta sem
  cadastro de tutor; marcar agendamento exige ter animal, e animal exige
  ficha.
- Trocar de área sem sair (já existe o atalho "Abrir o painel" na área de
  cliente para quem é de equipe).

## Impact

- Código: `petbits/states/auth_state.py` (`entrar`) e `petbits/xano.py`
  (`rota_do_papel` ganha a aba). Nenhum endpoint muda; nenhuma requisição a
  mais.
