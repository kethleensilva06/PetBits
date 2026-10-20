## 1. Script

- [x] 1.1 `scripts/publicar_no_reflex.py`: permitidos, prévia, duas variáveis, trava, `--publicar`
- [x] 1.2 `tests/test_publicar_no_reflex.py`
- [x] 1.3 README: como publicar

## 2. Verificação

- [x] 2.1 Testes locais passam
- [ ] 2.2 Prévia rodada e revisada; compilação de produção local (`reflex export --frontend-only --no-zip`)
- [ ] 2.3 Publicar só com a autorização da usuária, depois do `reflex login` dela

Medido: a prévia listou só `assets` (33), `petbits` (43), `requirements.txt` e
`rxconfig.py`, e as variáveis XANO_BASE_URL e XANO_AUTH_BASE_URL sem valores.
O `reflex export --backend-only --zip` com as mesmas exclusões, rodado
localmente, gerou 80 arquivos: esses e 2 de `.web/` gerados pelo Reflex;
nenhum `.env`, `contas-de-teste.local.txt`, `xano/` nem o token.

Achado na compilação de produção do frontend (`reflex export --frontend-only`):
o build do Vite termina, mas o prerender da página `/` estoura o tempo
("Prerender: Request failed for /: The operation was aborted due to timeout"),
nesta máquina Windows — a mesma lentidão do Vite que trava o servidor de
desenvolvimento na subida. Rodar o export com o servidor de desenvolvimento
ligado derrubou o site local (os dois usam `.web/`).

Pendente, nesta ordem:
- [x] 2.4 Compilar o frontend com o servidor de desenvolvimento parado. Medido: o
  React Router dá 10 s ao prerender da raiz e só importar o `@radix-ui/themes`
  leva 16,6 s nesta máquina (renderizar leva 0,1 s). Com `--no-ssr` e o limite
  em 60 s no `.web/` (D6), o build passou e gerou o `index.html`
- [ ] 2.5 `reflex login` da usuária, no navegador
- [ ] 2.6 Prévia revisada com ela e `--publicar` só com a autorização dela

Primeira tentativa de publicar, autorizada pela usuária: o `reflex deploy` saiu
com erro e sem mensagem, porque não havia login no Reflex do projeto
(`AppData/Local/reflex/hosting_v1.json` não existe). Nada foi enviado. O script
passou a conferir o login antes e a dizer o comando
(`.venv\Scriptseflex login`).
