# verificacao

## Purpose

Define as conferências automáticas do projeto: os testes locais das regras
de tela, a guarda que impede endpoint de equipe sem prova e endpoint público
sem motivo, e a verificação de ponta a ponta no Xano com as contas de teste.

## Requirements

### Requirement: Testes locais das regras de tela

O projeto SHALL ter testes automáticos, sem dependência externa e sem acesso
ao Xano, para as regras que a interface aplica: horários livres e prazo de
cancelamento, caminhos de situação de pedido, carrinhos, leitura e grupos das
contas de teste, papéis e destinos. Eles MUST rodar com um comando só.

#### Scenario: Rodar os testes

- **WHEN** quem desenvolve roda `python -m unittest discover -s tests`
- **THEN** todos os testes rodam sem rede e o resultado diz quantos passaram

#### Scenario: Regra quebrada

- **WHEN** alguém muda o expediente da agenda e o sábado passa a oferecer
  horário que termina depois das 12h
- **THEN** um teste falha, apontando o cenário da spec

### Requirement: Nenhum endpoint público sem motivo escrito

A guarda de endpoints SHALL acusar todo endpoint do repositório sem
`auth = "user"` que não esteja na lista de públicos permitidos, e cada
público permitido MUST ter o motivo escrito ao lado.

#### Scenario: Endpoint público novo

- **WHEN** um endpoint sem `auth = "user"` é acrescentado ao repositório
- **THEN** a guarda acusa e sai com código 1

#### Scenario: Endpoints públicos permitidos

- **WHEN** a guarda roda
- **THEN** `entrar` e `tutor/cadastro` passam, com o motivo exibido

### Requirement: Verificação de ponta a ponta

O projeto SHALL ter um script, rodado por quem desenvolve, que entra com uma
conta de equipe e uma de cliente do arquivo local de contas de teste e
confere no Xano os cenários principais das specs. Cada cenário MUST sair como
passou ou falhou, o script MUST sair com código 1 se algum falhar, e nenhuma
senha ou token MUST aparecer na saída.

#### Scenario: Tudo certo

- **WHEN** o script roda contra o Xano com as duas contas válidas
- **THEN** cada cenário aparece como passou, e o código de saída é 0

#### Scenario: Faltam contas

- **WHEN** o arquivo não tem conta de equipe ou de cliente com senha
- **THEN** o script para antes de qualquer requisição, dizendo qual falta

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

### Requirement: A ponta a ponta não deixa produto de teste à venda

O produto que a verificação de ponta a ponta cria SHALL ser desativado ao fim
da rodada em qualquer caso — passando, falhando ou interrompida por erro.

#### Scenario: Rodada que para no meio

- **WHEN** a verificação de ponta a ponta para por erro depois de criar o produto de verificação
- **THEN** o produto fica inativo, e a loja do cliente não o mostra

### Requirement: O teste das duas contas não grava nada

O `scripts/teste_duas_contas.py` SHALL conferir cada endpoint de equipe sem
criar nem alterar registro. As sondas de escrita MUST usar um corpo que a
validação recusa depois da prova de equipe, de modo que a equipe receba uma
recusa diferente de 403 e o cliente receba 403.

#### Scenario: Rodada completa

- **WHEN** o teste das duas contas roda até o fim
- **THEN** a lista de serviços e a de colaboradores têm os mesmos registros de antes

#### Scenario: A prova continua sendo conferida

- **WHEN** a sonda de criação de serviço vai com a conta de equipe
- **THEN** a resposta é 400 (nome em branco), e não 403
