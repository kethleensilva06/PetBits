## 1. Script

- [ ] 1.1 `scripts/criar_clientes_de_teste.py N`: geração de nome, e-mail, CPF, telefone e senha (D2); verificar que os CPFs passam no cálculo dos dígitos e as senhas na regra do cadastro
- [ ] 1.2 Cadastro por `xano.cadastrar_tutor` (D1), gravação um por um (D3), pausa (D4), parada sem `.env`; verificar com a requisição simulada: sucesso grava, recusa não grava e continua, saída sem senha, e os gravados aparecem em `do_grupo("clientes")`
- [ ] 1.3 README

## 2. Verificação

- [ ] 2.1 Rodar de verdade, feito por quem desenvolve, e conferir os novos clientes no `Alt+2`
- [ ] 2.2 `openspec validate --strict` e `verificar_equipe.py` limpos
