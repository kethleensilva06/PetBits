# Domain Model — PetBits

Este documento descreve os **conceitos** do domínio e como eles se relacionam.
Ele não define tabelas, colunas nem tipos: essas decisões pertencem à change
que for implementar cada parte. O objetivo é que uma decisão tomada numa
change não contradiga o resto do sistema.

## Visão geral dos relacionamentos

```text
Conta de acesso
      │
      ├── (é) ──► Tutor ──┬── Animal ──┬── Agendamento ──► Serviço
      │                   │            │        │
      │                   │            │        └────────► Colaborador
      │                   │            │
      │                   │            └── Atendimento ──► Colaborador
      │                   │
      │                   └── Pedido ── Item do pedido ──► Produto
      │
      └── (é) ──► Colaborador
```

Leitura em uma frase: *um tutor tem animais; cada animal recebe agendamentos e
acumula atendimentos; o tutor também faz pedidos de produtos.*

---

## Conta de acesso

Representa a identidade de quem entra no sistema.

### Responsabilidade

Autenticar a pessoa e dizer **qual é o papel dela**. Nada mais: a conta não
guarda dados do domínio.

### Principais informações

- nome de exibição;
- e-mail (identifica a conta);
- segredo de autenticação;
- papel: *tutor* ou *equipe da clínica*.

### Relacionamentos

Uma conta corresponde a um Tutor **ou** a um Colaborador. A conta é a porta; o
Tutor e o Colaborador são quem a pessoa é dentro do domínio.

### Regras estruturais

- O e-mail é único.
- O papel é atribuído pelo sistema, nunca escolhido por quem se cadastra. O
  cadastro público cria sempre uma conta de tutor.
- O papel é sempre lido do registro no momento da requisição.

---

## Tutor

A pessoa responsável por um ou mais animais.

### Responsabilidade

Ser o dono dos dados: os animais, os atendimentos deles e as compras são
sempre de **algum** tutor. É por ele que passa toda decisão de "quem pode ver
o quê".

### Principais informações

- nome;
- documento de identificação;
- contato (telefone, e-mail);
- endereço.

### Relacionamentos

- Um tutor possui zero ou mais Animais.
- Um tutor faz zero ou mais Pedidos.
- Um tutor **pode** ter uma Conta de acesso. Nem todo tutor tem: a clínica
  precisa poder cadastrar quem chega no balcão e nunca vai usar o site.

### Regras estruturais

- O documento de identificação é único: duas fichas para a mesma pessoa
  quebram o histórico do animal.
- Um tutor sem conta de acesso é válido. Uma conta de tutor sem ficha, não.

---

## Animal

O bicho sob cuidado da clínica.

### Responsabilidade

Ser o sujeito do histórico clínico. Toda informação de saúde se organiza em
torno dele, não do tutor.

### Principais informações

- nome;
- espécie e raça;
- data de nascimento;
- peso;
- observações relevantes (alergias, cuidados especiais).

### Relacionamentos

- Um animal pertence a **um** tutor.
- Um animal recebe zero ou mais Agendamentos.
- Um animal acumula zero ou mais Atendimentos.

### Regras estruturais

- Todo animal tem um tutor responsável. Não existe animal sem dono no sistema.
- A troca de tutor é um evento raro e deliberado, não um campo editável como
  outro qualquer.

---

## Colaborador

Quem trabalha na clínica.

### Responsabilidade

Ser o responsável por um atendimento — quem executou o serviço.

### Principais informações

- nome;
- função (veterinário, tosador, atendente);
- contato;
- data de entrada na clínica.

### Relacionamentos

- Um colaborador é responsável por zero ou mais Agendamentos.
- Um colaborador realiza zero ou mais Atendimentos.
- Um colaborador **pode** ter uma Conta de acesso.

### Regras estruturais

- A função determina que tipo de serviço a pessoa pode executar: um serviço
  clínico exige um veterinário.
- Os dados de contato e documento de um colaborador são internos: não são
  informação que um tutor deva receber. O nome e a função, sim — o tutor
  precisa saber quem atendeu o animal dele.

---

## Serviço

O que a clínica oferece: consulta, vacina, banho, tosa.

