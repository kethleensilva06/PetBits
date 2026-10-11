# Design

## Context

Ver `proposal.md` — Why. O que condiciona o desenho:

- A change anterior estabeleceu, e **mediu**, uma propriedade: com credencial
  errada, as duas abas são indistinguíveis em status, corpo, tempo e número de
  requisições. O `entrar.xs` existe por causa dela, e ela custou caro —
  inclusive um hash de descarte gerado pelo próprio Xano, porque o motor não
  aceita bcrypt.
- `user.role` é `enum role?` com `["admin", "member"]`, e **opcional**. As oito
  contas de equipe são todas `admin`.
- `exige_equipe` compara por igualdade contra o literal `"admin"`, e os onze
  endpoints `equipe/*` a chamam como segunda instrução.
- A guarda de repositório exige que todo `apis/pet_bits/equipe_*.xs` chame a
  prova, e que ninguém fora deles a chame.

## Goals / Non-Goals

**Goals:**

- Fazer a aba significar algo **sem** afrouxar a propriedade medida.
- Criar o terceiro papel de um jeito que continue falhando fechado: papel
  ausente, vazio ou desconhecido não alcança nada.

**Non-Goals:**

- Editar tutor pela clínica. A leitura continua aberta a toda a equipe.
- Restringir serviços. Manter o catálogo segue sendo de toda a equipe.
- Promover alguém pela aplicação.

## Decisions

### D1 — A aba vale, mas só depois da senha

A change anterior decidiu que a aba não participava de nada, e o motivo era
sólido: uma aba que recusa responde "esta conta é da clínica?" a quem só
precisa chutar e-mails. A clínica pediu o contrário, e as duas coisas cabem
juntas — **porque o que precisa ser protegido não é a aba, é o que se aprende
antes de ter a senha.**

A regra precisa, que substitui "a aba não participa de nada":

> A aba MAY decidir o que acontece **depois** de uma credencial correta.
> Antes disso, nada — status, corpo, tempo, número de requisições — pode
> depender dela.

Quem acertou a senha já sabe de quem é a conta; dizer "esta é de colaborador"
não entrega nada. Quem errou continua sem aprender se o e-mail existe, se tem
conta, ou que papel ela tem.

**Como isso se traduz em código:** a aba continua **não sendo enviada ao
servidor**. O `POST /entrar` e o `GET /auth/me` são byte a byte os mesmos nas
duas abas, na mesma ordem, sempre dois. A comparação acontece **no Reflex**,
depois do `/auth/me`, sobre o papel que o servidor devolveu. Se não combinar,
a sessão que acabou de ser aberta é **descartada** e a pessoa volta à tela com
a orientação.

Duas consequências que valem estar escritas:

- **O token chega a ser emitido.** A recusa é da aplicação, não da
  autenticação: o Xano criou a sessão e nós a jogamos fora. Não é falha — é o
  preço de manter as duas requisições idênticas. Fazer o backend recusar
  exigiria contar a ele qual aba foi usada, que é exatamente o que não pode.
- **Isto é conveniência de interface, não barreira.** Quem chamar
  `POST /entrar` direto entra, porque a aba não existe para o backend. E está
  certo: um colaborador com a senha dele alcançando a própria conta por fora
  da tela não é violação de nada. A barreira de verdade continua sendo o
  papel, conferido no banco a cada requisição.

### D2 — O terceiro papel, e por que ele é `staff` e não "não-admin"

`user.role` ganha `"staff"`. `admin` passa a significar **gerência**;
`member` continua tutor.

A tentação é não criar valor nenhum: "quem é gerente está na ficha de
colaborador, basta olhar lá". **Não.** A ficha de colaborador não liga a conta
nenhuma — foi decisão explícita da change anterior — e, se ligasse, derivar
permissão do cargo faria qualquer conta com escrita em `colaborador` conceder
acesso a si mesma. O cargo descreve o trabalho; o papel decide o alcance; um
não se lê do outro.

**A conferência continua por igualdade, agora contra dois literais:**

```
precondition (($conta.role == "admin") || ($conta.role == "staff"))
```

Não `!= "member"`. A diferença é a mesma de antes e continua sendo a que
importa: `!= "member"` deixa entrar papel vazio, papel com erro de digitação e
qualquer valor futuro que alguém acrescente ao enum sem pensar nesta linha.
Igualdade contra os valores esperados falha fechada em todos esses casos.

### D3 — Duas funções, não um parâmetro de nível

`PetBits/exige_equipe` passa a aceitar `admin` **ou** `staff`.
`PetBits/exige_gerencia` é nova e aceita só `admin`.

