# Project Overview — PetBits

## 1. Visão geral

PetBits é um sistema de gestão para uma clínica veterinária que também opera
como petshop. Ele reúne num só lugar o que hoje costuma viver em cadernos,
planilhas e na memória da equipe: quem são os tutores, quais animais estão sob
cuidado da clínica, o que foi feito em cada atendimento, o que está agendado e
o que foi vendido.

O sistema atende dois grupos com necessidades diferentes. A **equipe da
clínica** administra a operação. O **tutor** acompanha os próprios animais e
marca atendimentos sem precisar telefonar.

## 2. Problema

Numa clínica de bairro, a informação sobre um animal fica espalhada. A agenda
está num caderno, o histórico clínico numa ficha de papel, as vendas num
bloco de notas. Isso produz três problemas concretos:

- **Perda de histórico.** Quando o tutor troca de veterinário dentro da mesma
  clínica, o que foi feito antes depende de alguém lembrar ou achar a ficha.
- **Agenda frágil.** Marcar por telefone ocupa a recepção e permite marcar
  duas consultas no mesmo horário para o mesmo profissional.
- **Tutor sem autonomia.** Para saber quando é a próxima consulta, o que foi
  diagnosticado ou quanto custou a última compra, o tutor precisa ligar.

## 3. Objetivos

1. Manter o cadastro de tutores, animais e equipe num registro único.
2. Registrar o histórico clínico de cada animal de forma permanente e
   consultável.
3. Permitir que o tutor marque atendimento sozinho, sem conflito de horário.
4. Registrar as vendas do petshop e vinculá-las ao tutor.
5. Dar à equipe uma visão do dia: quem vem, com quem, para quê.

## 4. Público-alvo / usuários

**Equipe da clínica.** Veterinários, tosadores e atendentes. Usam o sistema
durante o expediente, para administrar cadastros, registrar atendimentos e
organizar a agenda.

**Tutor.** Dono de um ou mais animais atendidos pela clínica. Usa o sistema
ocasionalmente, para marcar atendimento e consultar o que já aconteceu.
Cadastra-se sozinho pelo site.

Um tutor **nunca** enxerga dados de outro tutor. Um tutor **nunca** administra
a clínica.

## 5. Escopo

### Dentro do escopo

- Cadastro e autenticação de tutores e de membros da equipe.
- Cadastro de animais, vinculados ao tutor responsável.
- Agendamento de serviços, com prevenção de conflito de horário.
- Registro do histórico clínico de cada animal.
- Catálogo de serviços e de produtos.
- Registro de pedidos do petshop.

### Fora do escopo (por ora)

- Pagamento online e emissão fiscal.
- Aplicativo móvel nativo.
- Integração com laboratórios ou sistemas externos.
- Controle de estoque com entrada de mercadoria.
- Prontuário com anexo de imagens ou exames.

O escopo pode crescer, mas cada ampliação deve entrar como uma change própria,
não como decisão tomada durante a implementação de outra coisa.

## 6. Principais funcionalidades

Descritas como **capacidades do usuário**, não como telas ou endpoints:

**Para o tutor**

- criar a própria conta e entrar no sistema;
- cadastrar e manter os dados dos seus animais;
- marcar um atendimento escolhendo animal, serviço e horário disponível;
- cancelar um atendimento que ainda não aconteceu;
- consultar o histórico clínico dos seus animais;
- acompanhar as próprias compras.

**Para a equipe da clínica**

- manter o cadastro de tutores, animais e colaboradores;
- manter o catálogo de serviços e de produtos;
- ver e organizar a agenda de atendimentos;
- registrar o que foi feito em cada atendimento;
- registrar pedidos do petshop;
- acompanhar uma visão geral do movimento da clínica.

## 7. Requisitos e restrições importantes

- **Um atendimento não pode ser marcado em cima de outro** para o mesmo
  profissional. Esta é a regra de negócio mais delicada do sistema, porque
  depende de concorrência: duas pessoas podem tentar o mesmo horário ao mesmo
  tempo.
- **O histórico clínico não é apagado.** Um atendimento registrado permanece
  registrado.
- **O acesso de um tutor é restrito aos dados dele.** Isso vale para leitura e
  para escrita.
- **Cancelar libera o horário**; não é o mesmo que apagar o registro.
- O sistema é usado em português brasileiro, com datas e valores no formato
  brasileiro.

## 8. Arquitetura tecnológica

**Frontend: Reflex.** Reflex será utilizado como tecnologia exclusiva para
implementação do frontend da aplicação. Ambiente Python gerenciado com `venv`
e `pip` (conforme o Apêndice B); `uv` não é utilizado.

**Persistência: Xano.** O banco de dados e a API REST ficam hospedados no
Xano. A aplicação Reflex não possui banco local nem ORM: toda persistência
acontece por HTTP contra a API do Xano.

**Autorização: no backend.** O Xano é quem decide o que cada pessoa pode ver e
fazer. O frontend esconde o que não interessa, mas esconder não é proteger.

