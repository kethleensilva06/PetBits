## 1. Sessão

- [x] 1.1 `fim_da_sessao` e as variáveis `petbits_expira`, `petbits_lembrar` e o cookie `petbits_aberto`
- [x] 1.2 Validade marcada na entrada e no cadastro; apagada ao sair
- [x] 1.3 Conferência em `_validar_sessao` e em `redirecionar_se_logado`
- [x] 1.4 Caixa "Manter conectado" na tela de entrada

## 2. Verificação

- [x] 2.1 Testes de `fim_da_sessao`; testes locais passam
- [x] 2.2 No navegador (localhost): marcada, a sessão continua numa aba nova; validade vencida leva à entrada com o aviso; desmarcada, sem o cookie, a sessão acaba sem aviso

Conferido no navegador (localhost), como cliente de teste:

- marcada, a entrada gravou a validade de 12 horas, e uma aba nova em `/`, com
  a anterior fechada, levou direto a `/animais`;
- com a validade posta no passado, abrir `/animais` levou a `/entrar` com
  "Sua sessão expirou", e o token foi apagado;
- desmarcada, o cookie `petbits_aberto` ficou marcado e uma aba nova continuou
  dentro; apagado o cookie (como o navegador faz ao fechar), `/` mostrou a
  página inicial, sem aviso e sem token.

Os 218 testes passam.
