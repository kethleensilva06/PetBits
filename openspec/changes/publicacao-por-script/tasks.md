## 1. Script

- [x] 1.1 Tradução do caminho pelo conteúdo (D1), com testes em `tests/` para tabela, função, endpoint simples e endpoint com parâmetro
- [x] 1.2 Prévia (D2) e publicação só com `--publicar` (D3); validação pelo parser antes de tudo
- [x] 1.3 `--conferir`: rodar contra o workspace real e registrar o resultado — **Resultado:** 56 documentos pareados; no repositório e não no Xano, os cinco `.xs` de autenticação despublicados; no Xano e não neste repositório, `equipe/animais POST`, `equipe/tutores POST` e `PetBits/exige_gerencia`, que estão na `main` (change `papeis-e-abas`, da Kethleen) e não na `Guerhart`

## 2. Verificação

- [x] 2.1 Prévia de arquivos já publicados e sem mudança mostra que nada mudaria — **A premissa era falsa:** o CLI marca `UPDATE` para arquivo sem mudança (D4). O script passou a deixar fora o que é igual depois de normalizar; a comparação é conservadora
- [x] 2.2 README; o registro da change `agendamento` aponta para o script
- [ ] 2.3 `openspec validate --strict` (lendo o Totals)
