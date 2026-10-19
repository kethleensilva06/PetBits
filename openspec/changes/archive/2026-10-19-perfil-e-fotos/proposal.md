## Why

O tutor cadastra-se uma vez e depois não tem como corrigir nada: mudou de
telefone, de endereço, quer trocar a senha — precisa ligar para a clínica.
E o animal dele aparece com uma foto genérica da espécie, quando ele tem no
celular a foto do próprio bicho. Ver o próprio animal na tela é o que faz a
área do cliente parecer dele.

## What Changes

- **Meu perfil:** o tutor toca no próprio avatar, no cabeçalho, e abre a tela
  de perfil. Ali altera nome, telefone e endereço, troca a senha (pedindo a
  atual) e envia uma foto de perfil. CPF e e-mail aparecem, mas travados.
- **Foto do animal:** no diálogo de edição do animal, o tutor envia uma foto;
  o cartão passa a mostrá-la no lugar da foto genérica da espécie.
- **Backend (Xano):**
  - colunas opcionais `foto` (imagem) em `tutor` e `pet`;
  - `PATCH me/tutor` — altera nome, telefone e endereço da ficha do token;
  - `POST me/senha` — troca a senha conferindo a atual;
  - `POST me/tutor/foto` e `POST pet/{pet_id}/foto` — recebem a imagem,
    conferem tipo e tamanho e gravam, sempre com o dono vindo do token.
- `docs/project-overview.md` registra que foto de perfil (tutor e animal)
  entra no escopo; anexo de imagem no prontuário continua fora.

## Capabilities

### New Capabilities

Nenhuma.

### Modified Capabilities

- `tutores`: o tutor altera os próprios dados de contato e a foto.
- `animais`: o animal ganha foto, enviada pelo dono.
- `autenticacao`: troca de senha pelo próprio tutor.

## Fora do escopo

- Alterar CPF ou e-mail pelo próprio tutor (continuam pela clínica).
- Recuperação de senha esquecida por e-mail.
- A equipe enviar ou trocar fotos.
- Recorte ou edição da imagem na tela; a foto vai como foi escolhida, só
  conferida em tipo e tamanho.
- Foto no prontuário, de exame ou de atendimento.

## Impact

- Xano: `tables/tutor.xs`, `tables/pet.xs`; quatro endpoints novos;
  publicação por `scripts/publicar.py`.
- Reflex: página `/perfil`, `PerfilState`, `petbits/xano.py`, `PetState`,
  `topo_do_cliente`, `inicio.py`.
- Docs: `docs/project-overview.md`.
- Dependências: nenhuma nova (upload pelo `rx.upload` do Reflex; envio ao
  Xano pelo `httpx` que o projeto já usa).
