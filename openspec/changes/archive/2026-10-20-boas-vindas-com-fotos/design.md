## Decisions

### D1. Fotos que o app já tem

Capa: `banner.webp` (cão e gato). Clínica: `vazio-agenda.webp` (chihuahua
em consulta). Banho e tosa: `produto-higiene.webp` (cão na banheira).
Petshop: `vazio-pedidos.webp` (dachshund na caixa). Todas têm crédito em
`assets/fotos/CREDITOS.md`; reaproveitar evita downloads e mantém a
identidade das telas de dentro.

### D2. Nenhuma requisição

A página continua sem `on_load` que chame o Xano (`porta-de-entrada`, D4):
só `redirecionar_se_logado`. As fotos vêm de `/fotos/`, servidas com o app.

### D3. Capa em duas colunas, uma no celular

Texto à esquerda e foto à direita em tela larga; no celular, a foto vem
primeiro, mais baixa, para o título e os botões ficarem na primeira tela.
Toda foto tem `alt` descritivo e `object_fit="cover"`, sem esticar.

### D4. Os caminhos ficam

Os três cartões (Sou cliente, Sou da equipe, Primeira vez?) são o que a
especificação exige da página. Eles descem para depois da faixa de serviços;
a capa já oferece Entrar e Criar conta para o cliente.
