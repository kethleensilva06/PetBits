## Decisions

### D1. O modo de cor do Reflex

`rx.toggle_color_mode` alterna o modo, e o Reflex guarda a escolha no
armazenamento local do navegador. O `rx.theme(appearance="inherit")` já segue
esse modo, então o degradê, os cartões e as fotos acompanham sem nenhuma
regra nova. Sem escolha, o modo é o do sistema.

### D2. Um botão só, em `petbits/visual.py`

`botao_tema()`: ícone de lua no claro e de sol no escuro
(`rx.color_mode_cond`), com `aria_label`. Entra na faixa do topo do cliente e
da clínica, antes do avatar, e fixo no canto superior direito das portas de
entrada, que não têm faixa.

## Verificação

- Navegador: o ícone troca o tema na hora nas duas áreas e nas entradas; a
  escolha continua depois de recarregar, com o sistema no modo oposto; celular
  sem rolagem lateral.
- `unittest` e `openspec validate tema-claro-escuro --strict`.
