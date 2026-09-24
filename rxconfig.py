import reflex as rx

# O banco de dados do PetBits fica no Xano e é acessado por HTTP
# (petbits/xano.py). O Reflex, portanto, não recebe db_url: nada neste projeto
# usa o ORM interno dele. As credenciais do Xano vêm do arquivo .env.
#
# Sobre o tema:
# - `jade` em vez de `teal` — o teal puxa para o ciano e lê como hospital;
#   o jade é o mesmo nível de saturação deslocado para o verde puro.
# - `gray_color="sand"` é o que entrega o tom acolhedor. Sem declarar, o Radix
#   escolhe `sage` (cinza esverdeado) e a tela inteira fica monocromática e
#   fria. O `sand` é um cinza quente, cor de papel, que contrasta com o verde.
# - `panel_background="solid"` porque o padrão translúcido suja os cartões
#   sobre tabelas densas.
# - `appearance` não é declarado de propósito: o color mode do Reflex sobrescreve
#   a classe do nó raiz, então fixar "light" aqui seria afirmar algo que o
#   próprio framework contradiz logo depois.
config = rx.Config(
    app_name="petbits",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(
                accent_color="jade",
                gray_color="sand",
                radius="large",
                scaling="100%",
                panel_background="solid",
            )
        ),
    ],
)
