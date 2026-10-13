## Why

O arquivo de contas de teste passou a ter a equipe inteira e os clientes, e o
`Alt+1` mostra tudo numa lista só. Para testar o lado do cliente — agenda,
animais — é preciso achar um cliente no meio dos funcionários. A clínica pediu
um atalho próprio para os clientes.

## What Changes

- `Alt+1` passa a listar só as contas de **equipe**.
- `Alt+2` lista só os **clientes**.
- O grupo vem do rótulo do bloco no arquivo: bloco que começa com `TUTOR` ou
  `CLIENTE` é cliente; qualquer outro é equipe. O formato do arquivo não muda.
- Com uma lista aberta, o atalho da outra troca de lista; o da mesma fecha;
  `Esc` fecha qualquer uma.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `contas-de-teste`: dois atalhos, um por grupo.

## Fora do escopo

- Mudar o formato de `contas-de-teste.local.txt`.
- Qualquer coisa fora do modo de desenvolvimento: as duas travas de produção
  continuam valendo para os dois atalhos.

## Impact

- Código: `petbits/contas_de_teste.py` (grupo de cada conta),
  `petbits/states/auth_state.py` (atalhos e escolha por grupo),
  `petbits/pages/entrar.py` (título da janelinha), `README.md`.
- Nenhuma requisição ao Xano.
