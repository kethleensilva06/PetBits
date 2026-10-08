# Proposal

## Why

Três coisas que a clínica pediu depois de usar o sistema, e que ele hoje não
sabe fazer.

**A aba não serve para nada.** A tela de entrada tem *Cliente* e
*Colaborador*, e as duas aceitam qualquer conta. Isso foi decisão deliberada
da change anterior — uma aba que recusa é uma aba que responde "esta conta é
da clínica?" a quem só precisa chutar e-mails. Mas o resultado na prática é
uma afirmação falsa na tela: duas abas que não fazem nada. A clínica quer que
a escolha signifique algo, e **dá para atender sem reabrir o oráculo**, desde
que a recusa aconteça só depois de a senha estar conferida.

**Toda conta de equipe é igual.** As oito contas da clínica têm o mesmo papel
`admin` e alcançam exatamente as mesmas coisas. Um atendente pode apagar o
cadastro de um veterinário. A clínica quer que manter o quadro de pessoal seja
da gerência, e isso não existe: o sistema tem dois papéis, tutor e equipe, e
nada entre eles.

**Não dá para ver a senha que se digitou.** Numa tela onde a recusa é genérica
de propósito — "credenciais inválidas", sem dizer o quê —, errar a senha e não
poder conferir o que foi digitado é atrito gratuito.

## What Changes

- Papel novo: **`staff`**, a equipe comum. `admin` passa a significar
  **gerência**. Tutor continua `member`.
- **Manter colaboradores** passa a exigir gerência. Ler continua sendo de toda
  a equipe.
- A **aba escolhida passa a valer**: conta de equipe não entra pela aba
  Cliente, conta de tutor não entra pela aba Colaborador.
- A tela de entrada ganha o **olho de ver a senha**.

### Como a aba passa a valer sem virar oráculo

A recusa por aba errada acontece **depois** de a senha ter sido conferida, e
não antes. Com credencial errada ou ausente, as duas abas continuam
indistinguíveis em status, corpo, tempo e número de requisições — que é a
propriedade crítica que a change anterior estabeleceu e que esta **não**
afrouxa.

Quem acertou a senha já sabe de quem é a conta. Dizer a essa pessoa "esta
conta é de colaborador, entre pela outra aba" não entrega informação nova. A
quem está chutando e-mails, nada muda.

### Fora do escopo

- **Editar tutor pela clínica.** A tela de tutores continua só leitura, e
  continua aberta a toda a equipe: contato de cliente é o trabalho do
  atendente. A regra de gerência para esse dado entra quando a edição existir.
- **Serviços.** Manter o catálogo continua sendo de toda a equipe.
- **Promover alguém pela aplicação.** Continua acontecendo fora dela, agora
  com três valores em vez de dois.
- Recuperação de senha, e qualquer mudança na verificação de credencial.

## Capabilities

### Modified Capabilities

- `autenticacao`: a aba escolhida passa a ser respeitada **depois** da
  verificação de credencial, e a tela ganha o olho de ver a senha.
- `acesso-da-equipe`: passa a haver dois níveis dentro da equipe — gerência e
  equipe comum — e o que cada um alcança.
- `colaboradores`: manter o quadro passa a exigir gerência.

## Impact

**Xano** (`workspace 169225`)

- `user.role` ganha o valor `staff`.
- Função nova para "esta credencial é da gerência?", irmã da que já existe
  para "é da equipe?".
- Os quatro endpoints de escrita de colaborador passam a exigir gerência; os
  outros sete de equipe não mudam.

**Aplicação Reflex**

- A entrada compara o papel devolvido por `/auth/me` com a aba escolhida.
- A área da clínica esconde o que a conta não alcança — **esconder é
  conveniência; quem recusa é o Xano.**
- Campo de senha com o olho, nas duas telas que pedem senha.

**Restrições a respeitar**

- A indistinguibilidade das duas abas **antes** de uma senha correta é
  requisito, não preferência.
- O papel continua vindo do banco a cada requisição, nunca do token nem do
  cliente.
- Papel desconhecido continua sendo negado por igualdade, nunca por negação.
