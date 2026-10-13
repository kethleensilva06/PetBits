## 1. Código

- [x] 1.1 `rota_do_papel(papel, aba)`: `/equipe` só para equipe + aba colaborador (D2); verificar as quatro combinações (equipe/tutor × cliente/colaborador) e papel vazio
- [x] 1.2 `AuthState.entrar` passa a aba para `rota_do_papel` depois do `/auth/me` (D1); verificar por leitura que a aba não entra em nenhuma requisição

## 2. Percurso

- [ ] 2.1 No navegador: conta de equipe pela aba Cliente vai para a área de cliente; pela aba Colaborador, para o painel — NÃO FEITA: as abas foram substituídas por duas páginas de entrada na change `porta-de-entrada`, e a verificação equivalente é a dela

## 3. Fechamento

- [x] 3.1 `openspec validate --strict` e `verificar_equipe.py` limpos
