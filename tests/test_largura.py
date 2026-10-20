"""Todas as abas do cliente têm a mesma largura (change `mesma-largura-no-cliente`).

A Loja usava a largura 4 do container e as outras a 3, e o cabeçalho "pulava"
ao trocar de aba. O teste lê a fonte de cada página do cliente e confere que o
container usa a constante, e não um número solto.
"""

import inspect
import re
import unittest

from petbits.pages import agenda, inicio, loja, perfil

PAGINAS_DO_CLIENTE = (inicio.inicio_page, agenda.agenda_page, loja.loja_page,
                      loja.pedidos_page, perfil.perfil_page)


class LarguraTest(unittest.TestCase):
    def test_toda_pagina_do_cliente_usa_a_constante(self):
        for pagina in PAGINAS_DO_CLIENTE:
            fonte = inspect.getsource(pagina)
            self.assertIn("rx.container(", fonte, pagina.__name__)
            self.assertIn("size=LARGURA_DO_CLIENTE", fonte, pagina.__name__)

    def test_nenhuma_declara_um_numero_no_container(self):
        for pagina in PAGINAS_DO_CLIENTE:
            final = inspect.getsource(pagina).rstrip()[-80:]
            self.assertIsNone(re.search(r'size="[1-4]",\s*\)$', final), pagina.__name__)


if __name__ == "__main__":
    unittest.main()
