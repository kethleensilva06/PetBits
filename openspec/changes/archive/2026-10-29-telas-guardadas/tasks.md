## 1. Guardados

- [x] 1.1 `petbits/guardados.py`: `guardado`, `renova`, `esquecer`, limpeza das vencidas
- [x] 1.2 Leituras e gravações do `xano.py` com os grupos e tempos do design
- [x] 1.3 `_limpar` esquece a credencial
- [x] 1.4 Botão Atualizar no topo das duas áreas

## 2. Verificação

- [x] 2.1 Testes dos guardados; testes locais passam
- [x] 2.2 No navegador (localhost): voltar a uma tela não pede de novo; salvar mostra a mudança na hora; Atualizar busca de novo

Os scripts que usam o `xano.py` (`verificar_ponta_a_ponta.py`,
`criar_clientes_de_teste.py`, `criar_produtos_de_exemplo.py`) desligam o
guardado (`guardados.ligado = False`): a ponta a ponta confere, com duas
contas, o que uma muda pela outra.

Conferido no navegador (localhost), como cliente de teste, contando as
chamadas ao Xano com `PETBITS_MEDIR` (servidor `petbits-medindo`):

- entrar: `POST /entrar`, `GET /auth/me`, `GET /me/tutor`, `GET /pet`,
  `GET /agendamentos`;
- abrir a Agenda pelo menu: só `GET /servicos` (antes, 3 chamadas) — animais e
  agendamentos vieram do guardado;
- voltar a Meus animais: nenhuma chamada;
- Atualizar: `GET /pet` e `GET /agendamentos` de novo;
- salvar o perfil (sem alterar nada) e voltar a ele pelo menu: `PATCH
  /me/tutor` e, na volta, `GET /me/tutor` buscado de novo.

Os 232 testes passam.
