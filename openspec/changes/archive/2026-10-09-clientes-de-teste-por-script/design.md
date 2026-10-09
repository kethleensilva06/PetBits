## Context

- O cadastro público (`POST tutor/cadastro`) cria conta e ficha juntas, e
  recusa e-mail ou CPF repetido com uma mensagem genérica.
- `petbits/xano.py` já tem `cadastrar_tutor`, usado pela tela de cadastro.
- `contas-de-teste.local.txt` é ignorado pelo git e alimenta o `Alt+2`.

## Decisions

### D1 — O script usa a mesma função da tela

`xano.cadastrar_tutor`, e não uma requisição montada à parte: o que o script
cria é exatamente o que um cliente criaria pela tela, e uma mudança no
cadastro não deixa o script para trás.

### D2 — Dados que não colidem com gente de verdade

- E-mail `cliente.teste.<carimbo>.<n>@exemplo.com`: `exemplo.com` é domínio
  reservado para exemplo, e o carimbo de tempo torna cada rodada única.
- CPF com dígitos verificadores válidos, gerado ao acaso. A chance de bater
  num CPF já cadastrado é desprezível; se bater, o cadastro recusa e o script
  segue (cenário da spec).
- Senha de 12 caracteres com `secrets`, sempre com letra e dígito.

### D3 — Grava depois de criar, um por um

Cada cliente vai para o arquivo logo depois de o cadastro confirmar. Uma
falha no meio deixa no arquivo exatamente os que existem, e nenhum que não
existe.

### D4 — Pausa pelo orçamento de requisições

2,2 segundos entre cadastros, a mesma folga de `teste_duas_contas.py`: o
limite de 10 requisições a cada 20 segundos é da instância, e o script não
pode derrubar a tela de quem estiver usando o sistema.

## Risks / Trade-offs

- [As contas ficam na base] → São de domínio `exemplo.com`, fáceis de achar e
  apagar no painel; apagar fica fora do escopo.
