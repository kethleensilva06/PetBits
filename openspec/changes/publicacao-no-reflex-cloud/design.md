## Decisions

### D1. Lista do que vai, e não do que não vai

O `reflex deploy` decide pelo contrário (vai tudo, menos o oculto). O script
inverte: `PERMITIDOS = ("petbits", "assets", "rxconfig.py", "requirements.txt")`
e todo o resto da raiz entra em `--exclude-from-backend`. Arquivo novo na raiz
não sobe sem alguém pôr na lista.

### D2. A prévia imita o empacotador

`arquivos_do_pacote()` percorre a pasta com as mesmas regras de
`reflex/utils/build.py` (pula oculto, `__pycache__`, venv e `.db`) e com as
exclusões do D1, e conta por pasta. É o que a usuária revisa antes de
autorizar.

### D3. Duas variáveis, nomeadas

O `.env` é lido, mas só `XANO_BASE_URL` e `XANO_AUTH_BASE_URL` saem dele, em
`--env`. Nunca `--envfile`: ele mandaria o `XANO_META_TOKEN`. Os valores não
são impressos.

### D4. Trava

Antes de chamar o `reflex deploy`, o script confere de novo: se `.env`,
`contas-de-teste.local.txt` ou algo de `xano/` estiver no pacote, ou se
alguma variável além das duas estiver no comando, ele para.

### D5. Produção sem atalho de teste

O atalho Alt+1/Alt+2 já não é montado em produção, e os manipuladores
recusam (`is_prod_mode`). Com o arquivo de contas fora do pacote, nem haveria
o que ler.
