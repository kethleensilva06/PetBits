# produtos Specification

## Purpose

Define o Produto — o que a loja vende: nome, preço, estoque e categoria.

É o catálogo do qual saem tanto a loja do cliente quanto a venda no balcão, e
é por isso que `ativo` e estoque importam aqui e não lá: produto inativo ou
sem estoque não chega a aparecer para quem compra. O que esta capability
governa é o cadastro em si; o que acontece quando alguém compra pertence a
`pedidos`.

## Requirements

### Requirement: Script cadastra produtos de exemplo

O projeto SHALL ter um script que entra com uma conta de equipe do arquivo
local de contas de teste e cadastra produtos de exemplo pelo mesmo cadastro
da tela da equipe. Produto cujo nome já exista no catálogo MUST ser pulado. A
senha da conta MUST NOT aparecer na saída.

#### Scenario: Catálogo vazio

- **WHEN** quem desenvolve roda o script com o catálogo vazio
- **THEN** 15 produtos ativos, com estoque, passam a aparecer na loja

#### Scenario: Rodar de novo

- **WHEN** o script roda com os produtos de exemplo já cadastrados
- **THEN** nenhum produto é duplicado

#### Scenario: Sem conta de equipe com senha

- **WHEN** o arquivo de contas de teste não tem conta de equipe com senha
- **THEN** o script para antes de qualquer requisição, explicando o que falta

#### Scenario: A conta não é de equipe

- **WHEN** a conta usada entra mas não tem papel de equipe
- **THEN** o script para sem cadastrar nada, explicando o motivo

### Requirement: Cadastro de produto

A equipe SHALL cadastrar produtos com nome, categoria, preço, estoque e,
opcionalmente, marca, unidade de venda e descrição. O nome MUST NOT ficar em
branco, o preço MUST ser maior que zero e o estoque MUST ser maior ou igual a
zero. Todo produto nasce ativo.

#### Scenario: Produto cadastrado

- **WHEN** a equipe cadastra "Ração adulto 1 kg", categoria ração, R$ 49,90,
  estoque 20
- **THEN** o produto aparece no catálogo da equipe e, por estar ativo e com
  estoque, na loja do cliente

#### Scenario: Preço inválido

- **WHEN** o cadastro informa preço zero ou negativo, mesmo fora da interface
- **THEN** a operação é recusada e o motivo é informado

#### Scenario: Estoque negativo

- **WHEN** o cadastro ou a alteração informa estoque negativo
- **THEN** a operação é recusada

### Requirement: Alterar e desativar produto

A equipe SHALL alterar os dados de um produto, inclusive o estoque, e
ativá-lo ou desativá-lo. Os campos não mencionados MUST permanecer. Produto
desativado MUST NOT aparecer na loja nem ser comprado.

#### Scenario: Desativar

- **WHEN** a equipe desativa um produto
- **THEN** ele some da loja do cliente e uma compra que o inclua é recusada
- **AND** continua no catálogo da equipe, marcado como inativo

#### Scenario: Alteração parcial

- **WHEN** a equipe altera só o preço de um produto
- **THEN** os outros campos permanecem como estavam

### Requirement: O catálogo é da equipe

Criar e alterar produtos SHALL ser exclusivo da equipe.

#### Scenario: Cliente tenta alterar o catálogo

- **WHEN** uma conta de cliente tenta criar ou alterar um produto, fora da
  interface
- **THEN** o backend recusa e o catálogo permanece inalterado

### Requirement: A loja mostra o que pode ser comprado

O cliente SHALL ver, na loja, os produtos ativos com estoque maior que zero,
com nome, categoria, marca, unidade, preço, descrição e quantidade
disponível.

#### Scenario: Produto sem estoque

- **WHEN** o estoque de um produto chega a zero
- **THEN** ele deixa de aparecer na loja

### Requirement: Detalhe do produto na loja

Na loja, clicar na foto ou no nome de um produto SHALL abrir o detalhe dele,
com a foto grande, categoria, marca, embalagem, descrição, preço,
disponibilidade, a quantidade já no carrinho e o botão de adicionar. Abrir o
detalhe SHALL NOT fazer requisição ao backend: os dados são os que a loja
já carregou.

#### Scenario: Abrir o detalhe

- **WHEN** a tutora clica na foto do "Arranhador de papelão"
- **THEN** abre o detalhe com a foto grande, a descrição "Com erva-de-gato inclusa." e o preço

#### Scenario: Adicionar pelo detalhe

