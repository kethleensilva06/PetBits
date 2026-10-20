## ADDED Requirements

### Requirement: Esqueletos enquanto a tela carrega

Enquanto os dados de uma tela não chegaram, a tela SHALL mostrar blocos
cinza no formato do conteúdo que vai aparecer, no lugar do spinner com
"Carregando...". O esqueleto MUST NOT aparecer junto com o conteúdo, com a
tela vazia nem com o erro, e SHALL avisar o leitor de tela de que a tela está
carregando.

#### Scenario: Abrir a loja

- **WHEN** a tutora abre a loja e os produtos ainda não chegaram
- **THEN** vê cartões cinza na grade dos produtos, e os produtos entram no lugar deles

#### Scenario: A carga falhou

- **WHEN** a carga de Meus pedidos falha
- **THEN** aparece o aviso de erro e nenhum esqueleto

#### Scenario: Leitor de tela

- **WHEN** um leitor de tela passa pelo esqueleto
- **THEN** ele lê que a tela está carregando
