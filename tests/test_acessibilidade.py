"""Acessibilidade (change `acessibilidade`)."""

import re
import unittest
from pathlib import Path

import reflex as rx

from petbits.visual import campo

RAIZ = Path(__file__).resolve().parent.parent


def _contraste(a: str, b: str) -> float:
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    x, y = sorted([lum(a), lum(b)])
    return (y + 0.05) / (x + 0.05)


class CoresTest(unittest.TestCase):
    def test_branco_sobre_os_solidos(self):
        css = (RAIZ / "assets/estilo.css").read_text(encoding="utf-8")
        for var in ("--teal-9", "--teal-10", "--orange-9", "--orange-10"):
            cor = re.search(var + r":\s*(#[0-9a-fA-F]{6})", css).group(1)
            self.assertGreaterEqual(_contraste(cor, "#ffffff"), 4.5, var)

    def test_texto_nao_usa_cinza_claro(self):
        """O cinza 9 e 10 do Radix dão 3,3 e 3,9 sobre branco (D2)."""
        for arquivo in list((RAIZ / "petbits").rglob("*.py")):
            fonte = arquivo.read_text(encoding="utf-8")
            self.assertIsNone(re.search(r'rx\.color\("gray", (9|10)\)', fonte), arquivo.name)

    def test_foco_visivel(self):
        css = (RAIZ / "assets/estilo.css").read_text(encoding="utf-8")
        self.assertRegex(css, r":focus-visible\s*\{[^}]*outline:")


class NomesTest(unittest.TestCase):
    def test_campo_da_o_rotulo_ao_campo(self):
        self.assertIn('"aria-label":"Nome"', str(campo("Nome", rx.input(value=""))))
        lista = campo("Animal", rx.select.root(rx.select.trigger(), rx.select.content()))
        self.assertIn('"aria-label":"Animal"', str(lista))

    def test_campo_com_on_change(self):
        """Com `on_change`, o Reflex embrulha o campo num `DebounceInput`."""
        class _Estado(rx.State):
            valor: str = ""

            def set_valor(self, v: str):
                self.valor = v

        texto = str(campo("Telefone", rx.input(value=_Estado.valor, on_change=_Estado.set_valor)))
        self.assertIn('"aria-label":"Telefone"', texto)

    def test_campo_aninhado(self):
        caixa = rx.hstack(rx.input(type="password"), rx.icon_button(rx.icon("eye")))
        self.assertIn('"aria-label":"Senha"', str(campo("Senha", caixa)))

    def test_nenhuma_pagina_tem_campo_proprio(self):
        for arquivo in (RAIZ / "petbits/pages").glob("*.py"):
            self.assertNotIn("def _campo(", arquivo.read_text(encoding="utf-8"), arquivo.name)

    def test_pagina_em_portugues(self):
        fonte = (RAIZ / "petbits/petbits.py").read_text(encoding="utf-8")
        self.assertIn('html_lang="pt-BR"', fonte)


if __name__ == "__main__":
    unittest.main()
