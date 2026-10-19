## ADDED Requirements

### Requirement: O colaborador altera os próprios dados

Uma conta de equipe SHALL alterar o nome e o telefone da própria ficha de
colaborador. A ficha MUST ser a que tem o mesmo e-mail da conta do token,
nunca uma indicada na requisição. Nome MUST NOT ficar em branco. Função,
e-mail, data de entrada e ativo MUST NOT ser alterados por este caminho.
Alterar o nome SHALL alterar também o nome da conta de acesso.

#### Scenario: Troca de telefone

- **WHEN** a veterinária muda o telefone no perfil e salva
- **THEN** a ficha dela passa a ter o novo telefone, e a função continua a mesma

#### Scenario: Tentativa de mudar a própria função

- **WHEN** uma requisição direta envia `funcao` junto com o telefone
- **THEN** a função não muda

#### Scenario: Conta de equipe sem ficha

- **WHEN** uma conta de equipe cujo e-mail não está em ficha nenhuma abre o perfil
- **THEN** vê a troca de senha e o aviso para procurar a gerência, e a alteração de dados é recusada

#### Scenario: Conta de tutor

- **WHEN** uma conta de tutor chama o perfil de colaborador, fora da interface
- **THEN** o backend recusa, sem devolver dado de ficha nenhuma

#### Scenario: Nome novo depois de sair e entrar

- **WHEN** o colaborador muda o nome, sai e entra de novo
- **THEN** a saudação do topo usa o nome novo

### Requirement: Foto do colaborador

Uma conta de equipe com ficha SHALL enviar uma foto, que substitui a anterior
e aparece no avatar do topo da clínica. Só imagens JPG, PNG ou WebP de até
5 MB SHALL ser aceitas. Sem foto, o avatar mostra as iniciais.

#### Scenario: Envio de foto

- **WHEN** o colaborador envia uma foto WebP pelo perfil
- **THEN** a foto passa a aparecer no avatar do topo

#### Scenario: Arquivo que não é imagem

- **WHEN** ele envia um PDF
- **THEN** o envio é recusado com o motivo, e a foto anterior continua
