# pedidos Specification

## Purpose

Define o Pedido — o que um cliente comprou da loja, e o que a clínica faz com
isso depois. Cobre as duas origens que levam ao mesmo registro: o pedido
feito pelo cliente no site e a **venda no balcão**, registrada pela equipe na
conta de quem está ali na frente.

O que esta capability governa é a **passagem de estado**: quais caminhos a
situação de um pedido pode seguir, quem pode movê-la, e o que cada passagem
faz com o estoque e com o pagamento. Cancelar devolve os itens; pagar é
registro da equipe, não do cliente.

## Requirements

### Requirement: A equipe vê os pedidos

A equipe SHALL ver todos os pedidos, do mais recente para o mais antigo,
podendo filtrar por situação, com cliente, telefone, itens, total, entrega,
endereço, forma de pagamento e situação. A lista MUST ser exclusiva da
equipe.

#### Scenario: Lista da equipe

- **WHEN** a equipe abre os pedidos
- **THEN** vê os pedidos de todos os clientes, com os itens de cada um

#### Scenario: Cliente pede a lista da clínica

- **WHEN** uma conta de cliente pede a lista de pedidos da clínica, fora da
  interface
- **THEN** o backend recusa

### Requirement: A situação só avança por caminhos válidos

A equipe SHALL mudar a situação de um pedido apenas pelos caminhos:
`pendente` para `pago`, `pronto_retirada`, `enviado` ou `cancelado`; `pago`
para `pronto_retirada`, `enviado` ou `cancelado`; `pronto_retirada` para
`entregue` ou `cancelado`; `enviado` para `entregue`. `pronto_retirada` MUST
valer só para retirada, e `enviado` só para entrega no endereço. `entregue` e
`cancelado` MUST NOT mudar mais.

#### Scenario: Pedido pronto para retirada

- **WHEN** a equipe marca como pronto um pedido pago de retirada
- **THEN** a situação passa a `pronto_retirada` e o cliente vê isso em "Meus
  pedidos"

#### Scenario: Caminho inválido

- **WHEN** a requisição tenta levar um pedido `entregue` para `pendente`, ou
  marcar como `enviado` um pedido de retirada, mesmo fora da interface
- **THEN** a operação é recusada e a situação não muda

### Requirement: Pagamento registrado pela equipe

Levar um pedido a `pago`, ou a `entregue` sem pagamento registrado, SHALL
gravar a data do pagamento. Um pedido já pago MUST manter a data original.

#### Scenario: Paga na retirada

- **WHEN** a equipe entrega um pedido `pronto_retirada` que tinha pagamento
  na loja e ainda não estava pago
- **THEN** a situação passa a `entregue` e a data do pagamento é registrada

### Requirement: Cancelar devolve o estoque

Cancelar um pedido SHALL devolver ao estoque a quantidade de cada item, numa
única transação: ou todo o estoque volta e o pedido fica cancelado, ou nada
muda.

#### Scenario: Cancelamento

- **WHEN** a equipe cancela um pedido com 2 unidades de um produto
- **THEN** o estoque desse produto aumenta em 2 e o pedido fica `cancelado`

### Requirement: Venda no balcão

A equipe SHALL registrar uma venda presencial na conta de um cliente
cadastrado, com um ou mais itens. A venda MUST nascer entregue, com o
pagamento na loja registrado, origem `balcao`, e MUST baixar o estoque e
calcular preço e total pelas mesmas regras do pedido feito pelo site. A venda
no balcão MUST ser exclusiva da equipe.

#### Scenario: Venda registrada

- **WHEN** o atendente vende 1 unidade de um produto ao cliente Ana
- **THEN** o pedido nasce entregue, pago, com origem balcão
- **AND** aparece em "Meus pedidos" da Ana, e o estoque baixa em 1

#### Scenario: Estoque insuficiente no balcão

- **WHEN** o atendente tenta vender mais do que o estoque
- **THEN** a venda é recusada e nenhum estoque muda

#### Scenario: Cliente inexistente

- **WHEN** a requisição informa um cliente que não existe
- **THEN** a venda é recusada

#### Scenario: Cliente tenta registrar venda no balcão

- **WHEN** uma conta de cliente chama a venda no balcão, fora da interface
- **THEN** o backend recusa

### Requirement: Origem do pedido

Todo pedido SHALL ter origem `site` ou `balcao`. Pedidos feitos pela loja do
site MUST ter origem `site`.

#### Scenario: Pedido pelo site

- **WHEN** o cliente compra pela loja
- **THEN** o pedido tem origem `site`

### Requirement: Fazer um pedido

O cliente SHALL fazer um pedido com um ou mais itens (produto e quantidade),
a forma de entrega — retirada na clínica ou entrega no endereço — e a forma
de pagamento — na loja ou online simulado. O pedido MUST pertencer ao cliente
do token. Um pedido sem itens MUST ser recusado.

#### Scenario: Pedido com retirada e pagamento na loja

