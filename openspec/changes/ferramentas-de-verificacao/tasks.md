## 1. Testes locais

- [x] 1.1 `tests/` com agenda, pedidos, carrinhos, contas de teste e papéis (D1); todos passam
- [x] 1.2 Conferir que um teste falha quando a regra muda (mudar o fechamento do sábado num teste temporário)

## 2. Guarda

- [x] 2.1 Conferência 4 em `verificar_equipe.py` com a lista de públicos permitidos (D2); verificar com um arquivo público temporário que ela acusa
- [x] 2.2 Registrar o que ela encontra no repositório de hoje — **Encontrou:** os cinco `.xs` de autenticação despublicados no Xano na change `operacao-da-clinica` (`auth/login`, `auth/signup`, `message/send_welcome_email`, `reset/magic-link-login`, `reset/request-reset-link`); `entrar` e `tutor/cadastro` passam como públicos permitidos

## 3. Ponta a ponta

- [x] 3.1 `scripts/verificar_ponta_a_ponta.py` (D3); verificar com o Xano simulado: contas ausentes param sem requisição, um cenário que falha dá código 1, saída sem senha nem token
- [ ] 3.2 Rodar de verdade, feito por quem desenvolve

## 4. Fechamento

- [x] 4.1 README
- [ ] 4.2 `openspec validate --strict` (lendo o Totals) — a change valida; o total falha só na spec `autenticacao` (herdado)
