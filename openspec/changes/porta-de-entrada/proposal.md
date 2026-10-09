## Why

Quem abre o PetBits cai direto num formulário de login com duas abas, e os
funcionários não acham por onde entrar na gerência — a aba Colaborador é uma
etiqueta pequena acima dos campos. A clínica pediu uma página inicial antes
do login e duas entradas separadas: uma para clientes e outra para
funcionários.

## What Changes

- **Página inicial pública** (`/boas-vindas`): o que é o PetBits e três
  caminhos — **Sou cliente**, **Sou da equipe** e **Criar conta**. Quem abre
  o endereço do sistema sem sessão chega aqui.
- **Entrada de clientes** (`/entrar`): formulário de login com "Criar conta".
- **Entrada da equipe** (`/entrar/equipe`): formulário de login próprio, sem
  "Criar conta" — contas de equipe são dadas pela clínica.
- As abas Cliente/Colaborador **saem**. Depois da senha aceita, **conta de
  equipe vai sempre para a gerência**, por qualquer entrada, e qualquer outra
  conta vai para a área de cliente.
- **Funcionário não usa a área de cliente:** quem é da equipe e abre `/` ou
  `/agenda` é levado à gerência, sem carregar dado de cliente. (Mudança de
  rumo pedida pela clínica durante a aplicação — ver D5.)
- **Não muda:** as duas páginas usam o mesmo formulário, o mesmo manipulador
  e o mesmo endpoint, a página nunca é enviada ao servidor, e a recusa é a
  mesma nas duas. Conta que não é de equipe nunca vai para a gerência.
- Os atalhos `Alt+1` e `Alt+2` funcionam nas duas páginas.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `autenticacao`: página inicial pública; entrada separada por público no
  lugar das abas; destino do visitante sem sessão.

## Fora do escopo

- Conteúdo de vitrine na página inicial (fica para a change da loja).
- Recuperação de senha.
- Mudar a regra de quem é equipe: continua sendo `role = admin` na conta.

## Impact

- Código: `petbits/pages/entrar.py` (duas páginas, página inicial),
  `petbits/states/auth_state.py` (qual entrada está aberta),
  `petbits/petbits.py` (rotas). Nenhum endpoint muda.
