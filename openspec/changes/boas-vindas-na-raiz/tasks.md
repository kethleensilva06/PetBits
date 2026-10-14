## 1. Rotas

- [ ] 1.1 `petbits.py`: boas-vindas em `/`, área do cliente em `/inicio`, entrada de clientes em `/entrar/cliente`; `/entrar` e `/boas-vindas` só redirecionam (D1, D2)
- [ ] 1.2 `xano.ROTA_TUTOR = "/inicio"`; verificar com o teste de destino por papel

## 2. Sessão e links

- [ ] 2.1 Redirecionamentos de sessão (D3): sem sessão em `/inicio` → `/`; demais rotas privadas, expirada e "Sair" → `/entrar/cliente`; sessão de cliente na área da clínica → `/inicio`; verificar com os testes de sessão
- [ ] 2.2 Links internos (logo, "Meus animais", "Cadastrar", "Voltar ao início", "Entrar", "Entrada de clientes") apontando para os endereços novos; verificar com uma busca que nenhum link aponta para `/entrar` ou `/boas-vindas`
- [ ] 2.3 `README.md` com os endereços novos

## 3. Verificação

- [ ] 3.1 Testes passando e as páginas compilando
- [ ] 3.2 No navegador, sem sessão: `/` mostra as boas-vindas, "Entrar" leva a `/entrar/cliente`, `/entrar` e `/boas-vindas` redirecionam, `/inicio` leva a `/`
- [ ] 3.3 No navegador, com conta de cliente (quem desenvolve): entrar por `/entrar/cliente` cai em `/inicio`; abrir `/` com sessão leva a `/inicio`
- [ ] 3.4 `openspec validate --strict` (lendo o Totals) e `verificar_equipe.py`