### Responsabilidade

Definir **quanto tempo** um atendimento ocupa na agenda e quanto custa. A
duração é o que torna a agenda calculável.

### Principais informações

- nome;
- descrição;
- preço;
- duração estimada.

### Relacionamentos

Um serviço aparece em zero ou mais Agendamentos.

### Regras estruturais

- A duração é obrigatória: sem ela não há como saber se dois atendimentos se
  sobrepõem.

---

## Agendamento

O compromisso: um animal, um serviço, um colaborador, um horário.

### Responsabilidade

Reservar um intervalo de tempo de um colaborador. É o conceito onde mora a
regra mais delicada do sistema.

### Principais informações

- animal atendido;
- serviço a ser realizado;
- colaborador responsável;
- data e hora de início;
- situação: marcado, em andamento, concluído ou cancelado;
- observações do tutor.

### Relacionamentos

- Refere-se a **um** animal, **um** serviço e **um** colaborador.
- O tutor do agendamento é o tutor do animal — não é um dado próprio.

### Regras estruturais

- **Dois agendamentos não podem se sobrepor para o mesmo colaborador.** O
  intervalo ocupado vai do início até o início mais a duração do serviço.
  Repare que a sobreposição não exige o mesmo horário de início: um banho de
  90 minutos às 9h conflita com uma consulta às 10h.
- Um agendamento **cancelado** libera o intervalo.
- O histórico do que foi marcado e cancelado tem valor; cancelar não apaga.

---

## Atendimento

O registro do que efetivamente aconteceu com o animal.

> No vocabulário da clínica isto é o **prontuário**. O termo "atendimento" é
> usado aqui para deixar claro que se trata de um evento, não de um documento
> que se sobrescreve.

### Responsabilidade

Preservar o histórico clínico. É a memória do sistema.

### Principais informações

- animal;
- colaborador que realizou;
- data do atendimento;
- diagnóstico;
- tratamento realizado;
- data de retorno, quando houver.

### Relacionamentos

- Pertence a **um** animal.
- Foi realizado por **um** colaborador.
- Pode ter nascido de um Agendamento, mas não depende dele: um atendimento de
  emergência acontece sem agendamento prévio.

### Regras estruturais

- Um atendimento registrado **não é removido**. Correções são feitas por novo
  registro ou por retificação explícita, nunca por apagamento.
- O tutor lê o histórico dos animais dele; quem escreve é a equipe.

---

## Produto

Item vendável do petshop: ração, brinquedo, medicamento, acessório.

### Principais informações

- nome;
- categoria e marca;
- unidade de venda;
- preço.

### Relacionamentos

Um produto aparece em zero ou mais Itens de pedido.

---

## Pedido

Uma compra feita por um tutor no petshop.

### Responsabilidade

Agrupar itens comprados numa única transação e registrar a situação dela.

### Principais informações

- tutor comprador;
- data;
- situação (pendente, pago, enviado, entregue);
- valor total.

### Relacionamentos

- Pertence a **um** tutor.
- Contém um ou mais Itens de pedido.

### Regras estruturais

- O valor total é **derivado** da soma dos itens, não digitado.
- Um pedido sem itens não faz sentido como registro final.

---

## Item do pedido

Uma linha da compra: qual produto, quantos, por quanto.

### Principais informações

- produto;
- quantidade;
- valor unitário no momento da compra;
- valor da linha.

### Relacionamentos

Pertence a **um** pedido e refere-se a **um** produto.

### Regras estruturais

- O valor unitário é **congelado** no momento da compra. Mudar o preço de um
  produto não pode reescrever o histórico de vendas.

---

## O que este modelo não decide

Deliberadamente em aberto, para ser resolvido pelas changes:

- nomes físicos de tabelas e colunas;
- se as situações (do agendamento, do pedido) são texto ou enumeração;
- como o vínculo entre Conta de acesso e Tutor/Colaborador é representado;
- que estrutura garante a não-sobreposição de agendamentos;
- quais conceitos existem já na primeira change e quais chegam depois.

O modelo ser global **não significa** que tudo seja implementado de uma vez.
Ele existe para que a primeira change não tome uma decisão que a quinta
precise desfazer.
