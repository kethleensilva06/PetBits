## ADDED Requirements

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
antigo, com itens, total, entrega, pagamento e situação.

#### Scenario: Dois clientes

- **WHEN** dois clientes têm pedidos
- **THEN** cada um vê só os seus, mesmo pedindo a lista fora da interface
