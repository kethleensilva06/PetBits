## Why

A usuária quer o site no ar. O GitHub Pages só serve arquivos estáticos, e o
PetBits precisa do servidor Python do Reflex ligado (o estado de cada tela e
as chamadas ao Xano moram nele). O Reflex Cloud roda as duas partes.

O `reflex deploy` empacota a pasta inteira do projeto, deixando de fora só o
que começa com ponto. Isso tira o `.env`, mas mandaria
`contas-de-teste.local.txt` (senhas das contas de teste), o export do Xano em
`xano/` e pastas que não são do site. E `--envfile .env` mandaria também o
`XANO_META_TOKEN`, que publica no Xano e não é do site.

## What Changes

- `scripts/publicar_no_reflex.py`, no mesmo jeito do `publicar.py`:
  - por padrão só mostra o plano: os arquivos que iriam, contados por pasta,
    e os NOMES das variáveis, sem os valores;
  - manda só o que o site usa: `petbits/`, `assets/`, `rxconfig.py` e
    `requirements.txt`; todo o resto do projeto vai em `--exclude-from-backend`;
  - das variáveis, só `XANO_BASE_URL` e `XANO_AUTH_BASE_URL`, lidas do `.env`;
  - recusa publicar se algum arquivo proibido estiver no pacote;
  - com `--publicar`, roda `reflex deploy --no-interactive`.
- Testes que garantem que `.env`, `contas-de-teste.local.txt` e o
  `XANO_META_TOKEN` nunca entram.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `publicacao`: publicar o site no Reflex Cloud sem segredo nem conta de teste.

## Fora do escopo

- Criar a conta no Reflex Cloud e entrar nela (`reflex login`): é a usuária
  quem faz, no navegador.
- Domínio próprio.

## Impact

- Código: `scripts/publicar_no_reflex.py` (novo); `tests/test_publicar_no_reflex.py`;
  `README.md` (como publicar).
