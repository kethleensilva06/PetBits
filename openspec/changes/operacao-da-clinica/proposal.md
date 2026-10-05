# Proposal

## Why

Metade do sistema não existe. O tutor entra, cadastra os animais e vê os
dados dele; a **clínica**, que é quem opera o negócio, não tem nada.

O sintoma é concreto e já está no ar: um colaborador consegue entrar hoje —
o login não olha o papel — e cai numa tela que diz "os seus animais". Como
uma conta da equipe não tem ficha de tutor, o filtro de posse devolve vazio,
e ele lê "Nenhum animal cadastrado ainda". Para quem administra a clínica,
isso é absurdo.

Esta change também é pré-requisito do agendamento, que vem depois: sem
colaborador cadastrado não há quem atenda, e sem serviço cadastrado não há
**duração** — e é a duração que torna a agenda calculável.

## What Changes

- A tela de entrada passa a ter **duas abas**: *Cliente* e *Colaborador*.
- Quem entra é levado à **sua** área: o tutor para os animais, a equipe para
  o painel da clínica.
- A equipe **cadastra e mantém colaboradores**: nome, função (veterinário,
  tosador, atendente) e contato.
- A equipe **cadastra e mantém serviços**: nome, preço e duração estimada.
- A equipe **vê todos os tutores e todos os animais** da clínica — a visão
  que o tutor não tem.
- Um tutor continua **sem alcançar** nada disso, nem pela interface nem por
  requisição direta.

### Sobre as duas abas

As duas abas usam **a mesma verificação de credencial**. A aba é escolha de
destino, não de autenticação.

Isto não é detalhe de implementação, é o ponto: se cada aba verificasse de um
jeito, descobrir quem é colaborador da clínica seria só tentar o mesmo e-mail
nas duas e ver em qual ele passa — e isso entrega o organograma a qualquer
pessoa. É a mesma família de falha que esta change **não** vai repetir, e que
a change anterior deixou registrada no cadastro público.

### Fora do escopo

- **Agendamento e histórico clínico** — são as changes seguintes.
- **Petshop** (produtos, pedidos) — fora do roteiro atual.
- **Cadastro de tutor de balcão pela clínica.** A equipe vê os tutores, mas
  ainda não os cria. Criar envolve o vínculo opcional com conta de acesso, que
  o design da change anterior registrou como o ponto onde a garantia de "uma
  conta, um tutor" precisa ser refeita à mão — merece uma change que trate só
  disso.
- **Promover alguém a colaborador pela aplicação.** Continua acontecendo fora
  do app, e isso não vai mudar: se houvesse um caminho na aplicação para virar
  equipe, haveria um caminho para invadi-la.
- **O oráculo de CPF do cadastro público**, registrado em aberto na change
  anterior. Tem change própria.
- Identidade visual.

### Uma distinção que vale fixar agora

**Colaborador** é um registro do domínio: quem trabalha na clínica, com
função e contato. **Conta de equipe** é uma credencial com papel de
administrador.

São coisas separadas, e o sistema não as liga nesta change. Um veterinário
pode estar cadastrado sem nunca acessar o sistema — como um tutor de balcão —,
e uma conta de equipe pode existir sem ficha de colaborador. Ligar as duas é
trabalho de uma change futura, quando houver motivo.

## Capabilities

### New Capabilities

- `colaboradores`: quem trabalha na clínica — dados, função e quem pode
  lê-los ou alterá-los.
- `servicos`: o que a clínica oferece — nome, preço e duração estimada, que é
  o que torna a agenda calculável.
- `acesso-da-equipe`: o que distingue uma conta de equipe de uma conta de
  tutor — para onde cada uma é levada ao entrar, e o que cada uma alcança.

### Modified Capabilities

- `autenticacao`: a entrada passa a conduzir cada papel à sua área, e a tela
  de entrada passa a ter duas abas que **não** diferem na verificação.
- `animais`: a equipe passa a enxergar todos os animais da clínica, por um
  caminho separado do caminho do tutor — que continua restrito ao dono.
- `tutores`: a equipe passa a enxergar todos os tutores.

## Impact

**Xano** (`workspace 169225`, API group `PetBits`)

- Tabelas novas: colaborador e serviço.
- Endpoints novos de colaborador e de serviço, todos restritos à equipe.
- Endpoints novos para a equipe ver tutores e animais — **separados** dos do
  tutor. O filtro de posse atual é por posse direta e exclui o tutor sem
  conta; um ramo por papel dentro do mesmo endpoint seria o lugar onde a
  garantia se perde.
- Provável função reutilizável para "esta credencial é da equipe?", já que
  todos os endpoints novos precisam da mesma resposta.

**Aplicação Reflex**

- Abas na tela de entrada e roteamento por papel depois de entrar.
- Área da equipe, com navegação própria.
- Telas de colaboradores, de serviços e de consulta a tutores e animais.

**Restrições a respeitar**

- O plano gratuito aceita 10 requisições a cada 20 segundos, **por
  instância**. O painel da equipe é a primeira tela do projeto com risco real
  de consultar várias tabelas de uma vez.
- O papel vem do banco a cada requisição, nunca do que o cliente enviou nem
  do token.
- Toda limpeza de dados ao sair precisa alcançar os States novos — a change
  anterior deixou registrado que essa lista cresce e que esquecê-la é
  silencioso.
