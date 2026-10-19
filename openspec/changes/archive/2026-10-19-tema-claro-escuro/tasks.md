## 1. Botão

- [x] 1.1 `botao_tema()` em `petbits/visual.py` (D1, D2)
- [x] 1.2 No topo do cliente, no topo da clínica e nas portas de entrada — com o ícone a mais, a faixa do topo do cliente quebrava no celular (o "Sair" descia); os espaços da faixa ficaram menores abaixo de `sm`

## 2. Verificação

- [x] 2.1 Navegador: troca na hora, escolha guardada, celular — **Visto em 19/10:** nas boas-vindas, com o sistema no claro, o sol/lua trocou o tema para escuro na hora (a classe do tema foi de `light` para `dark`) e o Reflex guardou `theme: dark`; recarregando, a página abriu escura com o sistema ainda no claro. Como Ana, no celular, o ícone no topo do cliente trocou de volta para o claro, sem rolagem lateral, e a faixa coube numa linha depois do ajuste. No fim, o navegador de teste voltou a seguir o sistema
- [x] 2.2 `unittest` e `openspec validate tema-claro-escuro --strict`
