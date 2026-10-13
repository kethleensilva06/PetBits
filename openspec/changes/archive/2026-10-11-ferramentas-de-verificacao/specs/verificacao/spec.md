## ADDED Requirements

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
