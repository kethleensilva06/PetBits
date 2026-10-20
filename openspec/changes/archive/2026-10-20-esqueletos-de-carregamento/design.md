## Decisions

### D1. `rx.skeleton` do Radix, em blocos no formato do conteúdo

O Radix já traz o pulso e a cor do tema. `petbits/esqueletos.py` monta os
formatos: `cartoes(n, colunas)` (grade de cartões com imagem e linhas),
`linhas(n)` (lista de cartões baixos), `perfil()` e `fichas(n)` (os botões
de horário). A grade usa as mesmas colunas da tela real, para o conteúdo
entrar no mesmo lugar.

### D2. Os quatro estados continuam disjuntos

O esqueleto ocupa só o lugar do "carregando": com dado, vazio ou erro, ele
não aparece. Os `rx.cond` existentes ficam; troca-se só o ramo.

### D3. Acessível

Cada esqueleto tem `role="status"`, `aria-busy` e um texto escondido
("Carregando os seus animais..."), para o leitor de tela não perder o aviso
que o spinner dava.

### D4. Spinner em botão fica

O spinner dentro de "Enviar foto" ou "Salvar" mostra uma ação em curso, não
uma carga de tela. Não há layout a preservar ali.

### D5. `preparar_carga` primeiro no `on_load` (achado na verificação)

Os carregadores são corrotinas sem `yield`: o `carregando = True` do começo só
chegava à tela junto com o resultado. O "carregando" nunca aparecia, e Loja,
Agenda e Perfil, que só olhavam `carregando`, mostravam o vazio ("Nenhum
produto à venda") até os dados virem. Transformar os carregadores em
geradores quebraria as dezesseis chamadas `await self.carregar_...()` que
existem por dentro dos States.

Cada State ganha `preparar_carga`, um evento sem requisição que zera o erro,
marca `carregando` e desmarca `ja_carregou`. Ele vai primeiro no `on_load` de
cada página, e o Reflex manda o estado à tela ao fim de cada evento. Loja e
Agenda ganham `mostrar_carregando` no mesmo formato de `PetState` e
`EquipeState`: carregando, ou ainda não carregado e sem erro.

Medido ao abrir Serviços pela primeira vez: o vazio aparece por ~6 ms (até o
`preparar_carga` chegar, menos de um quadro) e o esqueleto até ~645 ms, quando
os serviços entram. Antes, o vazio ficava os ~600 ms inteiros. Na volta a uma
tela já carregada, a lista anterior fica até a nova chegar, sem pulo.
