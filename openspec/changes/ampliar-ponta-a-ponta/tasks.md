## 1. Script

- [x] 1.1 Cenários novos de agenda (resposta sem nome nem contato, domingo, antes das 8h, fim depois do fechamento, horário no passado), loja (estoque negativo na criação e na alteração, alteração de só o preço, categoria inválida, produto inativo, pedido vazio, entrega no endereço, origem `site`), serviços (categoria inválida) e gerência (equipe comum criando colaborador)
- [x] 1.2 Duas contas de cliente (D1); cancelamento com menos de 24 h pulado com o motivo (D2)

## 2. Teste do script

- [x] 2.1 `tests/test_ponta_a_ponta.py` com o Xano simulado (D3): tudo passa com o backend certo; regra quebrada acusa e sai 1; segunda conta ausente vira pulado

## 3. Verificação

- [ ] 3.1 Rodar de verdade, feito por quem desenvolve
- [ ] 3.2 `openspec validate --strict` (lendo o Totals)
