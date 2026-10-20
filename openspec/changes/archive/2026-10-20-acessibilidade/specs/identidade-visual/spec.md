## ADDED Requirements

### Requirement: Contraste e nomes acessíveis

O texto das telas SHALL ter contraste de pelo menos 4,5 com o fundo (3 para
texto grande), também nos botões de cor sólida. Todo campo de formulário SHALL
ter um nome acessível igual ao rótulo visível, toda imagem SHALL ter texto
alternativo, e a página SHALL ser declarada em português (`pt-BR`). O foco do
teclado SHALL ser visível.

#### Scenario: Botão principal

- **WHEN** a tela mostra um botão verde-água com texto branco
- **THEN** o contraste entre o texto e o botão é de pelo menos 4,5

#### Scenario: Texto secundário

- **WHEN** a casa mostra a raça e o peso de um animal em cinza
- **THEN** o contraste com o fundo é de pelo menos 4,5

#### Scenario: Campo com leitor de tela

- **WHEN** um leitor de tela chega ao campo Nome do perfil
- **THEN** ele anuncia "Nome"

#### Scenario: Navegação pelo teclado

- **WHEN** alguém navega pelo teclado com Tab
- **THEN** o elemento em foco tem um contorno visível
