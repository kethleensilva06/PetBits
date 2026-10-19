"""A escolha da ilustração (change `cliente-ilustrado`, D2)."""

import os
import unittest

from petbits.ilustracoes import imagem_da_categoria, imagem_da_especie
from petbits.rotulos import CATEGORIAS_PRODUTO

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")


class EspecieTest(unittest.TestCase):
    def test_cao_escrito_de_varios_jeitos(self):
        for especie in ("Cachorro", "cão", " CAO ", "Cadela"):
            self.assertEqual(imagem_da_especie(especie), "/ilustracoes/cao.svg", especie)

    def test_gato(self):
        for especie in ("Gato", "gata", "GATINHO"):
            self.assertEqual(imagem_da_especie(especie), "/ilustracoes/gato.svg", especie)

    def test_desconhecida_vazia_ou_ausente(self):
        for especie in ("Calopsita", "", None, "-"):
            self.assertEqual(imagem_da_especie(especie), "/ilustracoes/outro.svg", especie)


class CategoriaTest(unittest.TestCase):
    def test_cada_categoria_tem_a_sua(self):
        for chave in CATEGORIAS_PRODUTO:
            self.assertEqual(imagem_da_categoria(chave), f"/ilustracoes/produto-{chave}.svg")

    def test_sem_categoria_cai_na_sacola(self):
        for chave in (None, "", "Ração", "eletronico"):
            self.assertEqual(imagem_da_categoria(chave), "/ilustracoes/produto-outro.svg")


class ArquivosTest(unittest.TestCase):
    """Toda imagem que as funções podem devolver existe de fato em `assets/`."""

    def test_arquivos_existem(self):
        caminhos = {imagem_da_especie(e) for e in ("cão", "gato", "outro")}
        caminhos |= {imagem_da_categoria(c) for c in list(CATEGORIAS_PRODUTO) + [None]}
        caminhos |= {f"/ilustracoes/{n}.svg" for n in
                     ("banner", "vazio-animais", "vazio-pedidos", "vazio-agenda")}
        for caminho in caminhos:
            self.assertTrue(os.path.isfile(os.path.join(ASSETS, caminho.lstrip("/"))), caminho)


if __name__ == "__main__":
    unittest.main()
