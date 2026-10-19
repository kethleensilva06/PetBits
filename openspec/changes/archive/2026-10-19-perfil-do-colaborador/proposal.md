## Why

Desde a `perfil-e-fotos`, o cliente toca no próprio avatar e cuida dos seus
dados, da senha e da foto. Quem trabalha na clínica não tem nada parecido:
para corrigir o próprio telefone, o colaborador depende da gerência, e para
trocar a senha não tem caminho nenhum. A área da clínica deveria ter o mesmo
"meu perfil" que a área do cliente.

De passagem apareceu um defeito da `perfil-e-fotos`: quando o tutor muda o
nome, o cabeçalho mostra o novo nome só até sair. Na entrada seguinte volta o
antigo, porque a saudação vem da conta de acesso (`user.name`), e só a ficha
de tutor foi alterada.

## What Changes

- **Meu perfil na área da clínica** (`/equipe/perfil`): quem é da equipe toca
  no próprio avatar, no topo da clínica, e altera nome e telefone, troca a
  senha (pedindo a atual) e envia uma foto. E-mail, função e data de entrada
  aparecem, mas travados: são definidos pela gerência.
- **Ligação pelo e-mail:** a ficha de colaborador de quem entrou é a que tem o
  mesmo e-mail da conta. Nada novo é criado nem concedido: colaborador
  continua sendo registro, não credencial. Conta de equipe sem ficha com o
  mesmo e-mail vê só a troca de senha e um aviso para procurar a gerência.
- **Backend (Xano):** coluna opcional `foto` em `colaborador`;
  `GET` e `PATCH equipe/meu-perfil` e `POST equipe/meu-perfil/foto`, com a
  prova de equipe e a ficha achada pelo e-mail da conta do token. A troca de
  senha usa o `POST me/senha`, que já serve a qualquer conta.
- **Nome que dura:** alterar o nome no perfil (do tutor ou do colaborador)
  também altera o nome da conta de acesso, para a saudação continuar certa
  depois de sair e entrar.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `colaboradores`: o colaborador altera os próprios dados e a foto.
- `tutores`: o nome alterado no perfil vale também para a conta de acesso.

## Fora do escopo

- O colaborador mudar a própria função, o e-mail, a data de entrada ou o
  ativo: continua só pela gerência (`equipe/colaboradores/{id}`).
- Ligar conta e ficha por um campo próprio (`id_user`); por ora o e-mail
  basta, e a gerência é quem o mantém.
- Tirar a marca "Powered by Xano" das fotos enviadas: o plano gratuito do Xano
  não permite (medido na sessão de 19/10), e a decisão de plano ou de
  armazenamento é sua.

## Impact

- Xano: `tables/colaborador.xs`; três endpoints novos `equipe_meu_perfil_*`;
  `me_tutor_update.xs` passa a alterar também o nome da conta.
- Reflex: página `/equipe/perfil`, `PerfilEquipeState`, `petbits/xano.py`,
  topo da área da clínica em `petbits/pages/equipe.py`, `AuthState`.
- Testes: os de `tests/` continuam; as provas vão contra o Xano e na tela.
