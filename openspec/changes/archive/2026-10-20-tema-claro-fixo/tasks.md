## 1. Tema

- [x] 1.1 `appearance="light"` (D1) — e o script no `<head>` que grava "light", porque o `appearance` sozinho não vencia o "dark" guardado (medido; ver D1)
- [x] 1.2 Tirar `botao_tema` e as três chamadas (D2)
- [x] 1.3 Fundo branco liso em `assets/estilo.css` (D3)

## 2. Verificação

- [x] 2.1 Navegador com o sistema em escuro e `theme: dark` guardado — **Visto em 20/10:** com o navegador em modo escuro e "dark" gravado à mão, `/equipe/servicos` abriu com a classe `light`, fundo `rgb(255, 255, 255)` sem degradê, e o valor guardado virou "light"; nenhum ícone de sol/lua no topo da clínica, e o painel também abriu claro e branco. Nas portas de entrada a retirada foi conferida no código (nenhuma chamada a `botao_tema` sobrou), não na tela: com a sessão aberta, `/entrar` leva ao painel. Antes do script, a mesma página abria escura (fundo `rgb(17, 17, 16)`), o que levou à D1.
      Logo depois de reiniciar o servidor, uma carga deu "Application Error" (`useContext` de null) enquanto o Vite reotimizava as dependências; a carga seguinte veio normal, e nenhuma outra repetiu
- [x] 2.2 `unittest` e `openspec validate tema-claro-fixo --strict`
