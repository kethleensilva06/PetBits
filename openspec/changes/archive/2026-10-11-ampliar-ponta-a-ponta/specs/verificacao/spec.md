## ADDED Requirements

### Requirement: A ponta a ponta cobre as recusas e as duas contas

A verificação de ponta a ponta SHALL conferir, além do caminho feliz, as
recusas das specs da agenda (fora do expediente, horário no passado, animal
de outro cliente), da loja (estoque negativo, produto inativo, pedido vazio,
categoria inválida), da gerência (equipe comum não mantém colaboradores) e
da separação entre clientes (um não vê nem cancela o que é do outro). Um
cenário que deixaria dado que o sistema não consegue desfazer MUST ser
pulado com o motivo escrito.

#### Scenario: Duas contas de cliente

- **WHEN** o arquivo de contas tem duas contas de cliente com senha
- **THEN** a segunda é usada para conferir que um cliente não vê, não usa e
  não cancela o que é do outro

#### Scenario: Uma conta de cliente só

- **WHEN** o arquivo tem uma conta de cliente só
- **THEN** os cenários de duas contas aparecem como pulados, com o motivo

### Requirement: O script de ponta a ponta tem teste próprio

O projeto SHALL testar o script de ponta a ponta contra um Xano simulado que
aplica as regras das specs, sem rede.

#### Scenario: Regra quebrada no backend simulado

- **WHEN** o Xano simulado deixa de baixar o estoque
- **THEN** o script acusa a falha e sai com código 1
