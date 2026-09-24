"""Cores e rótulos dos campos de domínio fechado.

Os status circulam pelo sistema como os valores crus do banco (`em_andamento`,
`concluido`). Quem traduz para texto legível e para cor é este módulo — não as
páginas, que antes repetiam o mesmo `rx.match` em cada tabela.

Por que `grass` e não `green` no sucesso: o accent do tema é `jade`, e
`jade-11` (#208368) e `green-11` (#218358) são praticamente a mesma cor. Um
badge "concluído" em verde sumiria dentro da identidade — ninguém distinguiria
"isto é a marca" de "isto deu certo". O `grass-11` (#2a7e3b) é um verde-folha
mais amarelado, a uns 40° de matiz do jade, e se separa.
"""

import reflex as rx

STATUS_AGENDAMENTO_CORES = {
    "agendado": "indigo",       # planejado, ainda vai acontecer
    "em_andamento": "amber",    # acontecendo agora — é o que pede atenção
    "concluido": "grass",
    "cancelado": "red",
}

STATUS_PEDIDO_CORES = {
    "pendente": "amber",
    "pago": "indigo",
    "enviado": "violet",
    "entregue": "grass",
}

# O banco guarda sem acento e com underscore; a tela não precisa mostrar isso.
STATUS_ROTULOS = {
    "agendado": "Agendado",
    "em_andamento": "Em andamento",
    "concluido": "Concluído",
    "cancelado": "Cancelado",
    "pendente": "Pendente",
    "pago": "Pago",
    "enviado": "Enviado",
    "entregue": "Entregue",
}

CARGO_ROTULOS = {
    "veterinario": "Veterinário",
    "tosador": "Tosador",
    "atendente": "Atendente",
}


def de_mapa(valor, mapa: dict[str, str], padrao: str = "gray"):
    """Traduz um Var usando um dicionário Python.

    Um Var do Reflex não indexa um dict em tempo de compilação, então o jeito
    de fazer essa tradução é montar um `rx.match` a partir dos pares.
    """
    return rx.match(valor, *mapa.items(), padrao)