A alternativa era uma função com um parâmetro de nível. Recusada pelo mesmo
motivo que a `enforce_role` do template foi, e vale repetir porque a tentação
volta: um parâmetro cria a pergunta "o que acontece se ele vier errado, vazio
ou ausente?", e a resposta certa exige mais uma guarda. Duas funções sem
parâmetro não têm essa pergunta — cada uma sabe uma coisa só, e o endpoint
escolhe qual chamar.

**Quem chama qual:**

| Endpoint | Prova |
|---|---|
| `equipe/painel`, `equipe/servicos*`, `equipe/tutores`, `equipe/animais`, `equipe/colaboradores` (GET) | `exige_equipe` |
| `equipe/colaboradores` (POST), `equipe/colaboradores/{id}` (PATCH) | `exige_gerencia` |

A guarda de repositório precisa aprender isso: hoje ela exige que todo
`equipe_*.xs` chame `exige_equipe`. Passa a aceitar **uma das duas**, e ganha
uma conferência nova — que `exige_gerencia` apareça **exatamente** nos dois
arquivos de escrita de colaborador. Sem isso, trocar uma prova pela outra por
engano passaria limpo, e é o tipo de troca que ninguém nota lendo o diff.

### D4 — A migração é o momento perigoso

Oito contas são `admin` hoje. Depois desta change, `admin` quer dizer outra
coisa — e **quem não for rebaixado continua com o alcance antigo**. O erro não
é alguém perder acesso; é alguém mantê-lo sem que ninguém perceba, porque a
tela não muda para quem já podia tudo.

Então a migração é explícita, conta a conta, e conferida depois:

- ficam `admin`: Carla, Patricia, Rafael, Sandra (as de cargo gerente)
- viram `staff`: Thiago, Letícia, Bianca, Otávio

A conferência pós-migração é `role == "admin"` entre quem **não** deveria ser
gerência — o espelho da conferência da change anterior, que procurava
`role != "admin"` entre quem deveria. O erro mudou de direção junto com o
significado do valor, e a conferência antiga, rodada hoje, não acusaria nada.

### D5 — O olho da senha

Um botão dentro do campo que alterna `type` entre `password` e `text`.

Duas coisas que parecem detalhe e não são: ele **começa oculto**, e o estado
de "revelado" **não sobrevive** a sair da tela. Um campo que lembra que estava
visível é um campo que mostra a senha para a próxima pessoa que abrir o
navegador — num computador de recepção, que é onde este sistema vai rodar.

## Risks / Trade-offs

**A recusa por aba acontece depois de uma sessão ter sido aberta.** O token
existe por um instante e é descartado. Em termos de segurança isso não concede
nada — a pessoa tinha a senha —, mas o `event_log` registra uma entrada que a
tela recusou, e quem for ler o log vai ver "entrou" onde a pessoa jurará que
não entrou. Vale uma linha na documentação de operação.

**A aba é conveniência, não barreira, e a tela vai parecer que é.** Alguém vai
concluir que colaborador "não consegue" entrar pelo lado do cliente e construir
algo em cima disso. Não consegue *pela tela*. Por `curl`, consegue — e tem de
conseguir, senão a aba teria de chegar ao backend.

**Equipe comum vê a lista de tutores inteira**, com documento, telefone e
endereço. Foi decisão explícita desta change — o atendente precisa do contato
—, mas amplia o que já estava registrado como risco: uma credencial de equipe
comprometida continua sendo a base de clientes inteira, e agora há mais
credenciais com menos supervisão.

**O enum `role` passa a ter três valores e continua opcional.** Conta criada à
mão sem papel não alcança nada — falha fechada —, mas agora há duas formas de
errar a criação em vez de uma, e a mais provável é criar gerência como `staff`
e descobrir só quando a pessoa tentar editar.

## Migration Plan

1. Acrescentar `staff` ao enum de `user.role` — sozinho, antes de qualquer
   endpoint, porque gravar o valor novo depende dele.
2. `exige_gerencia`, e `exige_equipe` aceitando os dois valores.
3. Os dois endpoints de escrita de colaborador trocam de prova.
4. **Rebaixar as quatro contas**, e rodar a conferência do D4.
5. Reflex: a comparação de aba, o esconder dos controles, o olho da senha.

A ordem importa num ponto: enquanto o passo 2 não estiver no ar, `exige_equipe`
ainda compara só contra `"admin"`, e uma conta já rebaixada para `staff`
perderia acesso a tudo. Por isso o rebaixamento vem **depois** das funções, e
não antes.
