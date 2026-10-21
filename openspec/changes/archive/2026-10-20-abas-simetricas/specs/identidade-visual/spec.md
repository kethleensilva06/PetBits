## MODIFIED Requirements

### Requirement: As abas do cliente têm a mesma largura

Meus animais, Agendar, Loja, Meus pedidos e Meu perfil SHALL ocupar a mesma
largura de página e começar no mesmo ponto da tela, tenha a aba barra de
rolagem ou não, para o cabeçalho, o avatar e o menu ficarem no mesmo lugar ao
trocar de aba.

#### Scenario: Da casa para a loja

- **WHEN** a tutora vai de Meus animais para a Loja numa tela larga
- **THEN** o conteúdo das duas ocupa a mesma largura, e o cabeçalho não muda de lugar

#### Scenario: Aba curta e aba longa

- **WHEN** Meus animais cabe na tela sem rolar e a Loja precisa de rolagem
- **THEN** o cabeçalho e o avatar ficam exatamente no mesmo lugar nas duas
