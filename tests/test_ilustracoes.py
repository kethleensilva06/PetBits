"""A escolha da imagem (changes `cliente-ilustrado` e `fotos-realistas`)."""

import os
import unittest

from petbits.ilustracoes import (chave_do_produto, imagem_da_categoria, imagem_da_especie,
                                 imagem_do_produto)
from petbits.rotulos import CATEGORIAS_PRODUTO

ASSETS = os.path.join(os.path.dirname(__file__), "..", "assets")


class EspecieTest(unittest.TestCase):
    def test_cao_escrito_de_varios_jeitos(self):
        for especie in ("Cachorro", "cão", " CAO ", "Cadela"):
            self.assertEqual(imagem_da_especie(especie), "/fotos/cao.webp", especie)

    def test_gato(self):
        for especie in ("Gato", "gata", "GATINHO"):
            self.assertEqual(imagem_da_especie(especie), "/fotos/gato.webp", especie)

    def test_desconhecida_vazia_ou_ausente(self):
        for especie in ("Calopsita", "", None, "-"):
            self.assertEqual(imagem_da_especie(especie), "/fotos/outro.webp", especie)


class CategoriaTest(unittest.TestCase):
    def test_cada_categoria_tem_a_sua(self):
        for chave in CATEGORIAS_PRODUTO:
            self.assertEqual(imagem_da_categoria(chave), f"/fotos/produto-{chave}.webp")

    def test_sem_categoria_cai_na_sacola(self):
        for chave in (None, "", "Ração", "eletronico"):
            self.assertEqual(imagem_da_categoria(chave), "/fotos/produto-outro.webp")


class ProdutoTest(unittest.TestCase):
    def test_chave_do_nome(self):
        self.assertEqual(chave_do_produto("Ração cães adultos 10 kg"), "racao-caes-adultos-10-kg")
        self.assertEqual(chave_do_produto("Tapete higiênico (30 un)"), "tapete-higienico-30-un")

    def test_produto_do_catalogo_tem_foto_propria(self):
        self.assertEqual(imagem_do_produto("Areia higiênica", "higiene"),
                         "/fotos/produtos/areia-higienica.webp")

    def test_produto_novo_cai_na_categoria(self):
        self.assertEqual(imagem_do_produto("Cama ortopédica", "acessorio"),
                         "/fotos/produto-acessorio.webp")

    def test_foto_enviada_pela_equipe_vence(self):
        """Change `foto-do-produto`, D4: a foto enviada vem antes da do app."""
        url = "https://exemplo.xano.io/vault/abc/produto.webp"
        self.assertEqual(imagem_do_produto("Areia higiênica", "higiene", {"url": url}), url)
        self.assertEqual(imagem_do_produto("Cama ortopédica", "acessorio", {"url": url}), url)

    def test_sem_foto_enviada_segue_a_regra_de_antes(self):
        for foto in (None, {}, {"url": ""}, "texto"):
            self.assertEqual(imagem_do_produto("Areia higiênica", "higiene", foto),
                             "/fotos/produtos/areia-higienica.webp", foto)
            self.assertEqual(imagem_do_produto("Cama ortopédica", "acessorio", foto),
                             "/fotos/produto-acessorio.webp", foto)

    def test_todo_produto_de_exemplo_tem_foto(self):
        import scripts.criar_produtos_de_exemplo as exemplo
        for nome, categoria, *_ in exemplo.PRODUTOS:
            self.assertTrue(imagem_do_produto(nome, categoria).startswith("/fotos/produtos/"),
                            nome)


class ArquivosTest(unittest.TestCase):
    """Toda imagem que as funções podem devolver existe de fato em `assets/`."""

    def test_arquivos_existem(self):
        caminhos = {imagem_da_especie(e) for e in ("cão", "gato", "outro")}
        caminhos |= {imagem_da_categoria(c) for c in list(CATEGORIAS_PRODUTO) + [None]}
        caminhos |= {f"/fotos/{n}.webp" for n in
                     ("banner", "vazio-animais", "vazio-pedidos", "vazio-agenda")}
        for caminho in caminhos:
            self.assertTrue(os.path.isfile(os.path.join(ASSETS, caminho.lstrip("/"))), caminho)

    def test_toda_foto_tem_credito(self):
        """Cada arquivo de `assets/fotos/` tem a sua linha em CREDITOS.md."""
        pasta = os.path.join(ASSETS, "fotos")
        with open(os.path.join(pasta, "CREDITOS.md"), encoding="utf-8") as f:
            creditos = f.read()
        fotos = [n for n in os.listdir(pasta) if n.endswith(".webp")]
        fotos += [n for n in os.listdir(os.path.join(pasta, "produtos")) if n.endswith(".webp")]
        self.assertEqual(len(fotos), 30)
        for nome in fotos:
            self.assertIn(f"`{nome}`", creditos, nome)


if __name__ == "__main__":
    unittest.main()
