## Why

O projeto estava no Reflex 0.9.10.post1, e a versão atual é a 0.11.0. O
ambiente virtual também precisava ser recriado: ele foi criado quando o
projeto estava em `E:\PetBits`, e depois que o disco passou a ser `D:` o
`reflex.exe` parou de funcionar, porque ainda apontava para o Python no
caminho antigo.

## What Changes

- `.venv` recriado em `D:\PetBits`; o antigo foi guardado como
  `.venv-antigo-E` (fora do Git), para ser apagado depois.
- `reflex` e os pacotes `reflex-base` e `reflex-components-*` passam para as
  versões da 0.11.0; `reflex-hosting-cli` passa de 0.2.1 para 0.2.2.
  `requirements.txt` fixa as versões novas.
- pip já estava na versão atual (26.3).

Nenhuma mudança de comportamento: nenhuma spec muda.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

Nenhuma. É mudança de infraestrutura, arquivada com `--skip-specs`.

## Impact

- `requirements.txt`.
- Quem já tem o projeto precisa rodar
  `.venv\Scripts\python.exe -m pip install -r requirements.txt`.
- O site publicado no Reflex Cloud só passa para a 0.11.0 na próxima
  publicação.
