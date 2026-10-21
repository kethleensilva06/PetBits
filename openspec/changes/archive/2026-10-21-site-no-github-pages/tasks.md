## 1. Pages

- [x] 1.1 `scripts/publicar_no_github_pages.py`, com testes
- [x] 1.2 `petbits/caminhos.py` e `no_site` nas imagens, com testes
- [x] 1.3 Branch `gh-pages` enviada e o Pages trocado da `main` para ela
- [x] 1.4 README

## 2. Verificação

- [x] 2.1 Testes locais passam
- [x] 2.2 No Pages: `/`, `/boas-vindas`, `/loja`, `/entrar` respondem; a raiz leva a `/PetBits/boas-vindas` e `/loja` sem sessão a `/entrar` (o servidor do Reflex Cloud responde); as quatro fotos da página inicial carregam de `/PetBits/fotos/`; o arquivo de ambiente do navegador só tem os endereços do servidor
- [x] 2.3 Local: as fotos continuam em `/fotos/` e carregam

Achados: Git Bash converteu `/PetBits` em `C:/Program Files/Git/PetBits`
(conversão automática de caminho do MSYS); o script em Python não passa por
isso. O GitHub Pages não reconstruiu sozinho ao trocar de branch; foi preciso
pedir um build.
