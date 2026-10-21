"""Esqueletos no lugar do spinner de carga (change `esqueletos-de-carregamento`)."""

import re
import unittest
from pathlib import Path

import reflex as rx

from petbits import esqueletos

PAGINAS = sorted(Path(__file__).resolve().parent.parent.glob("petbits/pages/*.py"))


class SemSpinnerDeCargaTest(unittest.TestCase):
    def test_nenhuma_pagina_tem_spinner_com_carregando(self):
        """O spinner em botão (enviando foto) fica (D4); o de carga de tela, não."""
        for pagina in PAGINAS:
            fonte = pagina.read_text(encoding="utf-8")
            achado = re.search(r"rx\.spinner\([^\n]*\n?[^\n]*(Carregando|Buscando)", fonte)
            self.assertIsNone(achado, pagina.name)


class AcessivelTest(unittest.TestCase):
    def test_todo_esqueleto_avisa_o_leitor_de_tela(self):
        for componente in (esqueletos.cartoes("Carregando a loja..."),
                           esqueletos.linhas("Carregando os pedidos..."),
                           esqueletos.perfil("Carregando o perfil..."),
                           esqueletos.fichas("Buscando horários...")):
            codigo = str(componente.render())
            self.assertIn("status", codigo)
            self.assertIn("aria-busy", codigo.replace("ariaBusy", "aria-busy").replace("aria_busy", "aria-busy"))


if __name__ == "__main__":
    unittest.main()
