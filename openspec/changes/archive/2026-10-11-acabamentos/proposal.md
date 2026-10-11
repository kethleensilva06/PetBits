## Why

O sistema cresceu rápido nas últimas changes e ficaram duplicações e
pequenos defeitos que ninguém pediu para corrigir, mas que vão morder:

- a guarda de sessão da área de cliente (`_token` e `_encerrar`) está
  copiada em três States, e a da equipe numa quarta forma — a próxima
  correção numa não chega nas outras;
- os rótulos de tela (categorias, situações, entregas, pagamentos, funções)
  estão espalhados por quatro arquivos, com duas cópias da lista de funções;
- a regra "categoria do serviço → funções que atendem" está escrita duas
  vezes no backend, em `agenda/ocupacao` e em `POST agendamentos`;
- o cabeçalho cumprimenta "Olá, Dr.!" quando o nome começa com título;
- o Reflex avisa a cada compilação que o plugin do Radix está implícito;
- `.vscode/launch.json` abre o navegador na porta 8080, e o app roda na 3000.

## What Changes

- `petbits/states/sessao.py` ganha a guarda de cliente e o encerramento num
  lugar só, usados por `PetState`, `AgendaState` e `LojaState`; `EquipeState`
  usa o mesmo encerramento.
- `petbits/rotulos.py` reúne os rótulos de tela; os States importam dele.
- Função `PetBits/funcoes_da_categoria` no Xano, usada pelos dois endpoints da
  agenda; os dois são republicados por `scripts/publicar.py`, sem mudança de
  comportamento.
- A saudação usa o primeiro nome que não é título (Dr., Dra., Sr., Sra.).
- `rxconfig.py` declara o `RadixThemesPlugin`.
- `.vscode/launch.json` aponta para a porta 3000.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `autenticacao`: a saudação pelo nome.

## Fora do escopo

- Mudar qualquer regra de negócio: tudo aqui é forma, exceto a saudação.

## Impact

- Código: `petbits/states/*`, `petbits/rotulos.py`, `petbits/agenda.py`,
  `rxconfig.py`, `.vscode/launch.json`; Xano: função nova e dois endpoints
  da agenda republicados.
