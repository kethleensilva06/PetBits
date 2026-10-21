## Decisions

### D1. `appearance="light"` e um script no `<head>`

`appearance="light"` no `rx.theme` faz o modo de cor padrão do Reflex ser o
claro, e o sistema operacional deixa de mandar.

**Medido:** isso não basta. O componente de tema do Reflex descarta o
`appearance` e segue o modo de cor guardado no navegador, e o ícone de
sol/lua da `tema-claro-escuro` gravou "dark" em quem o usou — com "dark"
guardado, a tela abria escura mesmo com o padrão claro. Um `rx.script` em
`head_components` grava "light" no `<head>`, antes de a página montar e de o
modo guardado ser lido.

### D2. O ícone sai, e a função também

`botao_tema()` e as três chamadas (topo do cliente, topo da clínica, portas
de entrada) saem; não sobra código morto.

### D3. Fundo branco liso

`body > .radix-themes` fica com `var(--color-background)`, branco no claro,
sem os dois degradês. Os cartões já são brancos; o banner da casa mantém o
seu degradê, que é dele e não do fundo.

## Verificação

- Navegador com o sistema em escuro e com `theme: dark` guardado: telas de
  entrada, casa, loja e clínica abrem claras, com fundo branco, e sem o ícone.
- `unittest` e `openspec validate tema-claro-fixo --strict`.
