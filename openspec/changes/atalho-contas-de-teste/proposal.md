## Why

Testar o sistema exige entrar e sair com contas de papéis diferentes —
tutor, gerente, veterinário, atendente — dezenas de vezes por sessão de
desenvolvimento. Digitar e-mail e senha toda vez é lento e leva a anotar
senhas em lugares piores do que um arquivo ignorado pelo git. O projeto já
guarda credenciais de teste em `contas-de-teste.local.txt` (lido por
`scripts/teste_duas_contas.py`), mas só os scripts as aproveitam; a tela não.

## What Changes

- Na tela de entrada, **apenas em modo de desenvolvimento**, `Alt+1` abre uma
  janelinha no canto inferior esquerdo com a lista das contas de teste.
  `Alt+1` de novo ou `Esc` fecha.
- Clicar numa conta **preenche** e-mail e senha no formulário e fecha a
  janelinha. Não entra sozinho: a pessoa ainda clica em **Entrar**.
- As contas vêm de `contas-de-teste.local.txt`, o mesmo arquivo local e não
  versionado que os scripts já usam, no mesmo formato. Nenhuma senha entra no
  código, no repositório nem no pacote do navegador.
- Em produção a janelinha não existe: não é montada na página e o
  manipulador recusa o preenchimento.

## Capabilities

### New Capabilities

- `contas-de-teste`: o atalho de desenvolvimento que lista contas de teste na
  tela de entrada e preenche o formulário com uma delas.

### Modified Capabilities

Nenhuma. A verificação de credencial, as abas e o destino por papel
(`autenticacao`) não mudam: o atalho só preenche os mesmos campos que a
pessoa digitaria.

## Fora do escopo

- Entrar automaticamente ao clicar numa conta.
- Criar as contas de teste no Xano. Elas continuam sendo criadas à mão (equipe)
  ou pelo cadastro (tutor); o arquivo só aponta para contas que já existem.
- Atalho nas outras telas (cadastro, área do tutor, área da equipe).
- Unificar o leitor do arquivo com o de `scripts/teste_duas_contas.py`: o
  formato é o mesmo, e o script fica como está.

## Impact

- Código: `petbits/contas_de_teste.py` (novo, leitor do arquivo),
  `petbits/states/auth_state.py` e `petbits/pages/entrar.py`.
- Documentação: `README.md` ganha a explicação do atalho e do arquivo.
- Requisições ao Xano: **nenhuma**. Abrir a lista e preencher o formulário
  acontecem só entre o navegador e o backend Python; o orçamento de 10
  requisições por 20 segundos não é tocado.
- Dependências: nenhuma nova.
