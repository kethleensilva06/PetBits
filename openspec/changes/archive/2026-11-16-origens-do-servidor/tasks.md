## 1. Configuração

- [x] 1.1 `cors_allowed_origins` em `rxconfig.py` com o Reflex Cloud, o GitHub Pages, `localhost:3000` e `127.0.0.1:3000`

## 2. Verificação

- [x] 2.1 Testes passando e o site local abrindo — **2026-11-16:** 236 testes, OK
- [x] 2.2 Publicar no Reflex Cloud e medir o handshake de `/_event`: 101 com `Origin` do Reflex Cloud e do GitHub Pages, 403 com um endereço de fora — **2026-11-16:** reflex.run → 101, github.io → 101, endereço de fora → 403
- [x] 2.3 Abrir o site publicado no navegador e ver a página conectada — **2026-11-16:** numa aba nova, `/animais` sem sessão foi levado a `/` pelo servidor, sem erro no console e sem o aviso "Cannot connect"
- [x] 2.4 `openspec validate --strict` (lendo o Totals) — **2026-11-16:** ver o commit
