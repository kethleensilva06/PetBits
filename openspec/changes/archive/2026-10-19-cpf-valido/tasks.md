## 1. Medição

- [x] 1.1 Medir no Xano como percorrer os dígitos de uma string (laço com `substr`/`split`, ou somas desenroladas) antes de escrever a função (D1) — **Medido pela própria prova contra o endpoint** (4.1): o laço `for` com `substr:$i:1|to_int`, `math.add` e `|modulus:11` funcionou de primeira — recusou os inválidos e aceitou o válido, então as somas desenroladas não foram necessárias

## 2. Backend

- [x] 2.1 `functions/pet_bits/cpf_valido.xs` (D1); validar com `validar_xanoscript.mjs`
- [x] 2.2 `tutor_cadastro.xs` e `equipe_tutor_create.xs` chamam a função antes de qualquer `db.has` e gravação, com "CPF inválido. Confira os números." (D2) — no Xano a mensagem sai sem acento, como o resto dos endpoints
- [x] 2.3 Publicar por `scripts/publicar.py`, com `--dry-run` antes — a prévia mostrou exatamente 1 função criada e 2 endpoints alterados; publicado em 19/10. Os avisos de "table does not exist" vêm do push parcial (só os três arquivos), não de erro

## 3. Reflex

- [x] 3.1 `petbits/documentos.py` (`so_digitos`, `cpf_valido`) e `tests/test_documentos.py` — `so_digitos` tira só o que o backend tira (`. - /` e espaço); qualquer outro caractere fica e invalida, como lá
- [x] 3.2 `AuthState.cadastrar` e o cadastro de balcão em `EquipeState` usam `cpf_valido` no lugar da contagem de 11 (D3); o `_so_digitos` do `AuthState`, que só servia a essa contagem, saiu
- [x] 3.3 `scripts/criar_clientes_de_teste.py` usa a função comum — **ajustado:** o script nunca chamava a própria cópia de `cpf_valido`, então ela só foi apagada; o teste de `test_documentos.py` confere que o `cpf_ficticio` do script gera CPFs válidos pela função comum (200 sorteios)

## 4. Verificação

- [x] 4.1 Contra o Xano: CPF com dígito errado e onze iguais recusados com 400 e sem `user` criado; CPF válido passa (cliente de teste criado) — **Feito em 19/10:** `123.456.789-00`, `111.111.111-11` e `1234567890a` no `POST tutor/cadastro` saíram com *CPF invalido. Confira os numeros.*, e entrar com o e-mail de cada tentativa deu credenciais inválidas — nenhuma conta nasceu. CPF válido: `criar_clientes_de_teste.py 1` criou a cliente "Beatriz Rocha (teste)" pelo cadastro público
- [x] 4.2 Balcão no navegador e por chamada direta com token de equipe — **Feito em 19/10:** com token de equipe, `POST equipe/tutores` com `123.456.789-00` e `222.222.222-22` recusados pelo backend com a mesma mensagem; na tela de Tutores, como Carla, o diálogo Novo tutor com `123.456.789-00` mostrou *CPF inválido. Confira os números.* sem enviar
- [x] 4.3 `unittest`, `verificar_equipe.py` e `openspec validate cpf-valido --strict` — 71 testes OK; `verificar_equipe.py` com 20 endpoints de equipe conferidos e nenhuma acusação
