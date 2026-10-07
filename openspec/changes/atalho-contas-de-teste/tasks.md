## 1. Leitura do arquivo

- [ ] 1.1 Escrever `petbits/contas_de_teste.py` com `ler()`, que devolve a lista de contas (rótulo, e-mail, senha) de `contas-de-teste.local.txt`, no formato do D1; verificar com um arquivo de exemplo que blocos `TUTOR` e `EQUIPE` e um bloco com outro título são lidos, que bloco sem senha é ignorado, e que arquivo ausente devolve lista vazia sem erro
- [ ] 1.2 Conferir com `git check-ignore` que `contas-de-teste.local.txt` é ignorado

## 2. Estado

- [ ] 2.1 Em `AuthState`: a lista pública (só rótulo e e-mail), o indicador de aberta, e os manipuladores de tecla (`Alt+1` alterna, `Esc` fecha) e de escolha por índice, que preenche `login_email` e `login_senha` e fecha a lista; verificar que a lista pública não tem a chave da senha
- [ ] 2.2 Recusa em produção nos manipuladores (D3, trava 2); verificar chamando-os com `REFLEX_ENV_MODE=prod` e conferindo que nada é preenchido
- [ ] 2.3 Nenhum dos manipuladores lê ou altera `aba`; verificar por leitura (D5)

## 3. Tela

- [ ] 3.1 Em `entrar.py`: `rx.window_event_listener` e a janelinha no canto inferior esquerdo, só fora de produção (D3, trava 1); verificar que a página montada com `REFLEX_ENV_MODE=prod` não contém a janelinha
- [ ] 3.2 Mensagem de arquivo ausente na janelinha; verificar renomeando o arquivo
- [ ] 3.3 Percurso no navegador: `Alt+1` abre, `Esc` fecha, `Alt+1` alterna, clicar numa conta preenche os dois campos e fecha, e a lista é a mesma nas duas abas
- [ ] 3.4 Conferir que abrir a lista e escolher uma conta não fazem requisição ao Xano (gancho `PETBITS_MEDIR` de `petbits/xano.py`)

## 4. Fechamento

- [ ] 4.1 README: o atalho, o formato do arquivo e o aviso de não publicar em modo de desenvolvimento
- [ ] 4.2 Conferir com `git grep` que nenhuma senha do arquivo aparece em arquivo versionado
- [ ] 4.3 Rodar `openspec validate --strict` e `scripts/verificar_equipe.py`; os dois limpos