- **WHEN** ela clica em "Adicionar ao carrinho" no detalhe
- **THEN** o produto entra no carrinho e o detalhe passa a mostrar "No carrinho: 1"

#### Scenario: Fechar

- **WHEN** ela aperta Esc ou o X
- **THEN** o detalhe fecha e a loja continua onde estava, com o carrinho intacto

### Requirement: Foto do produto enviada pela equipe

A equipe SHALL enviar a foto de um produto já cadastrado, que substitui a
anterior. Só imagens JPG, PNG ou WebP de até 5 MB SHALL ser aceitas, e o
conteúdo MUST ser de fato uma imagem, não só ter o nome de uma. Enviar foto
de produto SHALL ser exclusivo da equipe: a prova de equipe MUST vir antes de
qualquer leitura e de guardar o arquivo.

#### Scenario: Foto enviada

- **WHEN** a equipe envia uma foto WebP para a "Escova removedora de pelos" pelo diálogo de edição
- **THEN** o cartão do produto na tela da equipe passa a mostrar essa foto

#### Scenario: Trocar a foto

- **WHEN** a equipe envia outra foto para um produto que já tem uma
- **THEN** a nova substitui a anterior, na equipe e na loja

#### Scenario: Arquivo que não é imagem

- **WHEN** o envio é um PDF, um arquivo com nome `.jpg` que não é imagem, ou uma imagem de mais de 5 MB
- **THEN** é recusado com o motivo, e a foto anterior continua

#### Scenario: Cliente tenta enviar foto de produto

- **WHEN** uma conta de cliente chama o envio de foto de produto, fora da interface
- **THEN** o backend recusa como faz com o resto do catálogo, e o produto continua com a foto que tinha

#### Scenario: Produto inexistente

- **WHEN** a equipe envia foto para um `produto_id` que não existe
- **THEN** a resposta é "Produto não encontrado." e nada é guardado

### Requirement: Busca e filtro na loja

A loja SHALL permitir buscar produto pelo nome, ignorando maiúsculas e
acentos, e filtrar por categoria. Buscar e filtrar SHALL NOT fazer requisição
ao backend. Quando nada casa, a loja SHALL dizer isso.

#### Scenario: Busca sem acento

- **WHEN** a tutora digita "racao" na busca
- **THEN** aparecem as rações, e só elas

#### Scenario: Filtro por categoria

- **WHEN** ela escolhe a categoria Brinquedo
- **THEN** aparecem só os brinquedos

#### Scenario: Nada encontrado

- **WHEN** a busca não casa com produto nenhum
- **THEN** a loja diz que nada foi encontrado

### Requirement: Quantidade no detalhe e carrinho no cabeçalho

O detalhe do produto SHALL permitir escolher a quantidade antes de adicionar,
limitada ao estoque disponível. O cabeçalho da área do cliente SHALL mostrar
um ícone de carrinho com o total de itens, que leva à loja.

#### Scenario: Levar três

- **WHEN** a tutora escolhe 3 no detalhe e adiciona
- **THEN** o carrinho passa a ter 3 daquele produto e o ícone do cabeçalho mostra 3

#### Scenario: Mais que o estoque

- **WHEN** ela tenta escolher mais do que o disponível
- **THEN** a quantidade para no estoque

### Requirement: CPF e telefone formatados

CPF e telefone SHALL ser formatados enquanto se digita, nos cadastros e nos
perfis: CPF como `000.000.000-00` e telefone como `(00) 0000-0000` ou
`(00) 00000-0000`. O que vai ao backend MUST continuar valendo para as regras
de lá (o CPF é normalizado no servidor).

#### Scenario: Digitar o CPF

- **WHEN** alguém digita `12345678909` no campo de CPF
- **THEN** o campo mostra `123.456.789-09`

#### Scenario: Digitar o celular

- **WHEN** alguém digita `11988887777` no telefone
- **THEN** o campo mostra `(11) 98888-7777`

### Requirement: Ordenar a loja

A loja do cliente SHALL poder ser ordenada por Em destaque (a ordem do
catálogo), Menor preço, Maior preço e Nome (A–Z), junto com a busca e o
filtro de categoria, sem requisição ao backend. A ordem por nome MUST ignorar
acentos e maiúsculas.

#### Scenario: Menor preço

- **WHEN** a tutora escolhe Menor preço
- **THEN** o produto mais barato aparece primeiro

#### Scenario: Com categoria

- **WHEN** a tutora filtra Higiene e escolhe Maior preço
- **THEN** vê só os produtos de higiene, do mais caro para o mais barato
