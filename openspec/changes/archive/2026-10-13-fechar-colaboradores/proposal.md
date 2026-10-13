# Proposal

## Why

O cadastro de colaboradores está pela metade, e de um jeito que o próprio
código denuncia.

A coluna `ativo` existe. O `PATCH` a aceita como entrada, com um comentário
explicando que **desligar é alterar `ativo`**. A lista não filtra por ela, e o
comentário da tabela justifica isso dizendo que filtrar "sumiria também com o
único caminho de religar alguém". O cartão até mostra o selo *Inativo*.

**Só que não existe caminho nenhum.** Nenhuma tela desliga, nenhuma religa. O
comentário fala de um caminho que nunca foi construído, e quem sair da clínica
fica no quadro para sempre — porque esta change também não vai acrescentar
exclusão, pelo motivo que já está escrito: quem saiu ainda é quem executou os
serviços já registrados.

Junto disso vai um defeito pequeno da mesma tela: **a data de entrada não pode
ser apagada.** O formulário só envia o campo quando ele tem valor, então
esvaziá-lo não apaga nada — a tela diz que salvou e o valor antigo volta. Uma
data digitada errada só pode ser trocada, nunca removida.

## What Changes

- **Desligar e religar** colaborador, pela tela, restrito à **gerência** —
  manter o quadro é dela desde a change `papeis-e-abas`.
- A lista distingue quem está desligado, e o cadastro de quem saiu **continua
  aparecendo**: sumir com ele sumiria com o caminho de voltar.
- **Apagar a data de entrada** passa a ser possível.

### Fora do escopo

- **Excluir colaborador.** Quem saiu ainda é quem executou os serviços já
  registrados, e o sistema vai precisar dizer quem atendeu. Desligar é a
  operação certa; excluir destruiria história.
- Ligar colaborador a conta de acesso. Continua sendo coisa separada.

## Capabilities

### Modified Capabilities

- `colaboradores`: desligar e religar passam a existir, e os dados opcionais
  passam a poder ser esvaziados.

## Impact

**Xano** — possivelmente nenhum: o `PATCH` já aceita `ativo`. O que falta
medir é se ele aceita **esvaziar** um `timestamp`, que nunca foi exercitado
nesta conta.

**Aplicação Reflex** — botão de desligar/religar no cartão, visível só para a
gerência, e o formulário passando o campo de data mesmo vazio.

**Restrições a respeitar**

- A lista **não** passa a filtrar inativos: esconder quem saiu esconderia o
  caminho de voltar.
- Esconder o botão é conveniência; quem recusa é o `exige_gerencia`.
