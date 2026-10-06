"""A guarda de acesso que todo State privado usa.

Mora num módulo próprio porque passou a ter dois usuários. Duas classes
`SemSessao` em arquivos diferentes seriam tipos **diferentes**, e um
`except SemSessao` pegaria uma e deixaria a outra subir — o tipo de defeito
que só aparece quando alguém já está sem sessão.

**A guarda é o `raise` daqui, lido por um `return` antecipado dentro de cada
loader — não um `rx.redirect` no `on_load`.** `rx.redirect` é evento de
frontend e não cancela o que já está na fila do backend: o carregamento
enfileirado depois rodaria assim mesmo e a requisição sairia. Esconder a tela
sem impedir a requisição não esconde nada.
"""


class SemSessao(Exception):
    """Não há sessão válida para esta tela. `destino` é para onde mandar.

    Os dois destinos querem dizer coisas diferentes:

    - `/entrar` — não há sessão nenhuma;
    - `/` — há sessão, mas não é de equipe, então a área da clínica não é
      para esta pessoa.

    O segundo caso é **conveniência de interface**. Quem protege é o backend,
    que lê o papel do banco a cada requisição e recusa com 403 mesmo que a
    tela seja forjada no armazenamento local.
    """

    def __init__(self, destino: str = "/entrar"):
        super().__init__(destino)
        self.destino = destino
