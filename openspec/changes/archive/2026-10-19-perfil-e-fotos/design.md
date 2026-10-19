## Context

`GET me/tutor` devolve a ficha do token. `PATCH pet/{pet_id}` é o modelo de
escrita com posse: consulta-prova com `join` e `where` por id e dono, com
lock, dentro de transação, e `db.patch` pelo id da prova; e `pick` pelo corpo
cru para não apagar campo ausente. `entrar.xs` usa `security.check_password`.
A tabela `user` é do template (login, senha, event log) e não muda.

## Goals / Non-Goals

**Goals:** o tutor cuida dos próprios dados e das fotos, sem passar pela
clínica, com as mesmas garantias de dono que o resto do grupo.

**Non-Goals:** mudar CPF/e-mail, recuperação de senha, fotos pela equipe.

## Decisions

### D1. `image? foto` em `tutor` e em `pet`, nunca em `user`

Coluna opcional nas duas tabelas do domínio. `user` fica intocada pelo
mesmo motivo de sempre (`tables/tutor.xs`): um push errado ali derruba a
entrada de todo mundo. Antes do push, `--dry-run` para conferir que a única
mudança é a coluna nova.

### D2. Upload em dois saltos: navegador → Reflex → Xano

O `rx.upload` entrega o arquivo ao backend do Reflex; o State confere tipo e
tamanho (aviso rápido) e manda ao Xano em `multipart` com o token da sessão.
O Xano é quem decide: `storage.create_image` e depois confere `mime` e
`size` do que recebeu; fora da regra, recusa sem gravar na ficha.

O arquivo recusado depois do `storage.create_image` fica no armazenamento
sem ficha que aponte para ele. Aceito: é pequeno, raro e não é exposto.
Medir se o Xano recusa tipo errado já no `file? image` de entrada; se
recusar, a conferência de `mime` vira segunda linha de defesa.

### D3. Acesso `public` no armazenamento

Imagens `private` exigiriam URL assinada a cada exibição, ou seja, uma
requisição a mais por cartão — e a instância tem 10 a cada 20 s. As URLs
públicas do Xano têm caminho aleatório e não são listáveis. Risco aceito e
registrado: quem tiver a URL de uma foto vê a foto; a URL só chega a quem já
vê o cartão (o dono e a equipe).

### D4. `PATCH me/tutor` copia o modelo do `pet/{pet_id}`

Corpo cru + `pick` só de `nome`, `telefone`, `endereco` — `documento` e
`email` nem estão no `input`, então não há caminho para eles. Nome vazio
recusado. Ficha encontrada por `id_user == $auth.id`; sem ficha, `accessdenied`.

### D5. `POST me/senha` confere a atual no servidor

`db.get user` pelo `$auth.id`, `security.check_password` da atual, e
`db.edit` da nova — a coluna `password` já aplica `min:8|minAlpha:1|minDigit:1`.
A nova repetida é conferida na tela e no endpoint. Registrar no `event_log`
(`senha_trocada`), como o fluxo do template faz.

### D6. Avatar no cabeçalho leva a `/perfil`

`topo_do_cliente` ganha à direita o avatar (`rx.avatar` com a foto ou as
iniciais), que é link para `/perfil`. Buscar a ficha em toda tela custaria
uma requisição a mais por clique no menu; então o `AuthState` guarda a URL
da foto quando a ficha é lida (na entrada e no perfil) e a mantém no
armazenamento local, como já faz com o nome.

### D7. Foto do animal no diálogo de edição

O diálogo de edição ganha "Trocar foto". O cartão usa `foto.url` quando
existe e a foto genérica da espécie quando não. A lista `GET pets` passa a
incluir `foto` no `output`.

## Risks / Trade-offs

- [Foto pesada demora] → limite de 5 MB e aviso na tela antes de enviar.
- [Ordem com `fotos-realistas`] → as duas mexem em `inicio.py`; esta é
  aplicada depois, e o "sem foto" usa o que aquela deixar.

## Verificação

- `validar_xanoscript.mjs`; publicar com `--dry-run`, conferindo que as
  tabelas só ganham a coluna.
- Contra o Xano, com a conta de teste: alterar telefone e conferir por
  `GET me/tutor`; nome vazio recusado; `documento` no corpo ignorado;
  senha atual errada recusada; troca certa e entrada com a nova (e voltar à
  senha do arquivo de contas de teste); foto válida aceita, PDF e > 5 MB
  recusados; foto para `pet_id` de outro tutor recusada como inexistente
  (`scripts/teste_duas_contas.py`).
- Navegador: tocar no avatar, editar, trocar senha, enviar foto do tutor e de
  um animal; claro, escuro e celular.
- `unittest`, `verificar_equipe.py`, `openspec validate perfil-e-fotos --strict`.
