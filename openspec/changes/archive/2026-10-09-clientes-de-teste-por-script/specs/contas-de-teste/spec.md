## ADDED Requirements

### Requirement: Script cria clientes de teste e os registra no arquivo

O projeto SHALL ter um script que cria N clientes de teste pelo cadastro
público e acrescenta cada um, como bloco `TUTOR`, ao arquivo local de contas
de teste. Os dados gerados MUST cumprir as regras do cadastro — CPF de 11
dígitos e senha com ao menos 8 caracteres, uma letra e um número — e o e-mail
MUST ser único e do domínio `exemplo.com`. A senha MUST NOT aparecer na saída
do script.

#### Scenario: Criar clientes

- **WHEN** quem desenvolve roda o script pedindo 3 clientes
- **THEN** três contas de cliente são criadas pelo cadastro público
- **AND** as três aparecem no `Alt+2`, com e-mail e senha corretos

#### Scenario: Cadastro recusado

- **WHEN** o cadastro público recusa um dos clientes
- **THEN** o script informa a recusa, não grava esse cliente no arquivo e
  continua com os demais

#### Scenario: Sem configuração do Xano

- **WHEN** o `.env` não tem o endereço do Xano
- **THEN** o script para antes de qualquer requisição, explicando o que falta

#### Scenario: Senha fora da saída

- **WHEN** o script termina
- **THEN** a saída mostra nome e e-mail de cada cliente criado, e nenhuma senha
