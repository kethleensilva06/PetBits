## ADDED Requirements

### Requirement: O site também no GitHub Pages

A parte visual do site SHALL poder ser publicada no GitHub Pages do repositório,
em https://kethleensilva06.github.io/PetBits/, ligada ao servidor do Reflex
Cloud. Abrir qualquer endereço do site direto SHALL funcionar, e as imagens do
app MUST carregar sob o prefixo `/PetBits/`. Nada do `.env` MUST ir para o
GitHub Pages.

#### Scenario: Abrir a loja direto

- **WHEN** alguém sem sessão abre https://kethleensilva06.github.io/PetBits/loja
- **THEN** o servidor do Reflex Cloud responde e leva à entrada de clientes

#### Scenario: Fotos da página inicial

- **WHEN** a página inicial abre no GitHub Pages
- **THEN** as fotos carregam de `/PetBits/fotos/`