Decisões de arquitetura só mudam por uma change explícita.

## 9. Princípios de desenvolvimento

- **Fatias verticais, não camadas.** Cada change entrega uma funcionalidade
  utilizável de ponta a ponta, não "o banco inteiro" ou "o frontend inteiro".
- **Incremental.** O modelo de domínio é global desde o início; a
  implementação é feita aos poucos, na ordem que as changes definirem.
- **Especificar antes de implementar.** Mudanças relevantes passam pelo ciclo
  do OpenSpec.
- **Verificável.** Uma funcionalidade só está pronta quando existe um jeito
  declarado de conferir que ela funciona.

## 10. Segurança e integridade

- As regras de autorização são aplicadas no backend, sempre.
- O papel do usuário é lido do banco no momento da requisição, não do que o
  cliente enviou.
- Um usuário só é promovido a membro da equipe por fora da aplicação; o
  cadastro público cria apenas tutores.
- Senhas nunca trafegam nem são armazenadas em texto claro; isso é
  responsabilidade do mecanismo de autenticação do backend.
- Credenciais de acesso ao Xano vivem em `.env`, que não é versionado.

## 11. Estratégia de desenvolvimento

O desenvolvimento segue o ciclo do OpenSpec:

```text
Explore → Propose → Review → Apply → Archive → próxima change
```

Cada change delimita uma mudança funcional que pode ser planejada, revisada e
verificada por inteiro. A ordem das changes é decidida no Explore e revisada
conforme o sistema cresce.

### Roteiro atual — cinco changes

| # | Change | O que passa a ser possível |
|---|---|---|
| 1 | `acesso-do-tutor` ✓ | Criar conta pelo site, entrar, sair; sessão que sobrevive ao recarregar |
| 2 | `animais-do-tutor` ✓ | O tutor cadastra e mantém os próprios animais |
| 3 | `operacao-da-clinica` ✓ | A equipe entra e declara quem atende e o que a clínica oferece |
| 4 | `agendamento` *(em andamento)* | O tutor marca e cancela atendimento; a equipe vê a agenda |
| 5 | `historico-clinico` | A equipe registra o atendimento; o tutor lê o dos seus animais |

As cinco cobrem o núcleo clínico de ponta a ponta. A ordem não é arbitrária:
a change 2 estabelece o **padrão de posse** que a 4 e a 5 repetem, e a 3
precisa existir antes da 4 porque sem serviço cadastrado não há duração, e
sem duração não há agenda calculável.

**Fora do roteiro, por ora:** o petshop (produtos, pedidos e itens). Ele é o
único ramo do domínio independente do agendamento, então adiá-lo não bloqueia
nada. **A pedido da clínica, entrou em três changes:** `loja` *(em andamento)*
— catálogo da equipe com estoque e compra pelo cliente, com retirada ou entrega
e pagamento na loja ou online simulado —, `pedidos-da-equipe` e
`venda-no-balcao` (planejadas). O pedido anterior, de uma vitrine sem compra,
foi substituído pela loja de verdade.

**Changes de apoio, fora da contagem:** não entregam funcionalidade para a
clínica, mas passam pelo mesmo fluxo.

| Change | O que passa a ser possível |
|---|---|
| `atalho-contas-de-teste` ✓ | Em desenvolvimento, `Alt+1` na entrada lista as contas de teste e preenche o formulário |
| `entrada-sem-trava` ✓ | O botão Entrar nunca fica travado depois de uma tentativa interrompida |
| `atalho-de-clientes` ✓ | `Alt+1` lista a equipe e `Alt+2` os clientes de teste |
| `clientes-de-teste-por-script` ✓ | Um script cria clientes de teste e os põe no `Alt+2` |
| `aba-define-a-area` ✓ | A aba da entrada escolhia a área depois da senha aceita — substituída pela `porta-de-entrada` |
| `porta-de-entrada` *(em andamento)* | Página inicial pública; entradas separadas para clientes e equipe; funcionário sempre na gerência |
| `papel-staff` *(em andamento)* | O papel `staff`, criado no Xano, conta como equipe |
| `cadastro-de-cliente-pela-conta` *(em andamento)* | Conta sem ficha cria a própria ficha de cliente — motivo desfeito pela `porta-de-entrada`; decisão pendente |

O roteiro é revisado conforme o sistema cresce — ele registra a intenção
atual, não um compromisso.

## 12. Fonte de verdade e documentação

| Documento | Responde |
|---|---|
| `docs/project-overview.md` | O que é o projeto |
| `docs/domain-model.md` | Quais são os conceitos e como se relacionam |
| `AGENTS.md` | Como o agente deve trabalhar no projeto |
| `openspec/config.yaml` | Que contexto e regras valem em toda change |
| `openspec/specs/` | O comportamento consolidado do sistema |
| `openspec/changes/` | O que está sendo planejado ou implementado agora |

Quando este documento e o código discordarem, o código não está
automaticamente certo: a divergência deve ser resolvida por uma change.
