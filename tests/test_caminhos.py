"""Caminhos das imagens no GitHub Pages (change `site-no-github-pages`)."""

import unittest
from unittest import mock

import reflex as rx

from petbits import caminhos


class _Estado(rx.State):
    foto: str = ""


class NoSiteTest(unittest.TestCase):
    def test_sem_prefixo_nada_muda(self):
        with mock.patch.object(caminhos, "prefixo", return_value=""):
            self.assertEqual(caminhos.no_site("/fotos/banner.webp"), "/fotos/banner.webp")

    def test_com_prefixo_so_o_caminho_local(self):
        with mock.patch.object(caminhos, "prefixo", return_value="/PetBits"):
            self.assertEqual(caminhos.no_site("/fotos/banner.webp"), "/PetBits/fotos/banner.webp")
            foto_do_xano = "https://x.xano.io/vault/foto.webp"
            self.assertEqual(caminhos.no_site(foto_do_xano), foto_do_xano)

    def test_valor_do_servidor(self):
        with mock.patch.object(caminhos, "prefixo", return_value="/PetBits"):
            js = str(caminhos.no_site(_Estado.foto))
        self.assertIn('startsWith("/")', js)
        self.assertIn('"/PetBits"', js)


if __name__ == "__main__":
    unittest.main()
