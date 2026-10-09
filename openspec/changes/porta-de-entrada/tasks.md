## 1. Código

- [x] 1.1 Página inicial `/boas-vindas` com Sou cliente, Sou da equipe e Criar conta; quem tem sessão é levado à sua área (D4)
- [x] 1.2 `/entrar` (clientes) e `/entrar/equipe` (equipe) com o mesmo formulário e o mesmo `AuthState.entrar`; o `on_load` de cada uma define a aba (D1); sem as abas; "Criar conta" só na de clientes (D2); atalhos Alt+1/Alt+2 nas duas
- [x] 1.3 Visitante sem sessão em `/` vai para `/boas-vindas`; nas outras rotas privadas, para `/entrar`; sessão expirada continua em `/entrar` com aviso (D3)
- [x] 1.5 D5: `rota_do_papel` só pelo papel, sem aba; `AuthState.aba` sai; `PetState` e `AgendaState` mandam conta de equipe para a gerência antes de qualquer requisição; verificar chamando os carregadores com papel de equipe e contando as requisições (`PETBITS_MEDIR`)
- [x] 1.4 Verificar por leitura que as duas páginas chamam o mesmo manipulador e que a aba não entra em requisição

## 2. Verificação

- [x] 2.1 No navegador, sem sessão: abrir `/` mostra a página inicial; os três botões levam às páginas certas; a entrada da equipe não tem "Criar conta"
- [ ] 2.2 No navegador, feito por quem tem a senha: funcionário pela entrada da equipe vai para a gerência; cliente pela entrada de clientes vai para a área de cliente
- [ ] 2.3 `openspec validate --strict` e `verificar_equipe.py` limpos — a spec principal `autenticacao` falha no strict desde o archive da `aba-define-a-area` (requisito "Entrada com e-mail e senha" com mais de 500 caracteres); esta change remove esse requisito, então a conferência vale depois do archive