- **WHEN** o cliente pede 2 unidades de um produto com estoque, retirada na
  clínica, pagamento na loja
- **THEN** o pedido é criado como pendente, com forma de pagamento "na loja"
- **AND** aparece em "Meus pedidos"

#### Scenario: Pagamento online simulado

- **WHEN** o cliente escolhe pagamento online
- **THEN** o pedido é criado como pago, com forma de pagamento "online" e a
  data do pagamento, sem que nenhum valor seja cobrado

#### Scenario: Entrega no endereço

- **WHEN** o cliente escolhe entrega no endereço
- **THEN** o pedido guarda o endereço do cadastro do cliente naquele momento

#### Scenario: Entrega sem endereço cadastrado

- **WHEN** o cliente escolhe entrega no endereço e o cadastro dele não tem
  endereço
- **THEN** a operação é recusada com a orientação de escolher retirada

#### Scenario: Pedido vazio

- **WHEN** a requisição não tem nenhum item, ou um item com quantidade menor
  que 1
- **THEN** a operação é recusada

### Requirement: Preço e total calculados no servidor

O preço unitário de cada item SHALL ser o preço do produto no momento da
compra, congelado no item. O valor da linha e o total do pedido MUST ser
calculados pelo servidor; nenhum valor enviado pelo cliente participa do
cálculo. Mudar o preço de um produto MUST NOT alterar pedidos já feitos.

#### Scenario: Preço muda depois da compra

- **WHEN** a equipe altera o preço de um produto já comprado
- **THEN** o pedido antigo continua com o preço e o total da hora da compra

#### Scenario: Total enviado pelo cliente

- **WHEN** a requisição tenta informar preço ou total, fora da interface
- **THEN** esses valores são ignorados e o total sai do preço do catálogo

### Requirement: Estoque baixa com o pedido

Fazer o pedido SHALL baixar o estoque de cada produto pela quantidade pedida.
Se algum item pedir mais do que o estoque disponível, ou um produto inativo,
o pedido inteiro MUST ser recusado e nenhum estoque MUST mudar. Dois pedidos
simultâneos MUST NOT vender a mesma unidade duas vezes.

#### Scenario: Estoque insuficiente

- **WHEN** o cliente pede 5 unidades de um produto com estoque 3
- **THEN** o pedido é recusado, informando o produto
- **AND** nenhum estoque muda

#### Scenario: Última unidade

- **WHEN** dois clientes pedem ao mesmo tempo a última unidade de um produto
- **THEN** só um pedido é aceito

### Requirement: Meus pedidos

O cliente SHALL ver apenas os próprios pedidos, do mais recente para o mais
antigo, com itens, total, entrega, pagamento e situação. Cada pedido não
cancelado SHALL mostrar as etapas do seu caminho — Pedido recebido,
Pagamento, Pronto para retirada ou Enviado, Retirado ou Entregue —, com as
etapas feitas marcadas e a atual destacada. A etapa do pagamento SHALL ficar
feita só quando o pagamento foi registrado. O pedido cancelado SHALL dizer
que foi cancelado, sem as etapas.

#### Scenario: Dois clientes

- **WHEN** dois clientes têm pedidos
- **THEN** cada um vê só os seus, mesmo pedindo a lista fora da interface

#### Scenario: Pedido pago para entrega

- **WHEN** a cliente abre um pedido pago, com entrega no endereço
- **THEN** vê Pedido recebido e Pagamento feitos, Enviado como a etapa atual e Entregue por vir

#### Scenario: Pronto antes de pagar

- **WHEN** um pedido de retirada com pagamento na loja está pronto para retirada e ainda não foi pago
- **THEN** Pronto para retirada aparece feito, Retirado como a atual, e o pagamento como "Pagar na retirada", não feito

#### Scenario: Pedido cancelado

- **WHEN** o pedido foi cancelado
- **THEN** ele não mostra etapas, e diz que foi cancelado e que os itens voltaram ao estoque

### Requirement: O carrinho sobrevive a recarregar a página

O carrinho do cliente SHALL continuar com os mesmos produtos e quantidades
depois de recarregar a página, abrir outra aba ou o servidor reiniciar. Ao
abrir a loja, o carrinho SHALL ser conferido com o catálogo: produto fora da
loja sai, e quantidade acima do estoque é reduzida. Sair da conta MUST
esvaziar o carrinho.

#### Scenario: Recarregar a loja

- **WHEN** a tutora põe dois sachês no carrinho e aperta F5
- **THEN** o carrinho continua com os dois sachês

#### Scenario: Estoque menor

- **WHEN** o carrinho guardado tem 5 unidades e o estoque agora é 3
- **THEN** ao abrir a loja o carrinho fica com 3

#### Scenario: Outra pessoa no mesmo navegador

- **WHEN** a tutora sai da conta e outra pessoa entra no mesmo navegador
- **THEN** o carrinho da outra pessoa começa vazio
