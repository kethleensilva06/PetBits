## ADDED Requirements

### Requirement: Publicar o site sem segredo nem conta de teste

A publicação do site no Reflex Cloud SHALL mandar só os arquivos que o site
usa e só as variáveis `XANO_BASE_URL` e `XANO_AUTH_BASE_URL`. O `.env`, o
arquivo de contas de teste, o `XANO_META_TOKEN` e o export do Xano MUST NOT
ser enviados. Por padrão, a publicação SHALL só mostrar o plano, sem enviar
nada.

#### Scenario: Prévia

- **WHEN** alguém roda `scripts/publicar_no_reflex.py` sem `--publicar`
- **THEN** vê os arquivos que iriam e os nomes das variáveis, sem valores, e nada é enviado

#### Scenario: Arquivo proibido no pacote

- **WHEN** o arquivo de contas de teste entraria no pacote
- **THEN** o script para antes de chamar o `reflex deploy`
