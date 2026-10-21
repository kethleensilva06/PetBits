## Decisions

### D1. Uma compilação por versão do site

O Reflex fixa o prefixo (`frontend_path`) e o endereço do servidor (`api_url`)
na compilação. A versão do Pages é compilada com `/PetBits` e o servidor do
Reflex Cloud; a do Reflex Cloud, sem prefixo. O servidor é o mesmo para as duas
e aceita qualquer origem (`cors_allowed_origins` padrão, `*`).

### D2. A raiz da branch já é /PetBits/

O build prerenderiza as páginas em `PetBits/` (o Reflex as moveria para lá
também). No Pages, a raiz da branch já é servida em `/PetBits/`, então o script
sobe as páginas para a raiz e deixa `assets/`, `fotos/` e o resto onde estão.
Sem os `.gz` (o Pages comprime) e com `.nojekyll`, para ele não esconder
arquivos que começam com `_`.

### D3. Erro do Reflex no Windows, aceito

O último passo do `reflex export` com prefixo usa `PosixPath`, que não existe
no Windows, e quebra. É justamente o passo que move os arquivos para a subpasta
— que o Pages não usa (D2). O script aceita a falha se o build estiver completo
e apontando para o servidor.

### D4. Imagens com o prefixo na tela

O servidor manda `/fotos/...` sem prefixo (é o mesmo para as duas versões). O
prefixo entra na tela, na compilação: `no_site` usa o `frontend_path` da versão
que está sendo compilada, e só muda caminho que começa com "/".
