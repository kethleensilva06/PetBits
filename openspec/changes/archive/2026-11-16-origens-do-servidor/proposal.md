## Why

Depois de publicar o site com o Reflex 0.11.0 (change `atualizar-reflex`), a
página em `petbits-blue-grass.reflex.run` mostrava "Cannot connect to server".
O servidor estava no ar (`/ping` e `/_health` respondiam 200), mas recusava a
conexão de eventos (`/_event`) com 403 quando ela vinha de outro endereço.
Medido em 2026-11-16: sem `Origin`, 101; com `Origin` do Reflex Cloud, do
GitHub Pages ou de `localhost:3000`, 403.

O Reflex 0.11 passou a aceitar, em produção, só o próprio endereço do
servidor. No PetBits, o servidor fica em `*.fly.dev` e as páginas são
servidas por `petbits-blue-grass.reflex.run` e por
`kethleensilva06.github.io`, então nenhuma delas conectava.

## What Changes

- `rxconfig.py` lista em `cors_allowed_origins` os endereços que servem o
  site: o Reflex Cloud, o GitHub Pages e o servidor de desenvolvimento
  (`localhost:3000` e `127.0.0.1:3000`).
- O site é publicado de novo no Reflex Cloud.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `publicacao`: o servidor aceita a conexão das páginas do site, e só delas.

## Impact

- `rxconfig.py`.
- Um endereço novo para o site precisa entrar na lista antes de publicar.
