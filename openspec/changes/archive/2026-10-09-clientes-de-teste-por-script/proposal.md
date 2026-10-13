## Why

O `Alt+2` lista os clientes de teste, mas a base só tem dois clientes, sem
senha conhecida — as senhas não podem ser recuperadas do Xano. Criar clientes
pela tela, um por um, e copiar e-mail e senha para o arquivo é lento e
convida a errar a senha anotada.

## What Changes

- Script novo `scripts/criar_clientes_de_teste.py N`, rodado por quem
  desenvolve, que cria **N** clientes pelo **cadastro público** do PetBits —
  o mesmo `POST tutor/cadastro` da tela, pela mesma função do cliente HTTP.
- Cada cliente recebe nome fictício, e-mail `@exemplo.com` único, CPF
  fictício com dígitos verificadores válidos, telefone fictício e senha
  gerada que cumpre a regra do sistema.
- Cada cliente criado é **acrescentado** ao `contas-de-teste.local.txt` como
  bloco `TUTOR`, e passa a aparecer no `Alt+2`.
- A senha não aparece na saída do script: ela só vai para o arquivo local,
  que o git ignora.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `contas-de-teste`: um jeito de criar clientes de teste e registrá-los no
  arquivo.

## Fora do escopo

- Criar contas de equipe: elas continuam nascendo à mão no painel do Xano.
- Cadastrar animais para os clientes criados.
- Apagar clientes de teste.

## Impact

- Código: `scripts/criar_clientes_de_teste.py`; `README.md`.
- Xano: nenhum endpoint muda. Cada cliente custa uma requisição ao cadastro
  público; o script pausa entre elas pelo limite de 10 a cada 20 segundos.
- As contas são criadas na base de verdade — quem roda o script decide
  quantas.
