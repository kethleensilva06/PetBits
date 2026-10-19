## ADDED Requirements

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
